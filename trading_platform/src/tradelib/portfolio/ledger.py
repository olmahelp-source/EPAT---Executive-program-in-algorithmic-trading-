"""Average-cost position ledger with realized P&L, fees, and position flips (topic 476)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClosedTrade:
    symbol: str
    qty: float          # absolute quantity closed
    side: int           # +1 closed a long, -1 closed a short
    entry: float        # average entry price
    exit: float
    pnl: float          # gross of fees
    ts: int


class Ledger:
    def __init__(self, cash: float) -> None:
        self.cash = float(cash)
        self.initial_cash = float(cash)
        self.pos: dict[str, float] = {}
        self.avg: dict[str, float] = {}
        self.mult: dict[str, float] = {}
        self.realized = 0.0
        self.fees = 0.0
        self.trades: list[ClosedTrade] = []

    def fill(self, symbol: str, signed_qty: float, price: float, fee: float = 0.0,
             multiplier: float = 1.0, ts: int = 0) -> float:
        """Apply a fill and return the realized P&L it produced (before fees)."""
        if signed_qty == 0:
            return 0.0
        self.mult[symbol] = multiplier
        p, a = self.pos.get(symbol, 0.0), self.avg.get(symbol, 0.0)
        self.cash -= signed_qty * price * multiplier + fee
        self.fees += fee
        pnl = 0.0
        if p == 0 or (p > 0) == (signed_qty > 0):                    # opening or adding
            new = p + signed_qty
            a = (a * abs(p) + price * abs(signed_qty)) / abs(new)
            p = new
        else:                                                        # reducing, closing, or flipping
            closed = min(abs(signed_qty), abs(p))
            side = 1 if p > 0 else -1
            pnl = closed * (price - a) * side * multiplier
            self.trades.append(ClosedTrade(symbol, closed, side, a, price, pnl, ts))
            new = p + signed_qty
            if new == 0:
                a = 0.0
            elif (new > 0) != (p > 0):
                a = price                                            # the remainder opens at this price
            p = new
        self.pos[symbol], self.avg[symbol] = p, a
        self.realized += pnl
        return pnl

    def position(self, symbol: str) -> float:
        return self.pos.get(symbol, 0.0)

    def market_value(self, marks: dict[str, float]) -> float:
        return sum(q * marks[s] * self.mult.get(s, 1.0) for s, q in self.pos.items() if q)

    def equity(self, marks: dict[str, float]) -> float:
        return self.cash + self.market_value(marks)

    def unrealized(self, marks: dict[str, float]) -> float:
        return sum(q * (marks[s] - self.avg[s]) * self.mult.get(s, 1.0) for s, q in self.pos.items() if q)

    def gross_notional(self, marks: dict[str, float]) -> float:
        return sum(abs(q) * marks[s] * self.mult.get(s, 1.0) for s, q in self.pos.items() if q)
