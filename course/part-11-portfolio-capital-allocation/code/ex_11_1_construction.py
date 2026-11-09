"""Section 11.1 worked examples (topics 462 to 475). Run: python3 ex_11_1_construction.py"""
from __future__ import annotations

import math

import numpy as np

from common import (ND, cov_from, min_var_long_only, min_var_unconstrained, mv_long_only,
                    port_vol, project_capped_simplex, rng, risk_contrib)


# 462 ---------------------------------------------------------------------------
def mv_weights_budget(mu, S, lam):
    """max mu'w - lam/2 w'Sw  s.t. sum w = 1 (shorts allowed)."""
    Si = np.linalg.inv(S)
    one = np.ones(len(mu))
    gamma = (one @ Si @ mu / lam - 1) / (one @ Si @ one) * lam
    return Si @ (mu - gamma) / lam


def t462_mean_variance():
    vol = [0.15, 0.18, 0.22, 0.12]
    corr = np.array([[1, .5, .4, .3], [.5, 1, .8, .3], [.4, .8, 1, .2], [.3, .3, .2, 1]])
    S = cov_from(vol, corr)
    mu = np.array([0.06, 0.07, 0.08, 0.05])
    lam = 4.0
    w0 = mv_weights_budget(mu, S, lam)
    g = rng(1)
    changes, changes_mv = [], []
    wmv0 = min_var_unconstrained(S)
    for _ in range(300):
        mu2 = mu + g.normal(0, 0.005, 4)          # +/- 0.5% noise in expected returns
        changes.append(np.abs(mv_weights_budget(mu2, S, lam) - w0).sum())
    return {"weights_mean_variance": w0.round(3).tolist(), "weights_min_variance": wmv0.round(3).tolist(),
            "avg_L1_weight_change_for_0.5pct_mu_noise": float(np.mean(changes)),
            "sum_abs_weights (leverage)": float(np.abs(w0).sum())}


# 463 ---------------------------------------------------------------------------
def t463_black_litterman():
    S = cov_from([0.20, 0.25, 0.15], [[1, .6, .3], [.6, 1, .4], [.3, .4, 1]])
    w_mkt = np.array([0.5, 0.3, 0.2])
    delta, tau = 2.5, 0.05
    pi = delta * S @ w_mkt                                      # equilibrium (implied) returns
    P = np.array([[1.0, -1.0, 0.0]])                            # view: A outperforms B ...
    q = np.array([0.02])                                        # ... by 2%
    Omega = P @ (tau * S) @ P.T                                 # confidence equal to the prior's
    A = np.linalg.inv(tau * S) + P.T @ np.linalg.inv(Omega) @ P
    mu_bl = np.linalg.solve(A, np.linalg.inv(tau * S) @ pi + P.T @ np.linalg.inv(Omega) @ q)
    w_bl = np.linalg.solve(delta * S, mu_bl)
    return {"implied_returns_pct": (100 * pi).round(2).tolist(), "posterior_returns_pct": (100 * mu_bl).round(2).tolist(),
            "view_spread_prior_pct": float(100 * (pi[0] - pi[1])), "view_spread_posterior_pct": float(100 * (mu_bl[0] - mu_bl[1])),
            "market_weights": w_mkt.tolist(), "bl_weights": w_bl.round(3).tolist()}


# 464 ---------------------------------------------------------------------------
def erc_weights(S, iters: int = 2000):
    n = len(S)
    w = np.full(n, 1.0 / n)
    for _ in range(iters):
        rc = w * (S @ w)
        w = w * np.sqrt(rc.mean() / rc)
        w /= w.sum()
    return w


def t464_risk_parity():
    vol = np.array([0.10, 0.20, 0.30])
    S0 = cov_from(vol, np.eye(3))
    w0 = erc_weights(S0)
    S1 = cov_from(vol, [[1, .5, .2], [.5, 1, .4], [.2, .4, 1]])
    w1 = erc_weights(S1)
    return {"uncorrelated_weights": w0.round(4).tolist(), "inverse_vol_weights": ((1 / vol) / (1 / vol).sum()).round(4).tolist(),
            "correlated_weights": w1.round(4).tolist(),
            "correlated_risk_contributions_pct": (100 * risk_contrib(w1, S1) / port_vol(w1, S1)).round(2).tolist(),
            "equal_weight_risk_contributions_pct": (100 * risk_contrib(np.full(3, 1 / 3), S1) / port_vol(np.full(3, 1 / 3), S1)).round(2).tolist()}


