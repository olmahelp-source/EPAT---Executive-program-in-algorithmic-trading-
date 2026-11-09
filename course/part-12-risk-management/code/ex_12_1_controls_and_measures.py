"""Sections 12.1 and 12.2 worked examples (topics 497 to 514). Run: python3 ex_12_1_controls_and_measures.py"""
from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field

import numpy as np

from common import (ND, bs_greeks, bs_price, chi2_1_sf, cov_from, max_drawdown, rng, xlogy)


# 497 ---------------------------------------------------------------------------
@dataclass
class Limits:
    max_order_qty: int = 1000
    max_order_notional: float = 100_000
    max_abs_position: int = 3000
    collar_pct: float = 0.05
    max_ref_age_s: float = 5.0
    max_orders_per_window: int = 3
    window_s: float = 1.0


@dataclass
class OrderIntent:
    side: str
    qty: int
    price: float
    ts: float


class RiskGate:
    def __init__(self, limits: Limits) -> None:
        self.L = limits
        self._recent: deque[float] = deque()

    def check(self, o: OrderIntent, ref_price: float, ref_ts: float, position: int, working_signed: int):
        L, why = self.L, []
        if o.qty <= 0:
            why.append("non-positive quantity")
        if o.qty > L.max_order_qty:
            why.append("order quantity above limit")
        if o.qty * o.price > L.max_order_notional:
            why.append("order notional above limit")
        if o.ts - ref_ts > L.max_ref_age_s:
            why.append("reference price stale")
        elif abs(o.price - ref_price) / ref_price > L.collar_pct:
            why.append("price outside collar")
        signed = o.qty if o.side == "B" else -o.qty
        if abs(position + working_signed + signed) > L.max_abs_position:
            why.append("projected position above limit")
        while self._recent and o.ts - self._recent[0] > L.window_s:
            self._recent.popleft()
        if len(self._recent) >= L.max_orders_per_window:
            why.append("order rate limit")
        if not why:
            self._recent.append(o.ts)
        return why


def t497_pretrade_checks():
    gate = RiskGate(Limits())
    cases = [
        ("1. normal buy 500 @100.2", OrderIntent("B", 500, 100.2, 10.0), 100.0, 9.5, 0, 0),
        ("2. buy 2000 @100 (too big)", OrderIntent("B", 2000, 100.0, 20.0), 100.0, 19.5, 0, 0),
        ("3. buy 800 @108 (fat finger)", OrderIntent("B", 800, 108.0, 30.0), 100.0, 29.5, 0, 0),
        ("4. buy 900 @100, position 2500", OrderIntent("B", 900, 100.0, 40.0), 100.0, 39.5, 2500, 0),
        ("5. buy 900 @100, pos 1500 + 900 working", OrderIntent("B", 900, 100.0, 50.0), 100.0, 49.5, 1500, 900),
        ("6. buy 100 @100, reference 10 s old", OrderIntent("B", 100, 100.0, 60.0), 100.0, 50.0, 0, 0),
    ]
    out = {}
    for name, o, ref, rts, pos, wk in cases:
        out[name] = gate.check(o, ref, rts, pos, wk) or "ACCEPT"
    burst = []
    for i in range(5):
        burst.append(gate.check(OrderIntent("B", 10, 100.0, 100.0 + 0.1 * i), 100.0, 100.0, 0, 0) or "ACCEPT")
    out["burst of 5 orders within 0.4 s (limit 3 per second)"] = burst
    return out


# 498 ---------------------------------------------------------------------------
def t498_pnl_monitor():
    book = {"AAA": dict(qty=100, cost=150.0, px=155.0, age=1.0), "BBB": dict(qty=-200, cost=40.0, px=38.5, age=12.0)}
    stale_after, gross_limit = 5.0, 50_000
    rows, tot, gross, net = [], 0.0, 0.0, 0.0
    for s, p in book.items():
        pnl = p["qty"] * (p["px"] - p["cost"])
        tot += pnl
        gross += abs(p["qty"]) * p["px"]
        net += p["qty"] * p["px"]
        rows.append((s, round(pnl, 2), "STALE" if p["age"] > stale_after else "ok"))
    return {"positions (symbol, unrealized_pnl, price_status)": rows, "total_pnl": tot, "gross_exposure": gross,
            "net_exposure": net, "gross_limit_utilization_pct": 100 * gross / gross_limit}


