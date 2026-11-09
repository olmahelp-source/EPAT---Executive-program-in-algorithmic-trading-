"""Data cleaning and corporate-action adjustment (topics 80, 81, 84)."""
from __future__ import annotations

from dataclasses import dataclass, field

from tradelib.core.types import Bar


@dataclass
class CleanReport:
    kept: int = 0
    dropped: dict[str, int] = field(default_factory=dict)

    def _drop(self, reason: str) -> None:
        self.dropped[reason] = self.dropped.get(reason, 0) + 1


def clean_bars(bars: list[Bar], max_jump: float = 0.5) -> tuple[list[Bar], CleanReport]:
    """Drop bars that are clearly invalid. Every drop is counted by reason.

    Rules: non-positive prices, high below low, open or close outside the high-low range,
    negative volume, non-increasing timestamps, and single-bar moves above max_jump
    (default 50%). A large real move can be dropped by the last rule, so check the report.
    """
    out: list[Bar] = []
    rep = CleanReport()
    for b in bars:
        if min(b.open, b.high, b.low, b.close) <= 0:
            rep._drop("non_positive_price")
        elif b.high < b.low:
            rep._drop("high_below_low")
        elif not (b.low <= b.open <= b.high and b.low <= b.close <= b.high):
            rep._drop("open_or_close_outside_range")
        elif b.volume < 0:
            rep._drop("negative_volume")
        elif out and b.ts <= out[-1].ts:
            rep._drop("timestamp_not_increasing")
        elif out and abs(b.close / out[-1].close - 1) > max_jump:
            rep._drop("jump_over_threshold")
        else:
            out.append(b)
            rep.kept += 1
    return out, rep


def apply_split(bars: list[Bar], ratio: float, effective_ts: int) -> list[Bar]:
    """Adjust history for a split: bars BEFORE effective_ts get prices / ratio, volume x ratio.

    ratio=2 means a 2-for-1 split. Keep the raw series too: raw prices are needed for
    order sizing and price-level rules (topic 203).
    """
    if ratio <= 0:
        raise ValueError("ratio must be positive")
    out = []
    for b in bars:
        if b.ts < effective_ts:
            out.append(Bar(b.symbol, b.ts, b.open / ratio, b.high / ratio, b.low / ratio, b.close / ratio, b.volume * ratio))
        else:
            out.append(b)
    return out