# 465 ---------------------------------------------------------------------------
def single_linkage_order(D):
    clusters = [[i] for i in range(len(D))]
    while len(clusters) > 1:
        best = None
        for a in range(len(clusters)):
            for b in range(a + 1, len(clusters)):
                d = min(D[i, j] for i in clusters[a] for j in clusters[b])
                if best is None or d < best[0]:
                    best = (d, a, b)
        _, a, b = best
        merged = clusters[a] + clusters[b]
        clusters = [c for k, c in enumerate(clusters) if k not in (a, b)] + [merged]
    return clusters[0]


def cluster_var(S, items):
    sub = S[np.ix_(items, items)]
    iv = 1 / np.diag(sub)
    iv /= iv.sum()
    return float(iv @ sub @ iv)


def hrp_weights(S):
    sd = np.sqrt(np.diag(S))
    corr = S / np.outer(sd, sd)
    D = np.sqrt(0.5 * (1 - corr))
    order = single_linkage_order(D)
    w = np.ones(len(S))
    stack = [order]
    while stack:
        items = stack.pop()
        if len(items) <= 1:
            continue
        mid = len(items) // 2
        left, right = items[:mid], items[mid:]
        vl, vr = cluster_var(S, left), cluster_var(S, right)
        alpha = 1 - vl / (vl + vr)
        w[left] *= alpha
        w[right] *= 1 - alpha
        stack += [left, right]
    return order, w / w.sum()


def t465_hrp():
    vol = [0.10, 0.12, 0.11, 0.20, 0.22, 0.25]
    corr = np.full((6, 6), 0.2)
    corr[:3, :3] = 0.7
    corr[3:, 3:] = 0.7
    np.fill_diagonal(corr, 1.0)
    S = cov_from(vol, corr)
    order, w = hrp_weights(S)
    iv = 1 / np.diag(S)
    iv /= iv.sum()
    wmv = min_var_unconstrained(S)
    return {"leaf_order": order, "hrp_weights": w.round(3).tolist(), "inverse_variance_weights": iv.round(3).tolist(),
            "min_variance_unconstrained": wmv.round(3).tolist(), "hrp_vol_pct": 100 * port_vol(w, S),
            "invvar_vol_pct": 100 * port_vol(iv, S), "minvar_vol_pct": 100 * port_vol(wmv, S)}


# 466 ---------------------------------------------------------------------------
def t466_minvar_maxdiv():
    vol = np.array([0.20, 0.25, 0.15, 0.30])
    corr = np.array([[1, .4, .3, .5], [.4, 1, .3, .4], [.3, .3, 1, .2], [.5, .4, .2, 1]])
    S = cov_from(vol, corr)

    def dr(w):
        return float(w @ vol / port_vol(w, S))

    ew = np.full(4, 0.25)
    mv = min_var_unconstrained(S)
    md = np.linalg.solve(S, vol)
    md /= md.sum()                                    # maximum diversification = tangency with mu = sigma
    erc = erc_weights_local(S)
    out = {}
    for name, w in (("equal", ew), ("min_variance", mv), ("max_diversification", md), ("risk_parity", erc)):
        out[name] = {"weights": w.round(3).tolist(), "vol_pct": round(100 * port_vol(w, S), 2), "diversification_ratio": round(dr(w), 3)}
    return out


def erc_weights_local(S, iters=2000):
    n = len(S)
    w = np.full(n, 1.0 / n)
    for _ in range(iters):
        rc = w * (S @ w)
        w = w * np.sqrt(rc.mean() / rc)
        w /= w.sum()
    return w


# 467 ---------------------------------------------------------------------------
def cvar(losses: np.ndarray, alpha: float = 0.95) -> float:
    k = max(1, int(math.ceil((1 - alpha) * len(losses))))
    return float(np.sort(losses)[-k:].mean())


def min_cvar_long_only(R: np.ndarray, alpha: float = 0.95, iters: int = 4000):
    T, n = R.shape
    k = max(1, int(math.ceil((1 - alpha) * T)))
    w = np.full(n, 1.0 / n)
    best, best_val = w.copy(), cvar(-R @ w, alpha)
    for it in range(1, iters + 1):
        losses = -R @ w
        tail = np.argsort(losses)[-k:]
        grad = -R[tail].mean(0)
        w = project_capped_simplex(w - 0.02 / math.sqrt(it) * grad / (np.linalg.norm(grad) + 1e-12), 1.0)
        val = cvar(-R @ w, alpha)
        if val < best_val:
            best, best_val = w.copy(), val
    return best


