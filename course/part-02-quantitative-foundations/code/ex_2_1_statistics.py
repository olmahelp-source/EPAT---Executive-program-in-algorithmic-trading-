"""Section 2.1 worked examples (topics 36 to 56). Run: python3 ex_2_1_statistics.py"""
from __future__ import annotations

import math

import numpy as np

from common import (ND, DF_CRIT_5, EG_CRIT_5, acf, block_indices, dickey_fuller_t,
                    expected_max_sr, moments, norm_pdf, ols, ols_se, psr, rng, sharpe)


# 36 ---------------------------------------------------------------------------
def t36_descriptive():
    r = np.array([0.012, -0.008, 0.004, 0.015, -0.021, 0.009, 0.002, -0.005, 0.018, -0.012])
    m, s, sk, ku = moments(r)
    g = rng(1)
    fat = 0.01 * g.standard_t(5, 200_000) / math.sqrt(5 / 3)   # t5 scaled to 1% std
    _, _, sk2, ku2 = moments(fat)
    return {"mean": m, "std_sample": float(r.std(ddof=1)), "skew": sk, "excess_kurt": ku - 3,
            "t5_excess_kurt_sim": ku2 - 3, "t5_excess_kurt_theory": 6.0}


# 37 ---------------------------------------------------------------------------
def t_logpdf(x, df, loc, scale):
    z = (x - loc) / scale
    return (math.lgamma((df + 1) / 2) - math.lgamma(df / 2) - 0.5 * math.log(df * math.pi)
            - math.log(scale) - (df + 1) / 2 * np.log1p(z * z / df))


def t37_distributions():
    g = rng(2)
    x = 0.01 * g.standard_t(5, 2000) / math.sqrt(5 / 3)
    n, mu, sd = len(x), x.mean(), x.std()
    ll_norm = -0.5 * n * (math.log(2 * math.pi * sd ** 2) + 1)
    best = None
    for df in [3, 4, 5, 6, 8, 10, 15, 30]:
        scale = sd * math.sqrt((df - 2) / df)          # moment-matched scale
        ll = float(t_logpdf(x, df, mu, scale).sum())
        if best is None or ll > best[1]:
            best = (df, ll)
    return {"loglik_normal": ll_norm, "aic_normal": 4 - 2 * ll_norm,
            "best_df": best[0], "loglik_t": best[1], "aic_t": 6 - 2 * best[1]}


# 38 ---------------------------------------------------------------------------
def t38_ttest():
    n, mean, sd = 250, 0.0005, 0.01
    t = mean / (sd / math.sqrt(n))
    p = 2 * (1 - ND.cdf(abs(t)))
    return {"t_stat": t, "p_two_sided": p, "annual_sharpe": mean / sd * math.sqrt(252)}


# 39 ---------------------------------------------------------------------------
def benjamini_hochberg(p, q=0.05):
    order = np.argsort(p)
    m = len(p)
    k = 0
    for rank, i in enumerate(order, start=1):
        if p[i] <= rank / m * q:
            k = rank
    return k


def t39_multiple_testing():
    p = np.array([0.001, 0.008, 0.012, 0.03, 0.04, 0.2, 0.35, 0.5, 0.7, 0.9])
    return {"naive_rejections_5pct": int((p < 0.05).sum()),
            "bonferroni_threshold": 0.05 / len(p),
            "bonferroni_rejections": int((p < 0.05 / len(p)).sum()),
            "bh_rejections": benjamini_hochberg(p)}


# 40 ---------------------------------------------------------------------------
def t40_deflated_sharpe():
    n = 756
    sr_ann = 1.5
    sr = sr_ann / math.sqrt(252)
    skew, kurt = -0.5, 5.0
    n_trials = 100
    var_trials = (0.5 ** 2) / 252            # SR dispersion across trials: 0.5 annual
    sr_star = expected_max_sr(var_trials, n_trials)
    return {"sr_daily": sr, "sr_star_daily": sr_star, "sr_star_annual": sr_star * math.sqrt(252),
            "psr_vs_zero": psr(sr, 0.0, n, skew, kurt), "deflated_sharpe": psr(sr, sr_star, n, skew, kurt)}


# 41 ---------------------------------------------------------------------------
def t41_bootstrap():
    g = rng(3)
    n, phi = 1000, 0.3
    e = g.normal(0.0004, 0.01, n)
    r = np.empty(n)
    r[0] = e[0]
    for t in range(1, n):
        r[t] = e[t] + phi * r[t - 1]
    out = {"sharpe_daily": sharpe(r)}
    for name, L in (("iid", 1), ("block20", 20)):
        stats = np.array([sharpe(r[block_indices(n, L, g)]) for _ in range(2000)])
        out[f"boot_se_{name}"] = float(stats.std())
    return out