# 499 ---------------------------------------------------------------------------
class KillSwitch:
    def __init__(self, equity: float, daily_loss_limit_pct: float = 0.02, max_reject_rate: float = 0.30, window: int = 20):
        self.limit = -daily_loss_limit_pct * equity
        self.max_rr, self.window = max_reject_rate, window
        self.tripped_reason: str | None = None
        self._results: deque[bool] = deque(maxlen=window)

    def on_pnl(self, pnl: float):
        if self.tripped_reason is None and pnl <= self.limit:
            self.tripped_reason = f"daily loss {pnl:,.0f} <= {self.limit:,.0f}"

    def on_order_result(self, accepted: bool):
        self._results.append(accepted)
        if self.tripped_reason is None and len(self._results) == self.window:
            rejects = self.window - sum(self._results)
            if rejects > self.max_rr * self.window:
                self.tripped_reason = f"{rejects} rejects in the last {self.window} orders (limit {self.max_rr * self.window:.0f})"

    def allow_new_orders(self) -> bool:
        return self.tripped_reason is None


def t499_kill_switch():
    g = rng(61)
    ks = KillSwitch(equity=100_000)
    pnl, trip_minute = 0.0, None
    for minute in range(390):
        pnl += g.normal(-6.0, 40.0)                               # a bad trading day, minute by minute
        ks.on_pnl(pnl)
        if trip_minute is None and not ks.allow_new_orders():
            trip_minute = minute
            break
    ks2 = KillSwitch(equity=100_000)
    pattern = [True] * 10 + [False] * 4 + [True] * 6 + [False] * 5
    stop_at = None
    for i, ok in enumerate(pattern):
        ks2.on_order_result(ok)
        if stop_at is None and not ks2.allow_new_orders():
            stop_at = i
    return {"loss_limit": ks.limit, "loss_trip_minute": trip_minute, "pnl_at_trip": round(pnl, 0), "loss_reason": ks.tripped_reason,
            "reject_rule_tripped_at_order": stop_at, "reject_reason": ks2.tripped_reason}


# 500 ---------------------------------------------------------------------------
def sim_garch(n, omega, alpha, beta, g):
    r = np.empty(n)
    var = omega / (1 - alpha - beta)
    for t in range(n):
        r[t] = math.sqrt(var) * g.normal()
        var = omega + alpha * r[t] ** 2 + beta * var
    return r


def kupiec(x, T, p):
    ph = x / T
    ll0 = xlogy(T - x, 1 - p) + xlogy(x, p)
    ll1 = xlogy(T - x, 1 - ph) + xlogy(x, ph)
    lr = -2 * (ll0 - ll1)
    return lr, chi2_1_sf(lr)


def christoffersen_ind(hits):
    n00 = n01 = n10 = n11 = 0
    for a, b in zip(hits[:-1], hits[1:]):
        n00 += (a == 0 and b == 0); n01 += (a == 0 and b == 1); n10 += (a == 1 and b == 0); n11 += (a == 1 and b == 1)
    pi0 = n01 / max(n00 + n01, 1)
    pi1 = n11 / max(n10 + n11, 1)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    ll0 = xlogy(n00 + n10, 1 - pi) + xlogy(n01 + n11, pi)
    ll1 = xlogy(n00, 1 - pi0) + xlogy(n01, pi0) + xlogy(n10, 1 - pi1) + xlogy(n11, pi1)
    lr = -2 * (ll0 - ll1)
    return lr, chi2_1_sf(lr)


def t500_var_backtest():
    g = rng(62)
    n, W = 2750, 250
    r = sim_garch(n, 2e-6, 0.10, 0.88, g)
    z = ND.inv_cdf(0.99)
    var_norm, var_hist, var_ewma = [], [], []
    ew = r[:W].var()
    for t in range(W, n):
        win = r[t - W:t]
        var_norm.append(z * win.std(ddof=1))
        var_hist.append(-np.quantile(win, 0.01))
        var_ewma.append(z * math.sqrt(ew))
        ew = 0.94 * ew + 0.06 * r[t] ** 2
    actual = r[W:]
    T = len(actual)
    out = {"days": T, "expected_exceptions": 0.01 * T}
    for name, v in (("normal_250d", var_norm), ("historical_250d", var_hist), ("ewma_0.94", var_ewma)):
        hits = (actual < -np.array(v)).astype(int)
        x = int(hits.sum())
        lr, p = kupiec(x, T, 0.01)
        lci, pci = christoffersen_ind(list(hits))
        out[name] = {"exceptions": x, "kupiec_LR": round(float(lr), 2), "kupiec_p": round(float(p), 4),
                     "independence_LR": round(float(lci), 2), "independence_p": round(float(pci), 4)}
    return out


