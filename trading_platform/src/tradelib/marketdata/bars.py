"""Bar construction from ticks (topics 202, 204).

Only COMPLETED bars are ever returned, so downstream code cannot use a bar that is
still forming (the look-ahead trap described in topic 268).
"""
from __future__ import annotations

from tradelib.core.types import Bar


class BarBuilder:
    """Build time, volume, or dollar bars from a tick stream.

    kind="time":   threshold = bar length in seconds
    kind="volume": threshold = shares per bar
    kind="dollar": threshold = notional per bar
    """

    def __init__(self, symbol: str, kind: str = "time", threshold: float = 60.0) -> None:
        if kind not in ("time", "volume", "dollar"):
            raise ValueError("kind must be time, volume, or dollar")
        if threshold <= 0:
            raise ValueError("threshold must be positive")
        self.symbol, self.kind, self.threshold = symbol, kind, threshold
        self._reset()
        self._bucket: int | None = None

    def _reset(self) -> None:
        self._o = self._h = self._l = self._c = None
        self._v = 0.0
        self._acc = 0.0
        self._start: int | None = None

    def _start_bar(self, ts: int, price: float) -> None:
        self._o = self._h = self._l = self._c = price
        self._v, self._acc, self._start = 0.0, 0.0, ts

    def _add(self, price: float, size: float) -> None:
        self._h, self._l, self._c = max(self._h, price), min(self._l, price), price
        self._v += size
        self._acc += size if self.kind == "volume" else price * size

    def _emit(self, ts: int) -> Bar:
        bar = Bar(self.symbol, ts, self._o, self._h, self._l, self._c, self._v)
        self._reset()
        return bar

    def update(self, ts: int, price: float, size: float) -> Bar | None:
        if price <= 0 or size < 0:
            raise ValueError("price must be positive and size non-negative")
        if self.kind == "time":
            bucket = int(ts // self.threshold)
            done = None
            if self._bucket is not None and bucket != self._bucket:
                done = self._emit(int(self._bucket * self.threshold))
            if self._o is None:
                self._start_bar(ts, price)
            self._bucket = bucket
            self._add(price, size)
            return done
        if self._o is None:
            self._start_bar(ts, price)
        self._add(price, size)
        if self._acc >= self.threshold:
            return self._emit(self._start)
        return None

    @property
    def has_partial_bar(self) -> bool:
        """True while a bar is still forming. That bar is NOT available to strategies."""
        return self._o is not None
