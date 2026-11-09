"""Limit order book with price-time priority (topics 3, 91, 771).

Reference implementation. Price levels live in sorted lists, so insert is O(n) in the number
of levels. A production book would use arrays or intrusive lists.
"""
from __future__ import annotations

from bisect import insort
from collections import deque
from dataclasses import dataclass


@dataclass
class BookFill:
    taker_id: str
    maker_id: str
    price: float
    qty: int


@dataclass
class _Resting:
    order_id: str
    side: str  # "B" or "S"
    price: float
    qty: int


class OrderBook:
    def __init__(self) -> None:
        self._levels: dict[str, dict[float, deque[_Resting]]] = {"B": {}, "S": {}}
        self._prices: dict[str, list[float]] = {"B": [], "S": []}  # ascending
        self._index: dict[str, _Resting] = {}

    @property
    def best_bid(self) -> float | None:
        return self._prices["B"][-1] if self._prices["B"] else None

    @property
    def best_ask(self) -> float | None:
        return self._prices["S"][0] if self._prices["S"] else None

    @property
    def spread(self) -> float | None:
        b, a = self.best_bid, self.best_ask
        return None if b is None or a is None else a - b

    @property
    def mid(self) -> float | None:
        b, a = self.best_bid, self.best_ask
        return None if b is None or a is None else (a + b) / 2

    def spread_bps(self) -> float | None:
        s, m = self.spread, self.mid
        return None if s is None or not m else s / m * 1e4

    def microprice(self) -> float | None:
        """(bid x ask size + ask x bid size) / (bid size + ask size), a short-term price hint (topic 595)."""
        if self.best_bid is None or self.best_ask is None:
            return None
        bq = sum(o.qty for o in self._levels["B"][self.best_bid])
        aq = sum(o.qty for o in self._levels["S"][self.best_ask])
        return (self.best_bid * aq + self.best_ask * bq) / (bq + aq)

    def imbalance(self, levels: int = 5) -> float:
        """(bid depth - ask depth) / (bid depth + ask depth) over the top levels, in [-1, 1]."""
        b = sum(q for _, q in self.depth("B", levels))
        a = sum(q for _, q in self.depth("S", levels))
        return 0.0 if a + b == 0 else (b - a) / (a + b)

    def depth(self, side: str, levels: int = 5) -> list[tuple[float, int]]:
        prices = self._prices[side]
        ordered = reversed(prices) if side == "B" else iter(prices)
        out = []
        for p in ordered:
            out.append((p, sum(o.qty for o in self._levels[side][p])))
            if len(out) == levels:
                break
        return out

    def add_limit(self, order_id: str, side: str, price: float, qty: int) -> list[BookFill]:
        if order_id in self._index:
            raise ValueError(f"duplicate order id {order_id}")
        if side not in ("B", "S") or qty <= 0:
            raise ValueError("bad side or quantity")
        fills = self._match(order_id, side, price, qty)
        remaining = qty - sum(f.qty for f in fills)
        if remaining > 0:
            self._rest(_Resting(order_id, side, price, remaining))
        return fills

    def cancel(self, order_id: str) -> bool:
        order = self._index.pop(order_id, None)
        if order is None:
            return False
        level = self._levels[order.side][order.price]
        level.remove(order)
        if not level:
            del self._levels[order.side][order.price]
            self._prices[order.side].remove(order.price)
        return True

    def _rest(self, order: _Resting) -> None:
        levels = self._levels[order.side]
        if order.price not in levels:
            levels[order.price] = deque()
            insort(self._prices[order.side], order.price)
        levels[order.price].append(order)
        self._index[order.order_id] = order

    def _match(self, taker_id: str, side: str, price: float, qty: int) -> list[BookFill]:
        opp = "S" if side == "B" else "B"
        fills: list[BookFill] = []
        while qty > 0 and self._prices[opp]:
            best = self._prices[opp][0] if opp == "S" else self._prices[opp][-1]
            crosses = best <= price if side == "B" else best >= price
            if not crosses:
                break
            level = self._levels[opp][best]
            while qty > 0 and level:
                maker = level[0]
                traded = min(qty, maker.qty)
                fills.append(BookFill(taker_id, maker.order_id, best, traded))
                maker.qty -= traded
                qty -= traded
                if maker.qty == 0:
                    level.popleft()
                    del self._index[maker.order_id]
            if not level:
                del self._levels[opp][best]
                self._prices[opp].remove(best)
        return fills
