"""Shared helpers for the Part 12 worked examples. Needs only numpy."""
from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

ND = NormalDist()


def rng(seed: int = 7) -> np.random.Generator:
    return np.random.default_rng(seed)


def cov_from(vol, corr) -> np.ndarray:
    vol = np.asarray(vol, dtype=float)
    return np.outer(vol, vol) * np.asarray(corr, dtype=float)


def max_drawdown(equity: np.ndarray) -> np.ndarray:
    peak = np.maximum.accumulate(equity, axis=-1)
    return (1 - equity / peak).max(axis=-1)


def chi2_1_sf(x: float) -> float:
    """Survival function of chi-square with 1 degree of freedom."""
    return 1.0 - math.erf(math.sqrt(max(x, 0.0) / 2.0))


def xlogy(x: float, y: float) -> float:
    return 0.0 if x == 0 else x * math.log(y)


# --- Black-Scholes (no dividends) --------------------------------------------------
def _d(S, K, T, r, sig):
    d1 = (math.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * math.sqrt(T))
    return d1, d1 - sig * math.sqrt(T)


def bs_price(S, K, T, r, sig, kind="call") -> float:
    d1, d2 = _d(S, K, T, r, sig)
    if kind == "call":
        return S * ND.cdf(d1) - K * math.exp(-r * T) * ND.cdf(d2)
    return K * math.exp(-r * T) * ND.cdf(-d2) - S * ND.cdf(-d1)


def bs_greeks(S, K, T, r, sig, kind="call") -> dict:
    d1, d2 = _d(S, K, T, r, sig)
    pdf = ND.pdf(d1)
    delta = ND.cdf(d1) if kind == "call" else ND.cdf(d1) - 1
    gamma = pdf / (S * sig * math.sqrt(T))
    vega = S * pdf * math.sqrt(T)                       # per 1.00 (100 points) of volatility
    if kind == "call":
        theta = -S * pdf * sig / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * ND.cdf(d2)
    else:
        theta = -S * pdf * sig / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * ND.cdf(-d2)
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta}