# 501 ---------------------------------------------------------------------------
def t501_expected_shortfall():
    out = {}
    for a in (0.975, 0.99):
        z = ND.inv_cdf(a)
        out[f"normal_sigma1pct_a={a}"] = {"VaR_pct": round(100 * 0.01 * z, 3), "ES_pct": round(100 * 0.01 * ND.pdf(z) / (1 - a), 3)}
    g = rng(63)
    x = 0.01 * g.standard_t(5, 3_000_000) / math.sqrt(5 / 3)
    loss = -x
    for a in (0.975, 0.99):
        v = float(np.quantile(loss, a))
        e = float(loss[loss >= v].mean())
        out[f"student_t5_sigma1pct_a={a}"] = {"VaR_pct": round(100 * v, 3), "ES_pct": round(100 * e, 3), "ES/VaR": round(e / v, 3)}
    return out


# 502 ---------------------------------------------------------------------------
def t502_scenarios():
    sens = {"equity_return": 5_000_000.0, "vol_points": 8_000.0, "rate_bp": -12_000.0, "credit_bp": -5_000.0}
    scenarios = {
        "Equity crash -20% (vol +15, credit +150bp, rates -50bp)": dict(equity_return=-0.20, vol_points=15, rate_bp=-50, credit_bp=150),
        "Rates shock +100bp (equity -5%)": dict(equity_return=-0.05, vol_points=3, rate_bp=100, credit_bp=30),
        "Credit crunch (credit +300bp, equity -12%)": dict(equity_return=-0.12, vol_points=10, rate_bp=-25, credit_bp=300),
        "Melt-up (equity +10%, vol -5)": dict(equity_return=0.10, vol_points=-5, rate_bp=20, credit_bp=-30),
    }
    out = {}
    for name, sc in scenarios.items():
        parts = {k: sens[k] * v for k, v in sc.items()}
        out[name] = {"total": sum(parts.values()), **{k: round(v) for k, v in parts.items()}}
    return out


# 503 ---------------------------------------------------------------------------
def t503_reverse_stress():
    g_vec = np.array([5_000_000.0, -12_000.0, -5_000.0])              # P&L per unit move: equity return, rate bp, credit bp
    vol = np.array([0.012, 6.0, 4.0])                                 # daily vols
    corr = np.array([[1, 0.3, -0.4], [0.3, 1, 0.2], [-0.4, 0.2, 1]])
    S = cov_from(vol, corr)
    denom = float(g_vec @ S @ g_vec)
    out = {"portfolio_daily_pnl_sd": math.sqrt(denom)}
    for loss in (200_000.0, 300_000.0, 500_000.0):
        shock = -loss * (S @ g_vec) / denom                           # most likely shock producing the loss
        dist = loss / math.sqrt(denom)
        out[f"loss={loss:,.0f}"] = {"sigma_distance": round(dist, 2),
                                    "shock (equity %, rates bp, credit bp)": (round(100 * float(shock[0]), 2), round(float(shock[1]), 1), round(float(shock[2]), 1)),
                                    "check_pnl": round(float(g_vec @ shock)), "normal_probability": round(1 - ND.cdf(dist), 5)}
    return out


# 504 ---------------------------------------------------------------------------
def run_limits(r, restart: bool):
    eq, peak, m, halt = 1.0, 1.0, 1.0, 0
    path = np.empty(len(r))
    halts, ended_halted = 0, False
    for t in range(len(r)):
        if halt > 0:
            halt -= 1
            ret = 0.0
            if halt == 0 and restart:
                peak = eq                                    # cooling-off over: re-baseline the drawdown reference
        else:
            ret = m * r[t]
        eq *= 1 + ret
        peak = max(peak, eq)
        dd = 1 - eq / peak
        if dd >= 0.15 and halt == 0 and m == 0.5:
            halt, halts = 20, halts + 1
        if dd >= 0.10:
            m = 0.5
        elif dd < 0.05:
            m = 1.0
        path[t] = eq
        ended_halted = halt > 0 or (not restart and dd >= 0.15)
    return path, halts, ended_halted


