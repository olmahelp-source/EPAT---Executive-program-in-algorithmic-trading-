"""Shared helpers for the Part 2 worked examples. Needs only numpy."""
from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

ND = NormalDist()
GAMMA_EULER = 0.5772156649015329

DF_CRIT_5 = -2.86   # Dickey-Fuller 5% critical value, constant, no trend
EG_CRIT_5 = -3.34   # Engle-Granger 5% critical value, two variables (approx.)


def rng(seed: int = 7) -> np.random.Generator:
    return np.random.default_rng(seed)


def ols(X: np.ndarray, y: np.ndarray):
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    return beta, y - X @ beta


def ols_se(X: np.ndarray, y: np.ndarray):
    beta, resid = ols(X, y)
    n, k = X.shape
    s2 = resid @ resid / (n - k)
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta, np.sqrt(np.diag(cov)), resid


def moments(x: np.ndarray):
    """Return mean, population std, skewness, kurtosis (not excess)."""
    m = x.mean()
    d = x - m
    v = (d ** 2).mean()
    return float(m), math.sqrt(v), float((d ** 3).mean() / v ** 1.5), float((d ** 4).mean() / v ** 2)


def acf(x: np.ndarray, k: int) -> float:
    d = x - x.mean()
    return float(d[k:] @ d[:-k] / (d @ d))


def dickey_fuller_t(y: np.ndarray) -> float:
    """t-statistic of gamma in dy_t = a + gamma*y_{t-1} + e_t."""
    dy = np.diff(y)
    X = np.column_stack([np.ones(len(dy)), y[:-1]])
    beta, se, _ = ols_se(X, dy)
    return float(beta[1] / se[1])


def sharpe(r: np.ndarray) -> float:
    return float(r.mean() / r.std(ddof=1))


def psr(sr: float, sr0: float, n: int, skew: float, kurt: float) -> float:
    """Probabilistic Sharpe ratio: P(true SR > sr0). Per-period SR, non-excess kurtosis."""
    denom = math.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr ** 2)
    return ND.cdf((sr - sr0) * math.sqrt(n - 1) / denom)


def expected_max_sr(var_trials: float, n_trials: int) -> float:
    """Expected maximum Sharpe among n_trials unskilled trials (Bailey and Lopez de Prado)."""
    return math.sqrt(var_trials) * (
        (1 - GAMMA_EULER) * ND.inv_cdf(1 - 1 / n_trials)
        + GAMMA_EULER * ND.inv_cdf(1 - 1 / (n_trials * math.e))
    )


def block_indices(n: int, L: int, g: np.random.Generator) -> np.ndarray:
    """Moving-block bootstrap indices of length n with block length L."""
    nb = math.ceil(n / L)
    starts = g.integers(0, n - L + 1, nb)
    return (starts[:, None] + np.arange(L)).ravel()[:n]


def norm_pdf(x: float, mu: float, sd: float) -> float:
    z = (x - mu) / sd
    return math.exp(-0.5 * z * z) / (sd * math.sqrt(2 * math.pi))


def bs_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * ND.cdf(d1) - K * math.exp(-r * T) * ND.cdf(d2)
