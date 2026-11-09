"""Synthetic market data for tests, demos, and paper trading (topics 445, 585).

Correlated geometric Brownian motion with optional volatility regimes. This is test data,
not a market model: do not draw performance conclusions from it.
"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

from tradelib.core.types import Bar


def business_day_timestamps(start: dt.date, n: int) -> list[int]:
    """Epoch seconds (00:00 UTC) of the next n weekdays starting at `start`."""
    out, d = [], start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp()))
        d += dt.timedelta(days=1)
    return out


def generate_bars(symbols: list[str], n_days: int, seed: int = 7, start: dt.date = dt.date(2020, 1, 1),
                  start_price: float | list[float] = 100.0, drift: float | list[float] = 0.06,
                  vol: float | list[float] = 0.18, corr: float = 0.3, avg_volume: float = 1_000_000.0,
                  regime_vol_mult: float = 1.0, regime_len: int = 126) -> dict[str, list[Bar]]:
    """Daily OHLCV bars per symbol. regime_vol_mult > 1 alternates calm and turbulent blocks."""
    n = len(symbols)

    def arr(x):
        return np.full(n, float(x)) if np.isscalar(x) else np.asarray(x, dtype=float)

    p0, mu, sg = arr(start_price), arr(drift), arr(vol)
    rng = np.random.default_rng(seed)
    C = np.full((n, n), corr)
    np.fill_diagonal(C, 1.0)
    L = np.linalg.cholesky(C)
    ts = business_day_timestamps(start, n_days)
    z = rng.normal(size=(n_days, n)) @ L.T
    mult = np.where((np.arange(n_days) // regime_len) % 2 == 1, regime_vol_mult, 1.0)
    dailyvol = sg[None, :] * mult[:, None] / math.sqrt(252)
    rets = (mu[None, :] - 0.5 * sg[None, :] ** 2) / 252 + dailyvol * z
    close = p0[None, :] * np.exp(np.cumsum(rets, axis=0))
    prev = np.vstack([p0, close[:-1]])
    out: dict[str, list[Bar]] = {s: [] for s in symbols}
    for i, s in enumerate(symbols):
        for t in range(n_days):
            o = prev[t, i] * (1 + rng.normal(0, 0.1) * dailyvol[t, i])           # small overnight gap
            c = close[t, i]
            span = abs(rng.normal(0, 0.6)) * dailyvol[t, i] * c
            hi, lo = max(o, c) + span, max(min(o, c) - span, 0.01)
            vol_t = float(avg_volume * rng.lognormal(0, 0.3))
            out[s].append(Bar(s, ts[t], round(o, 4), round(hi, 4), round(lo, 4), round(c, 4), round(vol_t)))
    return out