# 42 ---------------------------------------------------------------------------
def t42_bayes():
    sigma, n, xbar = 0.01, 60, 0.001
    prior_mean, prior_sd = 0.0, 0.0005
    prec = n / sigma ** 2 + 1 / prior_sd ** 2
    post_mean = (n / sigma ** 2 * xbar + prior_mean / prior_sd ** 2) / prec
    return {"posterior_mean": post_mean, "posterior_sd": 1 / math.sqrt(prec),
            "weight_on_data": (n / sigma ** 2) / prec}


# 43 ---------------------------------------------------------------------------
def t43_mle():
    x = np.array([2, 4, 4, 4, 5, 5, 7, 9], dtype=float)
    return {"mean": float(x.mean()), "var_mle": float(x.var(ddof=0)), "var_unbiased": float(x.var(ddof=1))}


# 44 ---------------------------------------------------------------------------
def t44_sharpe_ci():
    n, sr_ann = 1260, 1.0
    sr = sr_ann / math.sqrt(252)
    se_iid = math.sqrt((1 + 0.5 * sr ** 2) / n)
    skew, kurt = -0.5, 5.0
    se_adj = math.sqrt((1 - skew * sr + (kurt - 1) / 4 * sr ** 2) / n)
    k = math.sqrt(252)
    return {"se_annual_iid": se_iid * k, "ci_iid": (sr_ann - 1.96 * se_iid * k, sr_ann + 1.96 * se_iid * k),
            "se_annual_adjusted": se_adj * k}


# 45 ---------------------------------------------------------------------------
def t45_autocorr():
    g = rng(4)
    n, phi = 500, 0.3
    e = g.normal(size=n)
    x = np.empty(n)
    x[0] = e[0]
    for t in range(1, n):
        x[t] = phi * x[t - 1] + e[t]
    rho = [acf(x, k) for k in range(1, 6)]
    q = n * (n + 2) * sum(r ** 2 / (n - k) for k, r in enumerate(rho, start=1))
    return {"rho_1_to_5": rho, "ljung_box_Q5": q, "chi2_5pct_crit_df5": 11.07}


# 46 ---------------------------------------------------------------------------
def t46_stationarity():
    g = rng(5)
    n, sims = 500, 400
    rej_rw = rej_ar = 0
    for _ in range(sims):
        e = g.normal(size=n)
        rw = np.cumsum(e)
        ar = np.empty(n)
        ar[0] = e[0]
        for t in range(1, n):
            ar[t] = 0.5 * ar[t - 1] + e[t]
        rej_rw += dickey_fuller_t(rw) < DF_CRIT_5
        rej_ar += dickey_fuller_t(ar) < DF_CRIT_5
    return {"reject_unit_root_random_walk": rej_rw / sims, "reject_unit_root_AR(0.5)": rej_ar / sims,
            "crit_5pct": DF_CRIT_5}


# 47 ---------------------------------------------------------------------------
def t47_cointegration():
    g = rng(6)
    n, sims = 500, 300
    coint_rej = spur_rej = 0
    spur_r2 = []
    spur_tbig = 0
    beta_hat = []
    for _ in range(sims):
        x = np.cumsum(g.normal(size=n))
        noise = np.empty(n)
        noise[0] = 0
        for t in range(1, n):
            noise[t] = 0.5 * noise[t - 1] + g.normal()
        y = 2 * x + noise
        X = np.column_stack([np.ones(n), x])
        b, resid = ols(X, y)
        beta_hat.append(b[1])
        coint_rej += dickey_fuller_t(resid) < EG_CRIT_5
        # spurious: independent random walks
        z = np.cumsum(g.normal(size=n))
        b2, se2, res2 = ols_se(X, z)
        spur_r2.append(1 - (res2 @ res2) / ((z - z.mean()) @ (z - z.mean())))
        spur_tbig += abs(b2[1] / se2[1]) > 2
        spur_rej += dickey_fuller_t(res2) < EG_CRIT_5
    return {"beta_hat_mean (true 2)": float(np.mean(beta_hat)),
            "EG_reject_when_cointegrated": coint_rej / sims,
            "naive_t_gt_2_independent_RWs": spur_tbig / sims,
            "mean_R2_independent_RWs": float(np.mean(spur_r2)),
            "EG_reject_independent_RWs": spur_rej / sims}


# 48 ---------------------------------------------------------------------------
def t48_regression():
    g = rng(8)
    n = 120
    z = g.normal(size=n)
    x1 = z + 0.05 * g.normal(size=n)
    x2 = z + 0.05 * g.normal(size=n)
    y = x1 + g.normal(scale=1.0, size=n)
    X = np.column_stack([x1, x2])
    out = {"corr_x1_x2": float(np.corrcoef(x1, x2)[0, 1])}
    for name, sl in (("first_half", slice(0, 60)), ("second_half", slice(60, 120))):
        b_ols, _ = ols(X[sl], y[sl])
        lam = 10.0
        b_ridge = np.linalg.solve(X[sl].T @ X[sl] + lam * np.eye(2), X[sl].T @ y[sl])
        out[f"ols_{name}"] = b_ols.round(3).tolist()
        out[f"ridge_{name}"] = b_ridge.round(3).tolist()
    return out