def t504_loss_limits():
    g = rng(64)
    sims, n = 400, 252 * 5
    stats = {"no_limits": [], "limits_with_restart_rule": [], "limits_without_restart_rule": []}
    halts_r, stuck = [], 0
    for _ in range(sims):
        r = g.normal(0.0004, 0.01, n)
        path = np.cumprod(1 + r)
        stats["no_limits"].append((path[-1], float(max_drawdown(path))))
        p2, h2, _ = run_limits(r, True)
        stats["limits_with_restart_rule"].append((p2[-1], float(max_drawdown(p2))))
        halts_r.append(h2)
        p3, h3, st = run_limits(r, False)
        stats["limits_without_restart_rule"].append((p3[-1], float(max_drawdown(p3))))
        stuck += bool(st)
    out = {}
    for name, v in stats.items():
        v = np.array(v)
        out[name] = {"median_final_equity": round(float(np.median(v[:, 0])), 3), "median_max_dd_pct": round(100 * float(np.median(v[:, 1])), 1),
                     "p95_max_dd_pct": round(100 * float(np.quantile(v[:, 1], 0.95)), 1)}
    out["halts_per_year (with restart rule)"] = float(np.mean(halts_r) / 5)
    out["share_of_paths_stuck_halted_at_end (no restart rule)"] = stuck / sims
    return out


# 505 ---------------------------------------------------------------------------
def t505_correlation_breakdown():
    N, sigma = 10, 0.20
    rows = {}
    for rho in (0.0, 0.3, 0.5, 0.8, 1.0):
        var = sigma ** 2 * (1 / N + (1 - 1 / N) * rho)
        rows[f"rho={rho}"] = {"portfolio_vol_pct": round(100 * math.sqrt(var), 2),
                              "diversification_ratio": round(sigma / math.sqrt(var), 2),
                              "effective_independent_bets": round(1 / (1 / N + (1 - 1 / N) * rho), 2)}
    return rows


# 506 ---------------------------------------------------------------------------
def t506_liquidity():
    price, part, c = 50.0, 0.10, 0.5
    names = {"A": (200_000, 2_000_000, 0.015, 5), "B": (500_000, 1_000_000, 0.025, 15), "C": (50_000, 5_000_000, 0.010, 3)}
    out = {}
    for s, (pos, adv, vol, spr) in names.items():
        days = pos / (part * adv)
        half_spread = spr / 2 / 1e4
        impact = c * vol * math.sqrt(pos / adv)
        out[s] = {"position_value": pos * price, "days_to_liquidate_at_10pct": round(days, 2),
                  "half_spread_bps": round(half_spread * 1e4, 1), "impact_bps": round(impact * 1e4, 1),
                  "total_cost_$": round(pos * price * (half_spread + impact))}
    return out


# 507 ---------------------------------------------------------------------------
def t507_counterparty():
    capital, lgd, protection = 10_000_000.0, 0.25, 500_000.0
    pd_ = np.array([0.003, 0.005, 0.015])
    allocs = {"all_in_broker_1": [1.0, 0.0, 0.0], "60/30/10": [0.6, 0.3, 0.1], "equal": [1 / 3] * 3, "all_in_broker_3": [0.0, 0.0, 1.0]}
    out = {}
    for name, a in allocs.items():
        amt = capital * np.array(a)
        unprot = np.maximum(amt - protection * (amt > 0), 0)
        out[name] = {"expected_annual_loss": round(float((pd_ * lgd * unprot).sum())),
                     "worst_single_failure_loss": round(float((lgd * unprot).max())),
                     "herfindahl": round(float((np.array(a) ** 2).sum()), 3)}
    return out


