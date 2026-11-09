"""Paper (simulated) broker.

It doubles as the simulated exchange for backtests: the same ``submit_order`` /
event interface as a live gateway, so strategy, risk and OMS code run unchanged.
Fills are driven by bars (``process_bar``) or quotes (``update_quote``).
"""
from __future__ import annotations

import dataclasses
import threading
from typing import Dict, List, Optional

from ..core.config import CostConfig
from ..core.enums import OrderType, Side, TimeInForce
from ..core.exceptions import BrokerConnectionError, OrderRejectedError
from ..core.models import Bar, Fill, Order
from ..utils.helpers import IdGenerator
from .base import BROKERS, BrokerEvent, BrokerGateway
from .costs import CostModel


@BROKERS.register("paper")
class PaperBroker(BrokerGateway):
    name = "paper"

    def __init__(self, initial_cash: float = 100_000.0, cost_model: Optional[CostModel] = None,
                 max_participation: Optional[float] = None, allow_short: bool = True,
                 immediate_market: bool = False, credentials=None, paper: bool = True) -> None:
        super().__init__()
        self.cash = float(initial_cash)
        self.costs = cost_model or CostModel(CostConfig())
        self.max_participation = max_participation   # fraction of bar volume per bar
        self.allow_short = allow_short
        self.immediate_market = immediate_market     # fill market orders at last quote on submit
        self._positions: Dict[str, float] = {}
        self._last: Dict[str, float] = {}
        self._open: Dict[str, Order] = {}
        self._seen_client_ids: set = set()
        self._ids = IdGenerator("BRK")
        self._lock = threading.RLock()
        self._fill_ids = IdGenerator("FIL")
        self._fail_next: List[Exception] = []
        self.now = None  # set by caller (backtest) to stamp fills; falls back to bar ts

    # ---- lifecycle ----------------------------------------------------------------------
    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    # ---- testing hook: simulate outages ---------------------------------------------------
    def fail_next(self, exc: Exception, times: int = 1) -> None:
        self._fail_next.extend([exc] * times)

    # ---- order entry --------------------------------------------------------------------
    def submit_order(self, order: Order) -> str:
        with self._lock:
            self._require_connected()
            if self._fail_next:
                raise self._fail_next.pop(0)
            if order.client_order_id in self._seen_client_ids:
                raise OrderRejectedError("duplicate client order id", code="DUPLICATE_ID")
            if order.quantity <= 0:
                raise OrderRejectedError("non-positive quantity")
            self._seen_client_ids.add(order.client_order_id)
            bid = self._ids.next()
            # the broker keeps its OWN copy; the OMS copy is only changed via events
            mine = dataclasses.replace(order, broker_order_id=bid, filled_qty=0.0, fills=[])
            self._open[order.client_order_id] = mine
            self._emit(BrokerEvent("ack", order.client_order_id, bid))
            if self.immediate_market and mine.order_type is OrderType.MARKET and mine.symbol in self._last:
                self._execute(mine, self._last[mine.symbol], mine.remaining, ts=self.now)
            return bid

    def cancel_order(self, order: Order) -> None:
        with self._lock:
            self._require_connected()
            mine = self._open.pop(order.client_order_id, None)
            if mine is None:
                raise OrderRejectedError("order not open at broker", code="UNKNOWN_ORDER")
            self._emit(BrokerEvent("cancelled", order.client_order_id, mine.broker_order_id))

    def get_positions(self) -> Dict[str, float]:
        with self._lock:
            return {s: q for s, q in self._positions.items() if abs(q) > 1e-12}

    def get_cash(self) -> float:
        return self.cash

    def open_order_ids(self) -> set:
        return set(self._open)

    # ---- market-driven matching ----------------------------------------------------------
    def update_quote(self, symbol: str, price: float, ts=None, volume: float = 0.0) -> None:
        """Tick-style update: treat as a degenerate bar."""
        self.process_bar(Bar(ts, symbol, price, price, price, price, volume))

    def process_bar(self, bar: Bar) -> None:
        with self._lock:
            self._last[bar.symbol] = bar.close
            capacity = (bar.volume * self.max_participation) if (self.max_participation and bar.volume > 0) else None
            for order in [o for o in list(self._open.values()) if o.symbol == bar.symbol]:
                px = self._match_price(order, bar)
                if px is not None:
                    qty = order.remaining if capacity is None else min(order.remaining, capacity)
                    if capacity is not None:
                        capacity -= qty
                    if qty > 0:
                        if order.tif is TimeInForce.FOK and qty < order.remaining:
                            self._open.pop(order.client_order_id, None)
                            self._emit(BrokerEvent("expired", order.client_order_id, order.broker_order_id,
                                                   reason="FOK not fully fillable"))
                            continue
                        self._execute(order, px, qty, ts=bar.ts, bar=bar)
                if order.client_order_id in self._open and order.tif in (TimeInForce.IOC, TimeInForce.FOK):
                    self._open.pop(order.client_order_id, None)
                    self._emit(BrokerEvent("expired", order.client_order_id, order.broker_order_id,
                                           reason="IOC remainder cancelled"))

    def _match_price(self, order: Order, bar: Bar) -> Optional[float]:
        """Price at which ``order`` would trade during ``bar``, or None."""
        buy = order.side is Side.BUY
        t = order.order_type
        if t is OrderType.MARKET:
            return bar.open
        if t is OrderType.LIMIT:
            lp = order.limit_price
            if buy and bar.low <= lp:
                return min(bar.open, lp)
            if not buy and bar.high >= lp:
                return max(bar.open, lp)
            return None
        sp = order.stop_price
        triggered = (buy and bar.high >= sp) or (not buy and bar.low <= sp)
        if not triggered:
            return None
        stop_px = max(bar.open, sp) if buy else min(bar.open, sp)   # gaps fill at open
        if t is OrderType.STOP:
            return stop_px
        lp = order.limit_price                                      # STOP_LIMIT
        if buy and stop_px <= lp:
            return stop_px
        if not buy and stop_px >= lp:
            return stop_px
        return None

    def _execute(self, order: Order, ref_price: float, qty: float, ts, bar: Optional[Bar] = None) -> None:
        pos = self._positions.get(order.symbol, 0.0)
        new_pos = pos + order.side.sign * qty
        if not self.allow_short and new_pos < -1e-12:
            self._open.pop(order.client_order_id, None)
            self._emit(BrokerEvent("rejected", order.client_order_id, order.broker_order_id,
                                   reason="short selling disabled"))
            return
        is_limit_like = order.order_type in (OrderType.LIMIT, OrderType.STOP_LIMIT)
        # passive limit fills get no slippage; marketable ones pay costs
        px = ref_price if is_limit_like else self.costs.fill_price(
            order.side, ref_price, qty, adv=(bar.volume if bar and bar.volume > 0 else None), volatility=None)
        commission = self.costs.commission(qty, px) + self.costs.tax(order.side, qty * px)
        self.cash -= order.side.sign * qty * px + commission
        self._positions[order.symbol] = new_pos
        fill = Fill(self._fill_ids.next(), order.client_order_id, order.symbol, order.side, qty, px,
                    ts, commission, order.strategy_id, order.account_id, order.broker_order_id)
        order.filled_qty += qty
        if order.filled_qty >= order.quantity - 1e-12:
            self._open.pop(order.client_order_id, None)
        self._emit(BrokerEvent("fill", order.client_order_id, order.broker_order_id, fill=fill))
