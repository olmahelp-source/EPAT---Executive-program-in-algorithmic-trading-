"""Section 2.3 worked examples (topics 66 to 78). Run: python3 ex_2_3_mathematics.py"""
from __future__ import annotations

import math

import numpy as np

from common import DF_CRIT_5, ND, bs_call, dickey_fuller_t, rng


# 66 ---------------------------------------------------------------------------
def t66_pca():
    C = np.array([[1.0, 0.8, 0.6], [0.8, 1.0, 0.7], [0.6, 0.7, 1.0]])
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    recon = vecs @ np.diag(vals) @ vecs.T
    return {"eigenvalues": vals.round(4).tolist(), "explained_variance_ratio": (vals / vals.sum()).round(4).tolist(),
            "first_pc_loadings": vecs[:, 0].round(4).tolist(), "reconstruction_max_error": float(np.abs(recon - C).max()),
            "condition_number": float(vals[0] / vals[-1])}


# 67 ---------------------------------------------------------------------------
def ledoit_wolf_identity(X: np.ndarray):
    """Shrink the sample covariance toward m*I (Ledoit and Wolf, 2004). X is T x N."""
    T, N = X.shape
    Xc = X - X.mean(0)
    S = Xc.T @ Xc / T
    m = np.trace(S) / N
    d2 = np.sum((S - m * np.eye(N)) ** 2) / N
    b2 = sum(np.sum((np.outer(x, x) - S) ** 2) for x in Xc) / (T ** 2) / N
    b2 = min(b2, d2)
    delta = b2 / d2
    return delta * m * np.eye(N) + (1 - delta) * S, delta


def min_var_weights(S: np.ndarray) -> np.ndarray:
    w = np.linalg.solve(S, np.ones(len(S)))
    return w / w.sum()


def t67_covariance_shrinkage():
    g = rng(31)
    N, T = 50, 60
    load = g.uniform(0.5, 1.5, N)
    true_cov = np.outer(load, load) * 0.0004 + np.diag(np.full(N, 0.0004))   # one factor + idiosyncratic
    Lc = np.linalg.cholesky(true_cov)
    res = {"sample_vs_shrunk_realized_vol_pct": []}
    vol_s, vol_l = [], []
    for _ in range(200):
        X = g.normal(size=(T, N)) @ Lc.T
        S = np.cov(X.T, bias=True)
        Sl, delta = ledoit_wolf_identity(X)
        for store, est in ((vol_s, S), (vol_l, Sl)):
            w = min_var_weights(est)
            store.append(math.sqrt(w @ true_cov @ w))
    S0 = np.cov((g.normal(size=(T, N)) @ Lc.T).T, bias=True)
    ev = np.linalg.eigvalsh(S0)
    q = N / T
    mp_upper = 1 * (1 + math.sqrt(q)) ** 2
    return {"N,T": (N, T), "cond_sample": float(ev[-1] / ev[0]),
            "cond_shrunk": float(np.linalg.cond(ledoit_wolf_identity(g.normal(size=(T, N)) @ Lc.T)[0])),
            "avg_realized_daily_vol_sample_minvar_pct": 100 * float(np.mean(vol_s)),
            "avg_realized_daily_vol_shrunk_minvar_pct": 100 * float(np.mean(vol_l)),
            "avg_shrinkage_intensity_last_run": float(delta),
            "true_min_variance_vol_pct (best possible)": 100 * math.sqrt(1 / (np.ones(N) @ np.linalg.solve(true_cov, np.ones(N)))),
            "marchenko_pastur_upper_edge (unit variance)": mp_upper}


# 68 ---------------------------------------------------------------------------
def t68_numerical_derivative():
    f, x, exact = math.exp, 1.0, math.e
    rows = {}
    for h in (1e-1, 1e-3, 1e-5, 1e-6, 1e-8, 1e-10, 1e-12):
        fwd = (f(x + h) - f(x)) / h
        cen = (f(x + h) - f(x - h)) / (2 * h)
        rows[f"h={h:g}"] = {"forward_err": abs(fwd - exact), "central_err": abs(cen - exact)}
    return {"exact_derivative": exact, "errors": rows, "rule_of_thumb_central_h": 2.2e-16 ** (1 / 3)}


# 69 ---------------------------------------------------------------------------
def long_only_min_var(S: np.ndarray):
    """Active-set method: drop assets with negative weight and re-solve."""
    active = list(range(len(S)))
    while True:
        sub = S[np.ix_(active, active)]
        w_sub = np.linalg.solve(sub, np.ones(len(active)))
        w_sub /= w_sub.sum()
        if (w_sub >= -1e-12).all():
            w = np.zeros(len(S))
            w[active] = w_sub
            return w
        active.pop(int(np.argmin(w_sub)))