# 49 ---------------------------------------------------------------------------
def newey_west_se_mean(x: np.ndarray, L: int) -> float:
    n = len(x)
    d = x - x.mean()
    omega = d @ d / n
    for k in range(1, L + 1):
        omega += 2 * (1 - k / (L + 1)) * (d[k:] @ d[:-k] / n)
    return math.sqrt(omega / n)


def t49_newey_west():
    g = rng(9)
    n, phi = 2000, 0.5
    e = g.normal(size=n)
    x = np.empty(n)
    x[0] = e[0]
    for t in range(1, n):
        x[t] = phi * x[t - 1] + e[t]
    L = int(4 * (n / 100) ** (2 / 9))
    naive = x.std(ddof=1) / math.sqrt(n)
    nw = newey_west_se_mean(x, L)
    return {"lags": L, "se_naive": naive, "se_newey_west": nw, "ratio": nw / naive,
            "theory_ratio_sqrt((1+phi)/(1-phi))": math.sqrt((1 + phi) / (1 - phi))}


# 50 ---------------------------------------------------------------------------
def fit_ar(x: np.ndarray, p: int):
    y = x[p:]
    X = np.column_stack([np.ones(len(y))] + [x[p - k:-k] for k in range(1, p + 1)])
    b, resid = ols(X, y)
    return b, float(resid @ resid), len(y)


def t50_ar_selection():
    g = rng(10)
    n = 1500
    e = g.normal(size=n)
    x = np.zeros(n)
    for t in range(2, n):
        x[t] = 0.5 * x[t - 1] - 0.3 * x[t - 2] + e[t]
    train, test = x[:1000], x[1000:]
    aic = {}
    for p in range(1, 6):
        _, rss, m = fit_ar(train, p)
        aic[p] = m * math.log(rss / m) + 2 * (p + 1)
    best_p = min(aic, key=aic.get)
    b, _, _ = fit_ar(train, best_p)
    preds = np.array([b[0] + sum(b[k] * test[t - k] for k in range(1, best_p + 1)) for t in range(best_p, len(test))])
    actual = test[best_p:]
    return {"aic": {k: round(v, 1) for k, v in aic.items()}, "best_p": best_p, "coef": b.round(3).tolist(),
            "mse_model": float(np.mean((actual - preds) ** 2)), "mse_zero_forecast": float(np.mean(actual ** 2))}


# 51 ---------------------------------------------------------------------------
def t51_vol_models():
    lam, var_prev, r = 0.94, 0.0001, -0.02
    ewma_var = lam * var_prev + (1 - lam) * r ** 2
    omega, alpha, beta = 2e-6, 0.08, 0.90
    long_run = omega / (1 - alpha - beta)
    var1 = omega + alpha * r ** 2 + beta * var_prev
    fc = {h: long_run + (alpha + beta) ** (h - 1) * (var1 - long_run) for h in (1, 5, 10, 20)}
    return {"ewma_var": ewma_var, "ewma_vol_pct": 100 * math.sqrt(ewma_var),
            "garch_long_run_vol_pct": 100 * math.sqrt(long_run), "garch_var_next": var1,
            "garch_vol_forecast_pct": {h: round(100 * math.sqrt(v), 3) for h, v in fc.items()}}


# 52 ---------------------------------------------------------------------------
def hamilton_filter(r, mu, sig, P, pi0):
    K = len(mu)
    prob = np.zeros((len(r), K))
    p = np.array(pi0)
    for t, x in enumerate(r):
        pred = p if t == 0 else p @ P
        lik = np.array([norm_pdf(x, mu[k], sig[k]) for k in range(K)])
        post = pred * lik
        post /= post.sum()
        prob[t] = post
        p = post
    return prob


def t52_regimes():
    g = rng(11)
    mu, sig = [0.0005, -0.001], [0.007, 0.02]
    P = np.array([[0.98, 0.02], [0.05, 0.95]])
    n = 1000
    s = np.zeros(n, dtype=int)
    for t in range(1, n):
        s[t] = g.choice(2, p=P[s[t - 1]])
    r = np.array([g.normal(mu[k], sig[k]) for k in s])
    prob = hamilton_filter(r, mu, sig, P, [0.5, 0.5])
    return {"share_high_vol_days": float(s.mean()),
            "filtered_accuracy": float((prob.argmax(1) == s).mean()),
            "always_low_vol_accuracy": float((s == 0).mean())}


