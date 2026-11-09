"""Section 2.2 worked examples (topics 57 to 65). Run: python3 ex_2_2_advanced.py"""
from __future__ import annotations

import math

import numpy as np

from common import ND, acf, block_indices, ols, psr, rng


# 57 ---------------------------------------------------------------------------
def t57_reality_check():
    g = rng(21)
    n, m, B, L = 500, 50, 1000, 10
    R = g.normal(0.0, 0.01, (n, m))                 # 50 strategies with zero true skill
    means = R.mean(0)
    tstats = means / (R.std(0, ddof=1) / math.sqrt(n))
    obs = math.sqrt(n) * means.max()
    Rc = R - means                                  # impose the null: every mean is zero
    boot = np.empty(B)
    for b in range(B):
        idx = block_indices(n, L, g)
        boot[b] = math.sqrt(n) * Rc[idx].mean(0).max()
    return {"best_strategy_t_stat": float(tstats.max()),
            "naive_p_best": 1 - ND.cdf(float(tstats.max())),
            "reality_check_p": float((boot >= obs).mean()),
            "expected_max_t_of_50_nulls": ND.inv_cdf(1 - 1 / 50)}


# 58 ---------------------------------------------------------------------------
def lo_eta(q: int, rho: list[float]) -> float:
    """Lo (2002) annualization factor for Sharpe under autocorrelation rho_1..rho_{q-1}."""
    return q / math.sqrt(q + 2 * sum((q - k) * rho[k - 1] for k in range(1, q)))


def min_track_record(sr: float, sr0: float, skew: float, kurt: float, z: float = 1.645) -> float:
    return 1 + (1 - skew * sr + (kurt - 1) / 4 * sr ** 2) * (z / (sr - sr0)) ** 2


def t58_lo_and_mintrl():
    sr_m = 0.20                                      # monthly Sharpe
    rho = [0.30, 0.10, 0.05] + [0.0] * 8
    eta = lo_eta(12, rho)
    sr_d = 1.0 / math.sqrt(252)
    n_star = min_track_record(sr_d, 0.0, -0.5, 5.0)
    return {"naive_annual_sharpe": sr_m * math.sqrt(12), "eta_lo": eta, "lo_annual_sharpe": sr_m * eta,
            "min_track_record_days": n_star, "min_track_record_years": n_star / 252}


# 59 ---------------------------------------------------------------------------
def t59_ergodicity():
    up, down = 1.5, 0.6                              # each round: +50% or -40%, 50/50
    ensemble = 0.5 * up + 0.5 * down
    time_avg = math.sqrt(up * down)
    g = rng(22)
    players, rounds = 20_000, 100
    wealth = np.prod(np.where(g.random((players, rounds)) < 0.5, up, down), axis=1)
    return {"expected_growth_per_round": ensemble - 1, "time_average_growth_per_round": time_avg - 1,
            "expected_wealth_after_100": ensemble ** rounds,
            "median_wealth_theory": time_avg ** rounds,
            "median_wealth_simulated": float(np.median(wealth)),
            "share_of_players_below_start": float((wealth < 1).mean()),
            "share_of_players_below_10pct": float((wealth < 0.1).mean())}


# 60 ---------------------------------------------------------------------------
def granger_F(y: np.ndarray, x: np.ndarray, p: int = 2) -> float:
    n = len(y)
    Y = y[p:]
    own = [y[p - k:n - k] for k in range(1, p + 1)]
    oth = [x[p - k:n - k] for k in range(1, p + 1)]
    Xr = np.column_stack([np.ones(n - p)] + own)
    Xu = np.column_stack([np.ones(n - p)] + own + oth)
    _, rr = ols(Xr, Y)
    _, ru = ols(Xu, Y)
    rss_r, rss_u = rr @ rr, ru @ ru
    return ((rss_r - rss_u) / p) / (rss_u / (n - p - Xu.shape[1]))


def t60_granger():
    g = rng(23)
    n = 600
    x = g.normal(size=n)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = 0.4 * y[t - 1] + 0.3 * x[t - 1] + g.normal()
    return {"F_x_causes_y": granger_F(y, x), "F_y_causes_x": granger_F(x, y), "approx_5pct_crit_F(2,590)": 3.01}