def t467_cvar():
    g = rng(5)
    T = 5000
    a1 = g.normal(0.0004, 0.010, T)                                     # plain asset, 1.0% vol
    jump = np.where(g.random(T) < 0.01, -0.06, 0.0)                     # 1% chance of a -6% crash
    a2 = g.normal(0.0004, 0.003, T) + jump                              # "calm" asset: lowest variance, ugly tail
    a3 = g.normal(0.0004, 0.012, T)
    R = np.column_stack([a1, a2, a3])
    S = np.cov(R.T)
    w_var = min_var_long_only(S)
    w_cvar = min_cvar_long_only(R, alpha=0.99)
    out = {"asset_vols_pct": (100 * R.std(0)).round(3).tolist()}
    for name, w in (("min_variance", w_var), ("min_cvar99", w_cvar)):
        out[name] = {"weights": w.round(3).tolist(), "vol_pct": round(100 * float(np.std(R @ w)), 3),
                     "cvar95_pct": round(100 * cvar(-R @ w), 3), "cvar99_pct": round(100 * cvar(-R @ w, 0.99), 3)}
    return out


# 468 ---------------------------------------------------------------------------
def t468_resampled():
    g = rng(6)
    mu_true = np.array([0.05, 0.06, 0.07, 0.065])
    S_true = cov_from([0.15, 0.18, 0.20, 0.19], [[1, .5, .4, .4], [.5, 1, .7, .7], [.4, .7, 1, .8], [.4, .7, .8, 1]])
    lam, T = 4.0, 60
    L = np.linalg.cholesky(S_true / 252)
    plain, resamp = [], []
    for _ in range(15):
        X = mu_true / 252 + g.normal(size=(T, 4)) @ L.T
        mu_h, S_h = X.mean(0) * 252, np.cov(X.T) * 252
        plain.append(mv_long_only(mu_h, S_h, lam, iters=600))
        Lh = np.linalg.cholesky(S_h / 252)
        ws = []
        for _ in range(25):
            Xs = mu_h / 252 + g.normal(size=(T, 4)) @ Lh.T
            ws.append(mv_long_only(Xs.mean(0) * 252, np.cov(Xs.T) * 252, lam, iters=300))
        resamp.append(np.mean(ws, axis=0))
    plain, resamp = np.array(plain), np.array(resamp)

    def util(w):
        return float(mu_true @ w - lam / 2 * w @ S_true @ w)

    return {"avg_weight_std_across_samples_plain": float(plain.std(0).mean()),
            "avg_weight_std_across_samples_resampled": float(resamp.std(0).mean()),
            "avg_true_utility_plain": float(np.mean([util(w) for w in plain])),
            "avg_true_utility_resampled": float(np.mean([util(w) for w in resamp])),
            "true_optimal_utility": util(mv_long_only(mu_true, S_true, lam))}


# 469 ---------------------------------------------------------------------------
def t469_factor_construction():
    beta = np.array([0.8, 1.0, 1.2, 0.6, 1.4])
    w = np.array([0.35, 0.25, 0.20, 0.10, 0.10])      # raw long-only tilts from a signal
    A = np.vstack([np.ones(5), beta])                 # constraints: dollar neutral, beta neutral
    w_neutral = w - A.T @ np.linalg.solve(A @ A.T, A @ w)
    g = rng(7)
    n = 250
    m = g.normal(0.0004, 0.01, n)
    est = []
    for b in beta:
        y = b * m + g.normal(0, 0.012, n)
        X = np.column_stack([np.ones(n), m])
        coef = np.linalg.solve(X.T @ X, X.T @ y)
        res = y - X @ coef
        se = math.sqrt(res @ res / (n - 2) * np.linalg.inv(X.T @ X)[1, 1])
        est.append((round(float(coef[1]), 3), round(se, 3)))
    return {"start_weights": w.tolist(), "start_beta_exposure": float(beta @ w),
            "neutral_weights": w_neutral.round(4).tolist(), "neutral_dollar": float(w_neutral.sum()),
            "neutral_beta": float(beta @ w_neutral), "estimated_betas (value, std error)": est, "true_betas": beta.tolist()}


