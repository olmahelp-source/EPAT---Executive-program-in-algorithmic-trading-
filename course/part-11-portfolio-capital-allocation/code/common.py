"""Shared helpers for the Part 11 worked examples. Needs only numpy."""
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


def port_vol(w, S) -> float:
    return math.sqrt(float(w @ S @ w))


def risk_contrib(w, S) -> np.ndarray:
    """Component contributions RC_i = w_i (S w)_i / sigma_p. They sum to sigma_p."""
    return w * (S @ w) / port_vol(w, S)


def project_capped_simplex(v: np.ndarray, cap: float = 1.0) -> np.ndarray:
    """Euclidean projection onto {w : sum w = 1, 0 <= w <= cap} (bisection on the shift)."""
    n = len(v)
    if n * cap < 1 - 1e-12:
        raise ValueError(f"infeasible: {n} assets x cap {cap} < 1")
    lo, hi = float(v.min()) - cap, float(v.max())
    for _ in range(100):
        tau = 0.5 * (lo + hi)
        if np.clip(v - tau, 0, cap).sum() > 1:
            lo = tau
        else:
            hi = tau
    return np.clip(v - 0.5 * (lo + hi), 0, cap)


def mv_long_only(mu, S, lam: float, cap: float = 1.0, iters: int = 3000) -> np.ndarray:
    """Maximize mu'w - (lam/2) w'Sw over the capped simplex by projected gradient ascent."""
    n = len(mu)
    step = 1.0 / (lam * np.linalg.eigvalsh(S).max())
    w = np.full(n, 1.0 / n)
    for _ in range(iters):
        w = project_capped_simplex(w + step * (mu - lam * S @ w), cap)
    return w


def min_var_long_only(S, cap: float = 1.0, iters: int = 3000) -> np.ndarray:
    return mv_long_only(np.zeros(len(S)), S, 1.0, cap, iters)


def min_var_unconstrained(S) -> np.ndarray:
    w = np.linalg.solve(S, np.ones(len(S)))
    return w / w.sum()
