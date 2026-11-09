"""CSV reading and writing for bars. Columns: symbol,ts,open,high,low,close,volume."""
from __future__ import annotations

import csv
from pathlib import Path

from tradelib.core.types import Bar

FIELDS = ["symbol", "ts", "open", "high", "low", "close", "volume"]


def write_bars_csv(path: str | Path, bars_by_symbol: dict[str, list[Bar]]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(FIELDS)
        for s in sorted(bars_by_symbol):
            for b in bars_by_symbol[s]:
                w.writerow([b.symbol, b.ts, b.open, b.high, b.low, b.close, b.volume])


def read_bars_csv(path: str | Path) -> dict[str, list[Bar]]:
    out: dict[str, list[Bar]] = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            b = Bar(row["symbol"], int(row["ts"]), float(row["open"]), float(row["high"]),
                    float(row["low"]), float(row["close"]), float(row["volume"]))
            out.setdefault(b.symbol, []).append(b)
    for s in out:
        out[s].sort(key=lambda x: x.ts)
    return out