def t69_optimization():
    vol = np.array([0.15, 0.30, 0.10])
    corr = np.array([[1, 0.95, 0.2], [0.95, 1, 0.1], [0.2, 0.1, 1]])
    S = np.outer(vol, vol) * corr
    w_free = min_var_weights(S)
    w_long = long_only_min_var(S)
    return {"unconstrained_weights": w_free.round(4).tolist(), "unconstrained_vol": math.sqrt(w_free @ S @ w_free),
            "long_only_weights": w_long.round(4).tolist(), "long_only_vol": math.sqrt(w_long @ S @ w_long)}


# 70 ---------------------------------------------------------------------------
def t70_ito():
    mu, sigma, T = 0.10, 0.30, 1.0
    g = rng(32)
    z = g.normal(size=1_000_000)
    ST = np.exp((mu - 0.5 * sigma ** 2) * T + sigma * math.sqrt(T) * z)
    return {"log_drift_theory (mu - sigma^2/2)": mu - 0.5 * sigma ** 2,
            "mean_log_return_sim": float(np.log(ST).mean()),
            "expected_gross_return_theory exp(mu*T)": math.exp(mu * T),
            "mean_gross_return_sim": float(ST.mean()),
            "median_gross_return_theory": math.exp((mu - 0.5 * sigma ** 2) * T),
            "median_gross_return_sim": float(np.median(ST))}


# 71 ---------------------------------------------------------------------------
def t71_sde_simulation():
    theta, mu, sigma, x0, T = 0.5, 0.0, 1.0, 2.0, 5.0
    g = rng(33)
    paths = 200_000
    exact_mean = mu + (x0 - mu) * math.exp(-theta * T)
    exact_var = sigma ** 2 / (2 * theta) * (1 - math.exp(-2 * theta * T))
    out = {"exact_mean": exact_mean, "exact_var": exact_var}
    for dt in (1.0, 0.1, 0.01):
        steps = int(T / dt)
        x = np.full(paths, x0)
        for _ in range(steps):
            x = x + theta * (mu - x) * dt + sigma * math.sqrt(dt) * g.normal(size=paths)
        out[f"euler_dt={dt}"] = {"mean": float(x.mean()), "var": float(x.var())}
    return out


# 72 ---------------------------------------------------------------------------
def t72_monte_carlo_option():
    S, K, T, r, sigma = 100.0, 105.0, 1.0, 0.05, 0.20
    bs = bs_call(S, K, T, r, sigma)
    g = rng(34)
    n = 100_000
    disc = math.exp(-r * T)

    def payoff(z):
        return disc * np.maximum(S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * math.sqrt(T) * z) - K, 0)

    z = g.normal(size=n)
    plain = payoff(z)
    anti = 0.5 * (payoff(z) + payoff(-z))
    return {"black_scholes": bs, "mc_plain": float(plain.mean()), "mc_plain_se": float(plain.std(ddof=1) / math.sqrt(n)),
            "mc_antithetic": float(anti.mean()), "mc_antithetic_se": float(anti.std(ddof=1) / math.sqrt(n))}


# 73 ---------------------------------------------------------------------------
def mutual_information(a: np.ndarray, b: np.ndarray) -> float:
    ua, ia = np.unique(a, return_inverse=True)
    ub, ib = np.unique(b, return_inverse=True)
    joint = np.zeros((len(ua), len(ub)))
    np.add.at(joint, (ia, ib), 1)
    joint /= joint.sum()
    pa, pb = joint.sum(1, keepdims=True), joint.sum(0, keepdims=True)
    nz = joint > 0
    return float((joint[nz] * np.log(joint[nz] / (pa @ pb)[nz])).sum())


def t73_mutual_information():
    g = rng(35)
    n = 5000
    x = g.normal(size=n)
    p_up = 0.5 + 0.05 * np.tanh(x)                       # weak, nonlinear link
    y = (g.random(n) < p_up).astype(int)
    bins = np.digitize(x, np.quantile(x, [0.2, 0.4, 0.6, 0.8]))
    mi = mutual_information(bins, y)
    perm = np.array([mutual_information(bins, g.permutation(y)) for _ in range(500)])
    h_y = -sum(p * math.log(p) for p in (y.mean(), 1 - y.mean()))
    return {"entropy_of_y_nats": h_y, "mutual_information": mi,
            "permutation_95th_pct": float(np.quantile(perm, 0.95)), "permutation_p_value": float((perm >= mi).mean())}


# 74 ---------------------------------------------------------------------------
def periodogram(x: np.ndarray) -> np.ndarray:
    x = x - x.mean()
    return np.abs(np.fft.rfft(x)) ** 2 / len(x)


def t74_fourier():
    g = rng(36)
    n, period = 512, 20
    t = np.arange(n)
    x = np.sin(2 * math.pi * t / period) + g.normal(0, 2.0, n)
    pg = periodogram(x)
    k = int(np.argmax(pg[1:])) + 1
    noise_max = [periodogram(g.normal(0, 2.0, n))[1:].max() for _ in range(300)]
    return {"peak_frequency_index": k, "estimated_period": n / k, "true_period": period,
            "peak_power": float(pg[k]), "noise_only_max_power_95th_pct": float(np.quantile(noise_max, 0.95))}


