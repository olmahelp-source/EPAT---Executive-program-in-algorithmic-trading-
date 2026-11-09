"""Order Management System: order state machine, client order IDs, working-exposure accounting.

Topics 521 (OMS), 528 (state machine), 529 (late fills after cancel), 530 (idempotent IDs),
533 (fill processing), 534 (pending exposure).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from tradelib.core.types import Fill, OrderRequest


class State(Enum):
    PENDING_NEW = "pending_new"
    ACKNOWLEDGED = "acknowledged"
    PARTIALLY_FILLED = "partially_filled"
    PENDING_CANCEL = "pending_cancel"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


TERMINAL = {State.FILLED, State.CANCELLED, State.REJECTED, State.EXPIRED}

# A fill can arrive before the acknowledgment (messages can be reordered) and while a cancel
# is pending (the cancel lost the race), so both are legal.
TRANSITIONS: dict[State, set[State]] = {
    State.PENDING_NEW: {State.ACKNOWLEDGED, State.REJECTED, State.PARTIALLY_FILLED, State.FILLED},
    State.ACKNOWLEDGED: {State.PARTIALLY_FILLED, State.FILLED, State.PENDING_CANCEL, State.CANCELLED, State.EXPIRED},
    State.PARTIALLY_FILLED: {State.PARTIALLY_FILLED, State.FILLED, State.PENDING_CANCEL, State.CANCELLED, State.EXPIRED},
    State.PENDING_CANCEL: {State.CANCELLED, State.FILLED, State.PARTIALLY_FILLED, State.ACKNOWLEDGED, State.EXPIRED},
    State.FILLED: set(), State.CANCELLED: set(), State.REJECTED: set(), State.EXPIRED: set(),
}


class InvalidTransition(Exception):
    pass


@dataclass
class Order:
    order_id: str
    request: OrderRequest
    created_ts: int
    state: State = State.PENDING_NEW
    cum_qty: int = 0
    notional: float = 0.0
    fills: list[Fill] = field(default_factory=list)
    reject_reason: str = ""
    _before_cancel: State | None = field(default=None, repr=False)

    @property
    def leaves_qty(self) -> int:
        return self.request.qty - self.cum_qty

    @property
    def avg_price(self) -> float | None:
        return self.notional / self.cum_qty if self.cum_qty else None

    @property
    def is_working(self) -> bool:
        return self.state not in TERMINAL

    def _move(self, new: State) -> None:
        if new not in TRANSITIONS[self.state]:
            raise InvalidTransition(f"{self.order_id}: {self.state.name} -> {new.name}")
        self.state = new


class ClientOrderIdGenerator:
    """IDs are made before sending and reused on retry, so a retry is idempotent (topic 530)."""

    def __init__(self, prefix: str = "ORD", start_seq: int = 0) -> None:
        self.prefix, self._seq = prefix, start_seq

    def next_id(self) -> str:
        self._seq += 1
        return f"{self.prefix}-{self._seq:08d}"

    @property
    def last_seq(self) -> int:
        return self._seq


EventHook = Callable[[str, dict], None]


class OMS:
    def __init__(self, id_gen: ClientOrderIdGenerator | None = None, on_event: EventHook | None = None) -> None:
        self.ids = id_gen or ClientOrderIdGenerator()
        self._orders: dict[str, Order] = {}
        self._on_event = on_event or (lambda kind, data: None)

    # ---- creation and lookup --------------------------------------------------
    def new_order(self, req: OrderRequest, ts: int) -> Order:
        o = Order(self.ids.next_id(), req, ts)
        self._orders[o.order_id] = o
        self._on_event("order_new", {"order_id": o.order_id, "symbol": req.symbol, "side": req.side.name, "qty": req.qty,
                                     "type": req.order_type.value, "limit": req.limit_price, "tif": req.tif.value,
                                     "strategy": req.strategy_id, "ts": ts})
        return o

    def get(self, order_id: str) -> Order:
        return self._orders[order_id]

    def all_orders(self) -> list[Order]:
        return list(self._orders.values())

    def open_orders(self, symbol: str | None = None) -> list[Order]:
        return [o for o in self._orders.values() if o.is_working and (symbol is None or o.request.symbol == symbol)]

    def working_signed_qty(self, symbol: str) -> int:
        """Signed quantity still working (buys positive). Risk must count it (topic 534)."""
        return sum(o.request.side.sign * o.leaves_qty for o in self.open_orders(symbol))

    # ---- events from the broker -----------------------------------------------
    def on_ack(self, order_id: str) -> None:
        o = self._orders[order_id]
        if o.state in (State.PARTIALLY_FILLED, State.FILLED):
            return                                   # a fill overtook the acknowledgment
        o._move(State.ACKNOWLEDGED)
        self._on_event("order_ack", {"order_id": order_id})

    def on_reject(self, order_id: str, reason: str) -> None:
        o = self._orders[order_id]
        o._move(State.REJECTED)
        o.reject_reason = reason
        self._on_event("order_reject", {"order_id": order_id, "reason": reason})

    def on_fill(self, fill: Fill) -> None:
        """A fill is authoritative even if a cancel is pending."""
        o = self._orders[fill.order_id]
        if fill.qty <= 0 or fill.qty > o.leaves_qty:
            raise ValueError(f"bad fill qty {fill.qty}; leaves {o.leaves_qty}")
        o.cum_qty += fill.qty
        o.notional += fill.qty * fill.price
        o.fills.append(fill)
        o._move(State.FILLED if o.leaves_qty == 0 else State.PARTIALLY_FILLED)
        self._on_event("fill", {"order_id": fill.order_id, "symbol": fill.symbol, "side": fill.side.name, "qty": fill.qty,
                                "price": fill.price, "fee": fill.fee, "ts": fill.ts})

    def request_cancel(self, order_id: str) -> None:
        o = self._orders[order_id]
        o._before_cancel = o.state
        o._move(State.PENDING_CANCEL)

    def on_cancel_ack(self, order_id: str) -> bool:
        o = self._orders[order_id]
        if o.state in TERMINAL:
            return False                              # the order filled first; nothing to cancel
        o._move(State.CANCELLED)
        self._on_event("order_cancelled", {"order_id": order_id})
        return True

    def on_cancel_reject(self, order_id: str) -> bool:
        o = self._orders[order_id]
        if o.state != State.PENDING_CANCEL:
            return False
        o._move(o._before_cancel or State.ACKNOWLEDGED)
        return True

    def on_expired(self, order_id: str) -> None:
        o = self._orders[order_id]
        if o.state in TERMINAL:
            return
        o._move(State.EXPIRED)
        self._on_event("order_expired", {"order_id": order_id})