# 53 ---------------------------------------------------------------------------
def kalman_beta(y, x, Q, R, b0=0.0, P0=1.0):
    b, P = b0, P0
    out = np.empty(len(y))
    for t in range(len(y)):
        P += Q
        S = x[t] * P * x[t] + R
        K = P * x[t] / S
        b += K * (y[t] - x[t] * b)
        P = (1 - K * x[t]) * P
        out[t] = b
    return out


def t53_kalman():
    g = rng(12)
    n = 600
    beta = np.linspace(1.0, 1.5, n)
    x = g.normal(0, 0.01, n)
    y = beta * x + g.normal(0, 0.005, n)
    W = 60
    roll = np.full(n, np.nan)
    for t in range(W, n):
        xs, ys = x[t - W:t], y[t - W:t]
        roll[t] = xs @ ys / (xs @ xs)
    sl = slice(100, n)
    out = {"rmse_rolling_ols_60": float(np.sqrt(np.mean((roll[sl] - beta[sl]) ** 2)))}
    for Q in (1e-6, 1e-5, 1e-4, 1e-3):          # process-noise variance is the tuning knob
        kb = kalman_beta(y, x, Q=Q, R=0.005 ** 2)
        out[f"rmse_kalman_Q={Q:g}"] = float(np.sqrt(np.mean((kb[sl] - beta[sl]) ** 2)))
    return out


# 54 ---------------------------------------------------------------------------
def t54_evt():
    g = rng(13)
    nu = 4
    scale = 0.01 / math.sqrt(nu / (nu - 2))
    losses = -scale * g.standard_t(nu, 20000)                       # one sample of 20,000 days
    truth = -scale * rng(99).standard_t(nu, 4_000_000)             # large sample as "truth"
    u = float(np.quantile(losses, 0.95))
    exc = losses[losses > u] - u
    m, s2 = exc.mean(), exc.var(ddof=1)
    xi = 0.5 * (1 - m ** 2 / s2)
    beta = 0.5 * m * (m ** 2 / s2 + 1)
    p = 0.999
    var_gpd = u + beta / xi * ((len(losses) / len(exc) * (1 - p)) ** (-xi) - 1)
    var_norm = losses.mean() + losses.std() * ND.inv_cdf(p)
    return {"threshold_u": u, "xi_hat (true 0.25)": xi, "beta_hat": beta,
            "VaR99.9_gpd": float(var_gpd), "VaR99.9_normal": float(var_norm),
            "VaR99.9_empirical_sample": float(np.quantile(losses, p)),
            "VaR99.9_truth_large_sample": float(np.quantile(truth, p))}


# 55 ---------------------------------------------------------------------------
def t55_copulas():
    g = rng(14)
    n, rho, nu, q = 600_000, 0.5, 4, 0.01
    L = np.linalg.cholesky(np.array([[1, rho], [rho, 1]]))
    z = g.normal(size=(n, 2)) @ L.T
    w = g.chisquare(nu, n) / nu
    tt = z / np.sqrt(w)[:, None]
    out = {}
    for name, a in (("gaussian", z), ("student_t4", tt)):
        q1, q2 = np.quantile(a[:, 0], q), np.quantile(a[:, 1], q)
        out[f"joint_1pct_exceed_{name}"] = float(np.mean((a[:, 0] < q1) & (a[:, 1] < q2)))
    out["independent_would_be"] = q * q
    theta = 2.0
    out["clayton_theta2_lower_tail_dep"] = 2 ** (-1 / theta)
    return out


# 56 ---------------------------------------------------------------------------
def kaplan_meier(obs):
    """obs: list of (time, event) where event=1 observed, 0 censored."""
    times = sorted({t for t, e in obs if e == 1})
    s, curve = 1.0, []
    for t in times:
        at_risk = sum(1 for tt, _ in obs if tt >= t)
        d = sum(1 for tt, e in obs if tt == t and e == 1)
        s *= 1 - d / at_risk
        curve.append((t, at_risk, d, round(s, 4)))
    return curve


def t56_survival():
    obs = [(3, 1), (5, 1), (5, 0), (8, 1), (10, 0), (12, 1), (15, 1), (20, 0)]
    return {"km_steps (t, at_risk, events, S)": kaplan_meier(obs)}


ALL = [t36_descriptive, t37_distributions, t38_ttest, t39_multiple_testing, t40_deflated_sharpe,
       t41_bootstrap, t42_bayes, t43_mle, t44_sharpe_ci, t45_autocorr, t46_stationarity,
       t47_cointegration, t48_regression, t49_newey_west, t50_ar_selection, t51_vol_models,
       t52_regimes, t53_kalman, t54_evt, t55_copulas, t56_survival]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