# 75 ---------------------------------------------------------------------------
def mixed_nash_2x2(A, B):
    """A: row player's payoffs, B: column player's. Returns (p_row1, q_col1) for the interior equilibrium."""
    (a, b), (c, d) = A
    (e, f), (gg, h) = B
    q = (d - b) / (a - b - c + d)          # column mix that makes the row player indifferent
    p = (h - gg) / (e - gg - f + h)        # row mix that makes the column player indifferent
    return p, q


def t75_game_theory():
    # Row = market maker (Tight, Wide). Column = informed trader (Trade, Skip).
    A = [[-3, 2], [1, 0]]
    B = [[3, 0], [-1, 0]]
    p, q = mixed_nash_2x2(A, B)
    return {"P(MM quotes Tight)": p, "P(informed Trades)": q,
            "MM_payoff_if_Tight": -3 * q + 2 * (1 - q), "MM_payoff_if_Wide": 1 * q + 0 * (1 - q),
            "Informed_payoff_if_Trade": 3 * p - 1 * (1 - p), "Informed_payoff_if_Skip": 0.0}


# 76 ---------------------------------------------------------------------------
def optimal_liquidation(Q: int, T: int, lam: float):
    """Minimize sum_t [q_t^2 + lam*(x_t - q_t)^2] with all shares sold by the last period."""
    V = [[0.0] * (Q + 1) for _ in range(T + 1)]
    pol = [[0] * (Q + 1) for _ in range(T)]
    for x in range(Q + 1):
        V[T - 1][x] = float(x * x)
        pol[T - 1][x] = x
    for t in range(T - 2, -1, -1):
        for x in range(Q + 1):
            best, arg = float("inf"), 0
            for q in range(x + 1):
                c = q * q + lam * (x - q) ** 2 + V[t + 1][x - q]
                if c < best:
                    best, arg = c, q
            V[t][x], pol[t][x] = best, arg
    x, plan = Q, []
    for t in range(T):
        q = pol[t][x]
        plan.append(q)
        x -= q
    return plan, V[0][Q]


def t76_dynamic_programming():
    out = {}
    for lam in (0.0, 0.5, 2.0):
        plan, cost = optimal_liquidation(10, 5, lam)
        out[f"lambda={lam}"] = {"schedule": plan, "total_cost": cost}
    return out


# 77 ---------------------------------------------------------------------------
def minimum_spanning_tree(D: np.ndarray):
    n = len(D)
    edges = sorted((D[i, j], i, j) for i in range(n) for j in range(i + 1, n))
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    tree = []
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            tree.append((i, j, round(w, 4)))
    return tree


def t77_graph_mst():
    names = ["A", "B", "C", "D", "E"]
    C = np.array([[1.0, 0.8, 0.7, 0.2, 0.1],
                  [0.8, 1.0, 0.6, 0.3, 0.2],
                  [0.7, 0.6, 1.0, 0.1, 0.0],
                  [0.2, 0.3, 0.1, 1.0, 0.75],
                  [0.1, 0.2, 0.0, 0.75, 1.0]])
    D = np.sqrt(0.5 * (1 - C))
    tree = minimum_spanning_tree(D)
    return {"d(rho=1)": 0.0, "d(rho=0)": math.sqrt(0.5), "d(rho=-1)": 1.0,
            "mst_edges": [(names[i], names[j], float(w)) for i, j, w in tree]}


# 78 ---------------------------------------------------------------------------
def ffd_weights(d: float, thresh: float = 1e-3, max_k: int = 2000):
    w = [1.0]
    for k in range(1, max_k):
        w_k = -w[-1] * (d - k + 1) / k
        if abs(w_k) < thresh:
            break
        w.append(w_k)
    return np.array(w)


def frac_diff(x: np.ndarray, d: float, thresh: float = 1e-3) -> np.ndarray:
    w = ffd_weights(d, thresh)
    width = len(w)
    return np.array([w @ x[t - width + 1:t + 1][::-1] for t in range(width - 1, len(x))])


def t78_fractional_differentiation():
    g = rng(37)
    n = 4000
    logp = np.cumsum(0.0003 + 0.01 * g.normal(size=n))     # log price: random walk with drift
    rows = {}
    for d in (0.0, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 1.0):
        s = frac_diff(logp, d)
        rows[f"d={d}"] = {"ADF_t": round(dickey_fuller_t(s), 2),
                          "passes_5pct": bool(dickey_fuller_t(s) < DF_CRIT_5),
                          "corr_with_original": round(float(np.corrcoef(s, logp[-len(s):])[0, 1]), 3)}
    return {"weights_d=0.4 (first 5)": ffd_weights(0.4)[:5].round(4).tolist(), "results": rows}


ALL = [t66_pca, t67_covariance_shrinkage, t68_numerical_derivative, t69_optimization, t70_ito,
       t71_sde_simulation, t72_monte_carlo_option, t73_mutual_information, t74_fourier,
       t75_game_theory, t76_dynamic_programming, t77_graph_mst, t78_fractional_differentiation]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
