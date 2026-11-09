"""Risk measures: VaR, expected shortfall, VaR backtests, exposure summaries (topics 195, 196, 500, 501)."""
from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

_ND = NormalDist()


def var_historical(returns: np.ndarray, level: float = 0.99) -> float:
    """Loss quantile as a positive number."""
    return float(-np.quantile(np.asarray(returns, dtype=float), 1 - level))


def var_parametric(returns: np.ndarray, level: float = 0.99) -> float:
    r = np.asarray(returns, dtype=float)
    return float(_ND.inv_cdf(level) * r.std(ddof=1) - r.mean())


def ewma_vol(returns: np.ndarray, lam: float = 0.94) -> float:
    """Latest EWMA volatility estimate (per period), seeded with the first 20 observations."""
    r = np.asarray(returns, dtype=float)
    if len(r) == 0:
        return 0.0
    var = float(np.var(r[:20])) if len(r) >= 2 else float(r[0] ** 2)
    for x in r:
        var = lam * var + (1 - lam) * x * x
    return math.sqrt(var)


def expected_shortfall(returns: np.ndarray, level: float = 0.975) -> float:
    losses = -np.asarray(returns, dtype=float)
    v = np.quantile(losses, level)
    return float(losses[losses >= v].mean())


def _xlogy(x: float, y: float) -> float:
    return 0.0 if x == 0 else x * math.log(y)


def kupiec_pof(exceptions: int, n: int, p: float) -> tuple[float, float]:
    """Kupiec proportion-of-failures test. Returns (LR statistic, p-value from chi-square 1 df)."""
    ph = exceptions / n
    ll0 = _xlogy(n - exceptions, 1 - p) + _xlogy(exceptions, p)
    ll1 = _xlogy(n - exceptions, 1 - ph) + _xlogy(exceptions, ph)
    lr = -2 * (ll0 - ll1)
    return lr, 1 - math.erf(math.sqrt(max(lr, 0.0) / 2))


def exposure_summary(positions: dict[str, float], prices: dict[str, float], equity: float,
                     multipliers: dict[str, float] | None = None) -> dict:
    """Gross, net, leverage, largest position, and Herfindahl index of position values."""
    mult = multipliers or {}
    vals = {s: q * prices[s] * mult.get(s, 1.0) for s, q in positions.items() if q}
    gross = sum(abs(v) for v in vals.values())
    net = sum(vals.values())
    hhi = sum((abs(v) / gross) ** 2 for v in vals.values()) if gross else 0.0
    return {"gross": gross, "net": net, "gross_leverage": gross / equity if equity else 0.0,
            "net_leverage": net / equity if equity else 0.0,
            "largest_position_pct": max((abs(v) for v in vals.values()), default=0.0) / equity if equity else 0.0,
            "herfindahl": hhi}