# 470 ---------------------------------------------------------------------------
def t470_constraints():
    S = cov_from([0.10, 0.15, 0.20, 0.12, 0.25], np.eye(5) * 0.6 + 0.4)
    free = min_var_long_only(S)
    capped = min_var_long_only(S, cap=0.30)
    try:
        min_var_long_only(S, cap=0.15)
        infeasible = "not detected"
    except ValueError as e:
        infeasible = str(e)
    return {"long_only_weights": free.round(3).tolist(), "long_only_vol_pct": 100 * port_vol(free, S),
            "cap30_weights": capped.round(3).tolist(), "cap30_vol_pct": 100 * port_vol(capped, S),
            "binding_caps": int((capped > 0.2999).sum()), "cap15_with_5_assets": infeasible}


# 471 ---------------------------------------------------------------------------
def trade_to_band(w_target, w0, c, lam, sigma):
    band = c / (lam * sigma ** 2)
    if w_target > w0 + band:
        return w_target - band
    if w_target < w0 - band:
        return w_target + band
    return w0


def t471_tcost_aware():
    mu, sigma, lam, c = 0.06, 0.20, 3.0, 0.001
    wt = mu / (lam * sigma ** 2)
    band = c / (lam * sigma ** 2)
    out = {"target_weight": wt, "no_trade_half_width": band}
    grid = np.linspace(0, 1, 100001)
    for w0 in (0.30, 0.495, 0.505, 0.60):
        w = trade_to_band(wt, w0, c, lam, sigma)
        u = mu * grid - lam / 2 * sigma ** 2 * grid ** 2 - c * np.abs(grid - w0)
        out[f"w0={w0}"] = {"closed_form": round(w, 4), "grid_search": round(float(grid[u.argmax()]), 4)}
    return out


# 472 ---------------------------------------------------------------------------
def t472_multiperiod():
    sigma, lam, k = 0.20, 3.0, 0.05                  # k: quadratic trading-cost coefficient
    mu1, mu2 = 0.08, 0.02
    grid = np.linspace(0, 1, 101)

    def u(mu, w):
        return mu * w - lam / 2 * sigma ** 2 * w ** 2

    w0 = 0.0
    # period 2 value function of the position carried in
    def cost(a, b):
        return k * (a - b) ** 2

    V2 = np.array([max(u(mu2, w2) - cost(w2, w1) for w2 in grid) for w1 in grid])
    myo1 = grid[np.argmax([u(mu1, w) - cost(w, w0) for w in grid])]
    dyn1 = grid[np.argmax([u(mu1, w) - cost(w, w0) + V2[i] for i, w in enumerate(grid)])]

    def total(w1):
        w2 = grid[np.argmax([u(mu2, w) - cost(w, w1) for w in grid])]
        return u(mu1, w1) - cost(w1, w0) + u(mu2, w2) - cost(w2, w1), w2

    t_m, w2_m = total(myo1)
    t_d, w2_d = total(dyn1)
    return {"target_period1": mu1 / (lam * sigma ** 2), "target_period2": mu2 / (lam * sigma ** 2),
            "myopic_w1": float(myo1), "myopic_w2": float(w2_m), "myopic_total_utility": float(t_m),
            "dynamic_w1": float(dyn1), "dynamic_w2": float(w2_d), "dynamic_total_utility": float(t_d)}


# 473 ---------------------------------------------------------------------------
def t473_strategy_allocation():
    vol = np.array([0.10, 0.15, 0.08])
    sharpe = np.array([1.0, 0.6, 0.8])
    corr_bt = np.array([[1, .2, .1], [.2, 1, .3], [.1, .3, 1]])
    corr_stress = np.full((3, 3), 0.7)
    np.fill_diagonal(corr_stress, 1.0)
    S_bt, S_st = cov_from(vol, corr_bt), cov_from(vol, corr_stress)
    w_erc = erc_weights_local(S_bt)
    w_eq = np.full(3, 1 / 3)
    w_sh = sharpe / sharpe.sum()
    out = {}
    for name, w in (("equal_capital", w_eq), ("sharpe_weighted", w_sh), ("risk_parity", w_erc)):
        out[name] = {"weights": w.round(3).tolist(), "vol_backtest_corr_pct": round(100 * port_vol(w, S_bt), 2),
                     "vol_stress_corr_pct": round(100 * port_vol(w, S_st), 2)}
    return out