# 61 ---------------------------------------------------------------------------
def quantile_reg(x: np.ndarray, y: np.ndarray, tau: float, iters: int = 200):
    X = np.column_stack([np.ones(len(x)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    for _ in range(iters):
        r = y - X @ b
        w = np.where(r > 0, tau, 1 - tau) / np.maximum(np.abs(r), 1e-6)
        b = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * y))
    return b


def t61_quantile_regression():
    g = rng(24)
    n = 5000
    x = g.uniform(0, 2, n)
    y = 0.3 * x + (0.5 + 0.5 * x) * g.normal(size=n)   # spread widens with x
    out = {}
    for tau in (0.05, 0.5, 0.95):
        b = quantile_reg(x, y, tau)
        z = ND.inv_cdf(tau)
        out[f"tau={tau}"] = {"intercept": round(float(b[0]), 3), "slope": round(float(b[1]), 3),
                             "theory_intercept": round(0.5 * z, 3), "theory_slope": round(0.3 + 0.5 * z, 3)}
    return out


# 62 ---------------------------------------------------------------------------
def variance_ratio(r: np.ndarray, q: int) -> float:
    rq = np.convolve(r, np.ones(q), mode="valid")       # overlapping q-period returns
    return float(rq.var(ddof=1) / (q * r.var(ddof=1)))


def t62_variance_ratio():
    g = rng(25)
    n = 20000
    out = {}
    for name, phi in (("random_walk", 0.0), ("trending_phi=+0.2", 0.2), ("mean_reverting_phi=-0.2", -0.2)):
        e = g.normal(size=n)
        r = np.empty(n)
        r[0] = e[0]
        for t in range(1, n):
            r[t] = phi * r[t - 1] + e[t]
        out[name] = {f"VR({q})": round(variance_ratio(r, q), 3) for q in (2, 5, 10)}
    return out


# 63 ---------------------------------------------------------------------------
def t63_ou_half_life():
    g = rng(26)
    theta, mu, sigma, n, sims = 0.10, 0.0, 1.0, 500, 400
    phi = math.exp(-theta)
    sd = sigma * math.sqrt((1 - phi ** 2) / (2 * theta))
    hl = []
    for _ in range(sims):
        x = np.empty(n)
        x[0] = mu
        for t in range(1, n):
            x[t] = mu + (x[t - 1] - mu) * phi + sd * g.normal()
        X = np.column_stack([np.ones(n - 1), x[:-1]])
        b, _ = ols(X, np.diff(x))
        if b[1] < 0:
            hl.append(math.log(2) / -math.log(1 + b[1]))
    hl = np.array(hl)
    return {"true_theta": theta, "true_half_life": math.log(2) / theta, "n_per_sample": n,
            "median_estimate": float(np.median(hl)), "p10_p90": (float(np.quantile(hl, 0.1)), float(np.quantile(hl, 0.9)))}


# 64 ---------------------------------------------------------------------------
def t64_filter_lookahead():
    g = rng(27)
    n, w = 20000, 11
    r = g.normal(0, 0.01, n)                             # pure noise returns: nothing to predict
    p = np.cumsum(r)
    half = w // 2
    cent = np.convolve(p, np.ones(w) / w, mode="same")  # two-sided moving average (uses the future)
    alpha = 2 / (w + 1)
    ema = np.empty(n)
    ema[0] = p[0]
    for t in range(1, n):
        ema[t] = alpha * p[t] + (1 - alpha) * ema[t - 1]
    # slope at time t = filter[t] - filter[t-1]; compare with the NEXT return r[t+1].
    slope_c, slope_e = np.diff(cent)[:-1], np.diff(ema)[:-1]   # times 1..n-2
    nxt = r[2:]                                                  # r[t+1] for t = 1..n-2
    c = slice(half + 1, len(nxt) - half - 1)                     # drop edge effects of "same" convolution
    corr_c = float(np.corrcoef(slope_c[c], nxt[c])[0, 1])
    corr_e = float(np.corrcoef(slope_e[c], nxt[c])[0, 1])
    return {"corr(centered_slope, next_return)": corr_c, "corr(EMA_slope, next_return)": corr_e}


# 65 ---------------------------------------------------------------------------
def t65_effective_sample_size():
    g = rng(28)
    n, L, sims = 1000, 5, 2000
    means = np.empty(sims)
    naive_se = np.empty(sims)
    for s in range(sims):
        d = g.normal(0, 0.01, n + L - 1)
        o = np.convolve(d, np.ones(L), mode="valid")     # overlapping 5-day sums, n of them
        means[s] = o.mean()
        naive_se[s] = o.std(ddof=1) / math.sqrt(n)
    rho = [(L - k) / L for k in range(1, L)]
    factor = 1 + 2 * sum(rho)
    return {"empirical_se_of_mean": float(means.std()), "naive_se_average": float(naive_se.mean()),
            "inflation_factor_sqrt": float(means.std() / naive_se.mean()), "theory_sqrt_factor": math.sqrt(factor),
            "n_effective": n / factor}


ALL = [t57_reality_check, t58_lo_and_mintrl, t59_ergodicity, t60_granger, t61_quantile_regression,
       t62_variance_ratio, t63_ou_half_life, t64_filter_lookahead, t65_effective_sample_size]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