# 508 ---------------------------------------------------------------------------
def t508_model_risk():
    g = rng(65)
    nu, sims, n = 5, 5000, 250
    scale = 0.01 / math.sqrt(nu / (nu - 2))
    true_var = float(-np.quantile(scale * g.standard_t(nu, 4_000_000), 0.01))   # true 99% VaR of the fat-tailed process
    hist, norm = [], []
    z = ND.inv_cdf(0.99)
    for _ in range(sims):
        x = scale * g.standard_t(nu, n)
        hist.append(-np.quantile(x, 0.01))
        norm.append(z * x.std(ddof=1))
    hist, norm = np.array(hist), np.array(norm)
    return {"true_VaR99_pct": 100 * true_var,
            "historical_250d: mean, rel_sd, p5-p95 (pct)": (round(float(100 * hist.mean()), 3), round(float(hist.std() / hist.mean()), 3),
                                                            (round(float(100 * np.quantile(hist, .05)), 3), round(float(100 * np.quantile(hist, .95)), 3))),
            "normal_250d: mean, rel_sd, p5-p95 (pct)": (round(float(100 * norm.mean()), 3), round(float(norm.std() / norm.mean()), 3),
                                                        (round(float(100 * np.quantile(norm, .05)), 3), round(float(100 * np.quantile(norm, .95)), 3))),
            "normal_bias_vs_truth_pct": float(100 * (norm.mean() / true_var - 1))}


# 509 ---------------------------------------------------------------------------
def enb(w, S):
    lam, E = np.linalg.eigh(S)
    expo = E.T @ w
    p = expo ** 2 * lam / float(w @ S @ w)
    top = np.sort(p)[::-1]
    p = p[p > 1e-12]
    return math.exp(-float((p * np.log(p)).sum())), top


def block_corr(sizes, within, between):
    n = sum(sizes)
    corr = np.full((n, n), between)
    i = 0
    for s_ in sizes:
        corr[i:i + s_, i:i + s_] = within
        i += s_
    np.fill_diagonal(corr, 1.0)
    return corr


def t509_concentration():
    sizes = [4, 3, 3]
    n = sum(sizes)
    w = np.full(n, 1 / n)                                   # ten equal positions in every case
    out = {"positions": n, "effective_names_by_weights (1/HHI)": float(1 / (w ** 2).sum())}
    for name, within, between in (("3 clusters, within 0.8, between 0.2", 0.8, 0.2),
                                  ("3 clusters, within 0.8, between 0.0", 0.8, 0.0),
                                  ("all assets independent", 0.0, 0.0)):
        S = cov_from(np.full(n, 0.20), block_corr(sizes, within, between))
        e, top = enb(w, S)
        out[name] = {"effective_number_of_bets": round(e, 2), "portfolio_vol_pct": round(100 * math.sqrt(float(w @ S @ w)), 2),
                     "risk_share_of_largest_principal_portfolio_pct": round(100 * float(top[0]), 1)}
    return out


# 510 ---------------------------------------------------------------------------
def t510_risk_budgeting():
    S = cov_from([0.10, 0.20, 0.30], [[1, .3, .2], [.3, 1, .4], [.2, .4, 1]])
    w = np.array([0.5, 0.3, 0.2])
    sp = math.sqrt(w @ S @ w)
    rc = w * (S @ w) / sp
    budget = np.array([0.6, 0.25, 0.15])
    wb = np.full(3, 1 / 3)
    for _ in range(3000):
        r = wb * (S @ wb)
        wb = wb * np.sqrt(budget * r.sum() / r)
        wb /= wb.sum()
    spb = math.sqrt(wb @ S @ wb)
    return {"capital_weights": w.tolist(), "portfolio_vol_pct": 100 * sp, "risk_contribution_pct": (100 * rc / sp).round(1).tolist(),
            "target_risk_budget_pct": (100 * budget).tolist(), "weights_for_budget": wb.round(3).tolist(),
            "achieved_risk_pct": (100 * wb * (S @ wb) / spb ** 2).round(1).tolist(), "vol_pct_for_budget": 100 * spb}


# 511 ---------------------------------------------------------------------------
BOOK = [(+200, 100.0, 0.25, "call"), (-300, 95.0, 0.25, "put"), (+100, 110.0, 0.50, "call")]   # (units, strike, T, kind)


def book_value(S, sig, r=0.03, shift_T=0.0):
    return sum(q * bs_price(S, K, T - shift_T, r, sig, k) for q, K, T, k in BOOK)