# 474 ---------------------------------------------------------------------------
def t474_regime_allocation():
    S_calm = cov_from([0.15, 0.05], [[1, -0.2], [-0.2, 1]])
    S_stress = cov_from([0.30, 0.08], [[1, 0.3], [0.3, 1]])
    mu_calm, mu_stress = np.array([0.08, 0.03]), np.array([-0.05, 0.02])
    w_calm = mv_long_only(mu_calm, S_calm, 4.0)
    w_stress = mv_long_only(mu_stress, S_stress, 4.0)
    g = rng(8)
    n = 500
    p = np.empty(n)
    p[0] = 0.5
    for t in range(1, n):
        p[t] = min(1, max(0, 0.97 * p[t - 1] + 0.03 * 0.5 + g.normal(0, 0.06)))
    blended = np.array([(1 - x) * w_calm + x * w_stress for x in p])
    turn_blend = np.abs(np.diff(blended, axis=0)).sum(1).sum() / 2
    state, switches = 0, 0
    path = []
    for x in p:
        if state == 0 and x > 0.7:
            state, switches = 1, switches + 1
        elif state == 1 and x < 0.3:
            state, switches = 0, switches + 1
        path.append(w_stress if state else w_calm)
    turn_hyst = np.abs(np.diff(np.array(path), axis=0)).sum() / 2
    naive_switch = int(((p[1:] > 0.5) != (p[:-1] > 0.5)).sum())
    return {"calm_weights": w_calm.round(3).tolist(), "stress_weights": w_stress.round(3).tolist(),
            "blend_by_probability_turnover_total": float(turn_blend), "hard_switch_at_50pct_flips": naive_switch,
            "hysteresis_(70/30)_flips": switches, "hysteresis_turnover_total": float(turn_hyst)}


# 475 ---------------------------------------------------------------------------
def t475_rebalancing():
    g = rng(9)
    sims, days, years = 200, 252 * 20, 20
    mu = np.array([0.07, 0.03]) / 252
    vol = np.array([0.16, 0.05]) / math.sqrt(252)
    C = np.linalg.cholesky(np.array([[1, 0.1], [0.1, 1]]))
    target = np.array([0.6, 0.4])
    cost = 0.0010                                        # 10 bps of traded notional
    policies = {"never": None, "monthly": 21, "quarterly": 63, "band_5pct": "b5", "band_2pct": "b2"}
    res = {k: {"turn": np.zeros(sims), "drift": np.zeros(sims), "wealth": np.ones(sims)} for k in policies}
    Z = g.normal(size=(days, sims, 2)) @ C.T
    rets = np.exp(mu - 0.5 * vol ** 2 + vol * Z)         # gross return per day, shape (days, sims, 2)
    for name, pol in policies.items():
        w = np.tile(target, (sims, 1))
        wealth = np.ones(sims)
        turnover = np.zeros(sims)
        drift2 = np.zeros(sims)
        for d in range(days):
            growth = (w * rets[d]).sum(1)
            w = w * rets[d] / growth[:, None]
            wealth *= growth
            drift2 += (w[:, 0] - target[0]) ** 2
            if pol is None:
                continue
            if isinstance(pol, int):
                do = np.full(sims, (d + 1) % pol == 0)
            else:
                thr = 0.05 if pol == "b5" else 0.02
                do = np.abs(w[:, 0] - target[0]) > thr
            t = np.abs(w - target).sum(1) / 2 * do
            wealth *= 1 - cost * 2 * t                   # traded notional = 2 x one-way turnover
            turnover += t
            w = np.where(do[:, None], target, w)
        res[name] = {"turnover_per_year_pct": 100 * float(turnover.mean() / years),
                     "rms_weight_drift_pct": 100 * float(np.sqrt(drift2.mean() / days)),
                     "avg_final_wealth": float(wealth.mean()), "median_final_wealth": float(np.median(wealth))}
    return res


ALL = [t462_mean_variance, t463_black_litterman, t464_risk_parity, t465_hrp, t466_minvar_maxdiv,
       t467_cvar, t468_resampled, t469_factor_construction, t470_constraints, t471_tcost_aware,
       t472_multiperiod, t473_strategy_allocation, t474_regime_allocation, t475_rebalancing]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
