"""Sections 11.2 and 11.3 worked examples (topics 476 to 484). Run: python3 ex_11_2_book_and_risk_models.py"""
from __future__ import annotations

import math

import numpy as np

from common import ND, cov_from, port_vol, rng


# 476 ---------------------------------------------------------------------------
class Ledger:
    """Average-cost position ledger with realized P&L, including position flips."""

    def __init__(self):
        self.pos: dict[str, float] = {}
        self.avg: dict[str, float] = {}
        self.realized = 0.0
        self.fees = 0.0

    def fill(self, sym: str, qty: float, price: float, fee: float = 0.0) -> float:
        p, a = self.pos.get(sym, 0.0), self.avg.get(sym, 0.0)
        self.fees += fee
        pnl = 0.0
        if p == 0 or (p > 0) == (qty > 0):                 # opening or adding
            new = p + qty
            a = (a * abs(p) + price * abs(qty)) / abs(new)
            p = new
        else:                                              # reducing, closing, or flipping
            closed = min(abs(qty), abs(p))
            pnl = closed * (price - a) * (1 if p > 0 else -1)
            new = p + qty
            if new == 0:
                a = 0.0
            elif (new > 0) != (p > 0):
                a = price                                  # the remainder is a new position at this price
            p = new
        self.pos[sym], self.avg[sym] = p, a
        self.realized += pnl
        return pnl

    def unrealized(self, marks: dict[str, float]) -> float:
        return sum(q * (marks[s] - self.avg[s]) for s, q in self.pos.items() if q != 0)


def t476_ledger():
    L = Ledger()
    steps = []
    for q, px in ((100, 50), (50, 56), (-120, 60), (-100, 58), (40, 55)):
        pnl = L.fill("XYZ", q, px)
        steps.append((q, px, round(pnl, 2), L.pos["XYZ"], round(L.avg["XYZ"], 4)))
    return {"steps (qty, price, realized_pnl, position, avg_cost)": steps, "total_realized": L.realized,
            "unrealized_at_54": L.unrealized({"XYZ": 54.0})}


# 477 ---------------------------------------------------------------------------
def reconcile(local: dict, broker: dict, qty_tol: float = 0.0):
    breaks = []
    for s in sorted(set(local) | set(broker)):
        a, b = local.get(s, 0.0), broker.get(s, 0.0)
        if s not in broker and a != 0:
            breaks.append((s, "missing_at_broker", a, b))
        elif s not in local and b != 0:
            breaks.append((s, "unknown_locally", a, b))
        elif abs(a - b) > qty_tol:
            breaks.append((s, "quantity_mismatch", a, b))
    return breaks


def t477_reconciliation():
    local = {"AAA": 100, "BBB": -50, "CCC": 200, "DDD": 0}
    broker = {"AAA": 100, "BBB": -40, "EEE": 75, "CCC": 200}
    return {"breaks (symbol, type, local, broker)": reconcile(local, broker)}


# 478 ---------------------------------------------------------------------------
def t478_risk_model():
    B = np.array([[1.0, 0.2], [0.9, -0.1], [1.2, 0.5], [0.7, 0.0]])          # market, value loadings
    F = cov_from([0.16, 0.08], [[1, -0.2], [-0.2, 1]])
    spec = np.array([0.10, 0.12, 0.15, 0.08])
    S = B @ F @ B.T + np.diag(spec ** 2)
    w = np.array([0.3, 0.3, 0.2, 0.2])
    expo = B.T @ w
    sys_var = float(expo @ F @ expo)
    spec_var = float((w ** 2 * spec ** 2).sum())
    total = float(w @ S @ w)
    return {"factor_exposures (market, value)": expo.round(3).tolist(), "systematic_variance": sys_var,
            "specific_variance": spec_var, "total_variance": total, "check_sum": sys_var + spec_var,
            "systematic_share_pct": 100 * sys_var / total, "portfolio_vol_pct": 100 * math.sqrt(total),
            "min_eigenvalue_of_S (must be > 0)": float(np.linalg.eigvalsh(S).min())}


# 479 ---------------------------------------------------------------------------
def t479_factor_zoo():
    g = rng(41)
    m, n = 300, 240                                        # 300 candidate factors, 20 years of monthly data
    r = g.normal(0, 0.03, (m, n))                          # every factor is pure noise
    t = r.mean(1) / (r.std(1, ddof=1) / math.sqrt(n))
    z_bonf = ND.inv_cdf(1 - 0.05 / (2 * m))
    return {"factors_with_|t|>2": int((np.abs(t) > 2).sum()), "expected_by_chance_|t|>2": m * 2 * (1 - ND.cdf(2)),
            "factors_with_|t|>3": int((np.abs(t) > 3).sum()), "expected_by_chance_|t|>3": m * 2 * (1 - ND.cdf(3)),
            "best_t_stat": float(np.abs(t).max()), "bonferroni_threshold_t": z_bonf}