def t511_option_book_risk():
    S0, sig0, r = 100.0, 0.20, 0.03
    agg = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0}
    for q, K, T, k in BOOK:
        gr = bs_greeks(S0, K, T, r, sig0, k)
        for key in agg:
            agg[key] += q * gr[key]
    base = book_value(S0, sig0)
    grid = {}
    for dS in (-0.10, -0.05, 0.0, 0.05, 0.10):
        for dv in (-5, 0, 5):
            S, sig = S0 * (1 + dS), sig0 + dv / 100
            full = book_value(S, sig) - base
            ds = S - S0
            approx = agg["delta"] * ds + 0.5 * agg["gamma"] * ds ** 2 + agg["vega"] * (dv / 100)
            grid[f"spot {dS:+.0%}, vol {dv:+d}pts"] = (round(full), round(approx), round(full - approx))
    return {"book_value": base, "delta_shares": agg["delta"], "gamma": agg["gamma"], "vega_per_vol_point": agg["vega"] / 100,
            "theta_per_day": agg["theta"] / 365, "grid (full_reval, delta-gamma-vega, error)": grid}


# 512 ---------------------------------------------------------------------------
def t512_gap_risk():
    g = rng(66)
    n = 1_000_000
    gap = g.normal(0.0002, 0.005, n)
    jumps = g.random(n) < 0.01
    gap = gap + jumps * g.normal(-0.03, 0.02, n)
    loss = -gap
    q = {a: float(np.quantile(loss, a)) for a in (0.95, 0.99, 0.999)}
    stop = 0.02
    beyond = loss[loss > stop]
    budget = 0.01
    return {"overnight_loss_quantiles_pct": {a: round(100 * v, 2) for a, v in q.items()},
            "prob_gap_loss_exceeds_2pct_stop": float((loss > stop).mean()),
            "avg_loss_given_beyond_stop_pct": 100 * float(beyond.mean()),
            "max_position_for_1pct_equity_gap_budget_using_99%_pct_of_equity": 100 * budget / q[0.99],
            "max_position_for_1pct_equity_gap_budget_using_99.9%_pct_of_equity": 100 * budget / q[0.999]}


# 513 ---------------------------------------------------------------------------
def t513_operational_risk():
    g = rng(67)
    years = 200_000
    out = {}
    for name, lam, cap in (("no_controls", 4.0, None), ("controls: half the frequency, 50k cap per event", 2.0, 50_000.0)):
        counts = g.poisson(lam, years)
        sev = g.lognormal(math.log(10_000), 1.5, counts.sum())
        if cap:
            sev = np.minimum(sev, cap)
        total = np.bincount(np.repeat(np.arange(years), counts), weights=sev, minlength=years)
        out[name] = {"mean_annual_loss": round(float(total.mean())), "p95": round(float(np.quantile(total, 0.95))),
                     "p99": round(float(np.quantile(total, 0.99))), "p99.9": round(float(np.quantile(total, 0.999)))}
    return out


# 514 ---------------------------------------------------------------------------
def t514_risk_of_ruin():
    g = rng(68)
    sims, trades = 4000, 1000
    out = {}
    for f in (0.02, 0.05, 0.10, 0.20):
        known = np.where(g.random((sims, trades)) < 0.55, f, -f)
        p_unc = g.uniform(0.48, 0.58, (sims, 1))                    # edge unknown: p drawn per account
        unc = np.where(g.random((sims, trades)) < p_unc, f, -f)
        row = {}
        for name, o in (("known_p=0.55", known), ("p_uncertain_U(0.48,0.58)", unc)):
            eq = np.cumprod(1 + o, axis=1)
            row[name] = round(float((eq.min(1) <= 0.5).mean()), 3)
        out[f"risk_per_trade={f:.0%}"] = row
    return out


ALL = [t497_pretrade_checks, t498_pnl_monitor, t499_kill_switch, t500_var_backtest, t501_expected_shortfall,
       t502_scenarios, t503_reverse_stress, t504_loss_limits, t505_correlation_breakdown, t506_liquidity,
       t507_counterparty, t508_model_risk, t509_concentration, t510_risk_budgeting, t511_option_book_risk,
       t512_gap_risk, t513_operational_risk, t514_risk_of_ruin]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
