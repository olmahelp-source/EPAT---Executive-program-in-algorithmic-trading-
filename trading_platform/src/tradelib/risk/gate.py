"""Pre-trade risk gate: every order must pass it (topics 497, 538, 539, 534)."""
from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field

from tradelib.core.types import OrderRequest, OrderType


@dataclass
class Limits:
    max_order_qty: int = 10 ** 9
    max_order_notional: float = math.inf
    max_position_pct: float = 1.0          # |position value| per symbol as a fraction of equity
    max_gross_leverage: float = 2.0        # gross notional / equity after the order
    collar_pct: float = 0.10               # limit price must be within this of the reference price
    max_ref_age_s: float = math.inf        # reference price must be at most this old
    max_orders_per_window: int = 10 ** 9
    window_s: float = 1.0


@dataclass
class RiskContext:
    position: int                  # confirmed signed position (shares or contracts)
    working_signed: int            # signed quantity of orders still working
    equity: float
    gross_notional: float          # current gross exposure across the book
    ref_price: float
    ref_ts: int
    now_ts: int
    multiplier: float = 1.0


@dataclass
class RiskDecision:
    ok: bool
    reasons: list[str] = field(default_factory=list)


class RiskGate:
    def __init__(self, limits: Limits | None = None) -> None:
        self.limits = limits or Limits()
        self._recent: deque[float] = deque()
        self.halted = False

    def halt(self) -> None:
        self.halted = True

    def resume(self) -> None:
        self.halted = False

    def check(self, req: OrderRequest, ctx: RiskContext) -> RiskDecision:
        L, why = self.limits, []
        if self.halted:
            why.append("trading halted")
        if req.qty <= 0:
            why.append("non-positive quantity")
        if req.qty > L.max_order_qty:
            why.append(f"order quantity {req.qty} above limit {L.max_order_qty}")
        px = req.limit_price if (req.order_type == OrderType.LIMIT and req.limit_price) else ctx.ref_price
        notional = req.qty * px * ctx.multiplier
        if notional > L.max_order_notional:
            why.append("order notional above limit")
        if ctx.now_ts - ctx.ref_ts > L.max_ref_age_s:
            why.append("reference price stale")
        elif req.order_type == OrderType.LIMIT and req.limit_price and ctx.ref_price > 0:
            if abs(req.limit_price - ctx.ref_price) / ctx.ref_price > L.collar_pct:
                why.append("limit price outside collar")

        before = ctx.position + ctx.working_signed
        after = before + req.signed_qty
        if req.reduce_only and (abs(after) > abs(before) or before * after < 0):
            why.append("reduce-only order would increase or flip the position")
        if ctx.equity > 0:
            if abs(after) * ctx.ref_price * ctx.multiplier > L.max_position_pct * ctx.equity:
                why.append("projected position above per-symbol limit")
            gross_after = ctx.gross_notional + (abs(after) - abs(before)) * ctx.ref_price * ctx.multiplier
            if gross_after > L.max_gross_leverage * ctx.equity and abs(after) > abs(before):
                why.append("projected gross leverage above limit")

        while self._recent and ctx.now_ts - self._recent[0] >= L.window_s:
            self._recent.popleft()
        if len(self._recent) >= L.max_orders_per_window:
            why.append("order rate limit")
        if not why:
            self._recent.append(ctx.now_ts)
        return RiskDecision(ok=not why, reasons=why)