# 480 ---------------------------------------------------------------------------
def t480_hedging():
    g = rng(42)
    n, rho, s_s, s_f = 20000, 0.9, 0.012, 0.010
    zf, e = g.normal(size=n), g.normal(size=n)
    rf = s_f * zf
    rs = s_s * (rho * zf + math.sqrt(1 - rho ** 2) * e)
    h = np.cov(rs, rf)[0, 1] / rf.var(ddof=1)

    def eff(hh):
        return 1 - (rs - hh * rf).var() / rs.var()

    window = [np.cov(rs[i:i + 60], rf[i:i + 60])[0, 1] / rf[i:i + 60].var(ddof=1) for i in range(0, 12000, 60)]
    return {"hedge_ratio_theory (rho*s_s/s_f)": rho * s_s / s_f, "hedge_ratio_estimated": float(h),
            "effectiveness_optimal_h": eff(h), "effectiveness_theory (rho^2)": rho ** 2,
            "effectiveness_naive_h=1": eff(1.0),
            "60day_window_hedge_ratio_range_p10_p90": (float(np.quantile(window, 0.1)), float(np.quantile(window, 0.9)))}


# 481 ---------------------------------------------------------------------------
def t481_neutral_construction():
    wl, bl = np.array([0.4, 0.3, 0.3]), np.array([1.2, 1.0, 1.4])
    ws, bs = np.array([0.4, 0.3, 0.3]), np.array([0.8, 0.7, 0.9])
    net_dollar = wl.sum() - ws.sum()
    net_beta = wl @ bl - ws @ bs
    k = (wl @ bl) / (ws @ bs)                              # scale the short book to cancel beta
    w = np.concatenate([wl, -ws])
    beta = np.concatenate([bl, bs])
    A = np.vstack([np.ones(6), beta])
    w_both = w - A.T @ np.linalg.solve(A @ A.T, A @ w)     # smallest change that makes both zero
    return {"dollar_neutral_book: net_dollar, net_beta": (float(net_dollar), float(net_beta)),
            "short_scale_for_beta_neutral": float(k), "after_scaling: net_dollar": float(wl.sum() - k * ws.sum()),
            "both_neutral_weights": w_both.round(3).tolist(), "both_neutral_check": (float(w_both.sum()), float(beta @ w_both)),
            "gross_exposure_before_after": (float(np.abs(w).sum()), float(np.abs(w_both).sum()))}


# 482 ---------------------------------------------------------------------------
def t482_active_measures():
    wp = np.array([0.30, 0.25, 0.20, 0.15, 0.10])
    wb = np.array([0.40, 0.20, 0.15, 0.15, 0.10])
    S = cov_from([0.20, 0.25, 0.22, 0.18, 0.30], np.full((5, 5), 0.5) + 0.5 * np.eye(5))
    a = wp - wb
    te = port_vol(a, S)
    active_ret = 0.015
    return {"active_share": 0.5 * float(np.abs(a).sum()), "tracking_error_pct": 100 * te,
            "information_ratio (1.5% active return)": active_ret / te}


# 483 ---------------------------------------------------------------------------
def t483_smart_beta():
    g = rng(43)
    n = 100
    cap = g.lognormal(0, 1.0, n)
    vol = g.uniform(0.15, 0.45, n)
    v1 = g.normal(size=n)
    v2 = 0.85 * v1 + math.sqrt(1 - 0.85 ** 2) * g.normal(size=n)    # value score a month later

    def weights(score, scheme):
        sel = np.argsort(score)[-30:]
        w = np.zeros(n)
        if scheme == "cap":
            w[sel] = cap[sel]
        elif scheme == "equal":
            w[sel] = 1.0
        else:
            w[sel] = 1 / vol[sel]
        return w / w.sum()

    out = {}
    for scheme in ("cap", "equal", "inverse_vol"):
        w1, w2 = weights(v1, scheme), weights(v2, scheme)
        out[scheme] = {"one_way_turnover_pct": round(100 * 0.5 * float(np.abs(w2 - w1).sum()), 1),
                       "effective_names": round(float(1 / (w1 ** 2).sum()), 1), "max_weight_pct": round(100 * float(w1.max()), 1)}
    return out


# 484 ---------------------------------------------------------------------------
def t484_esg_constraint():
    S = cov_from([0.12, 0.15, 0.20, 0.18, 0.25], np.full((5, 5), 0.3) + 0.7 * np.eye(5))
    esg = np.array([80.0, 60.0, 55.0, 70.0, 40.0])
    Si = np.linalg.inv(S)
    A = np.vstack([np.ones(5), esg])
    base = Si @ np.ones(5)
    base /= base.sum()
    out = {"unconstrained": {"score": float(esg @ base), "vol_pct": 100 * port_vol(base, S), "weights": base.round(3).tolist()}}
    for target in (70, 75, 80):
        b = np.array([1.0, target])
        w = Si @ A.T @ np.linalg.solve(A @ Si @ A.T, b)
        out[f"score={target}"] = {"score": float(esg @ w), "vol_pct": round(100 * port_vol(w, S), 3), "weights": w.round(3).tolist()}
    return out


ALL = [t476_ledger, t477_reconciliation, t478_risk_model, t479_factor_zoo, t480_hedging,
       t481_neutral_construction, t482_active_measures, t483_smart_beta, t484_esg_constraint]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
