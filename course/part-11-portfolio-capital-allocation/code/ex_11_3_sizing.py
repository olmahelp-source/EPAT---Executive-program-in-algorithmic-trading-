"""Section 11.4 worked examples (topics 485 to 496). Run: python3 ex_11_3_sizing.py"""
from __future__ import annotations

import math

import numpy as np

from common import ND, rng


def max_drawdown(equity: np.ndarray) -> np.ndarray:
    """Max drawdown along the last axis (positive fractions)."""
    peak = np.maximum.accumulate(equity, axis=-1)
    return (1 - equity / peak).max(axis=-1)


# 485 ---------------------------------------------------------------------------
def t485_fixed_fractional():
    equity, risk, entry, stop = 100_000, 0.01, 50.0, 48.0
    shares = equity * risk / (entry - stop)
    g = rng(51)
    sims, trades, p, win_R = 2000, 1000, 0.45, 2.0           # 45% winners paying +2R, 55% losers -1R
    outcomes = np.where(g.random((sims, trades)) < p, win_R, -1.0)
    out = {"shares_for_1pct_risk": shares, "expectancy_R_per_trade": p * win_R - (1 - p), "kelly_fraction": (p * win_R - (1 - p)) / win_R}
    for f in (0.005, 0.01, 0.02, 0.05, 0.10, 0.20):
        eq = np.cumprod(1 + f * outcomes, axis=1)
        mdd = max_drawdown(eq)
        out[f"risk={f:.1%}"] = {"median_final_equity": round(float(np.median(eq[:, -1])), 2),
                                "median_max_dd_pct": round(100 * float(np.median(mdd)), 1),
                                "prob_dd_ge_50pct": round(float((mdd >= 0.5).mean()), 3)}
    return out


# 486 ---------------------------------------------------------------------------
def t486_kelly():
    mu, sigma = 0.08, 0.20
    fstar = mu / sigma ** 2
    g = rng(52)
    days, sims = 2520, 4000
    r = g.normal(mu / 252, sigma / math.sqrt(252), (sims, days))
    out = {"binary_p0.55_b1": (0.55 * 1 - 0.45) / 1, "binary_p0.40_b2": (0.40 * 2 - 0.60) / 2,
           "continuous_kelly_leverage": fstar, "max_growth_rate": mu ** 2 / (2 * sigma ** 2)}
    for m in (0.25, 0.5, 1.0, 1.5, 2.0):
        f = m * fstar
        growth = mu * f - 0.5 * sigma ** 2 * f ** 2
        wealth = np.exp(np.log1p(f * r).sum(1))
        out[f"{m}x_Kelly"] = {"theory_growth_pct": round(100 * growth, 2), "vol_pct": round(100 * f * sigma, 1),
                              "median_10y_multiple": round(float(np.median(wealth)), 2),
                              "p5_10y_multiple": round(float(np.quantile(wealth, 0.05)), 2)}
    out["edge_overestimated_2x: leverage_used / true_kelly"] = 2.0
    return out


# 487 ---------------------------------------------------------------------------
def t487_vol_targeting():
    g = rng(53)
    n, target, cap = 252 * 10, 0.10, 3.0
    vol_ann = np.where(np.arange(n) // 126 % 2 == 0, 0.10, 0.40)       # alternating calm and turbulent half-years
    r = g.normal(0.0003, 1, n) * vol_ann / math.sqrt(252)
    var = np.empty(n)
    var[0] = r[:20].var()
    for t in range(1, n):
        var[t] = 0.94 * var[t - 1] + 0.06 * r[t - 1] ** 2              # EWMA estimate known at the start of day t
    lev = np.minimum(cap, target / (np.sqrt(var * 252)))
    scaled = lev * r
    calm = vol_ann == 0.10
    rv = lambda x, m: float(x[m].std() * math.sqrt(252))
    return {"unscaled_realized_vol_calm/turbulent_pct": (100 * rv(r, calm), 100 * rv(r, ~calm)),
            "targeted_realized_vol_calm/turbulent_pct": (100 * rv(scaled, calm), 100 * rv(scaled, ~calm)),
            "avg_leverage_calm/turbulent": (float(lev[calm].mean()), float(lev[~calm].mean())),
            "max_leverage_used": float(lev.max()),
            "max_dd_unscaled_pct": 100 * float(max_drawdown(np.cumprod(1 + r))),
            "max_dd_targeted_pct": 100 * float(max_drawdown(np.cumprod(1 + scaled)))}


# 488 ---------------------------------------------------------------------------
def t488_risk_per_trade():
    equity, risk, entry = 100_000, 0.01, 50.0
    g = rng(54)
    gaps = 0.012 * g.standard_t(3, 200_000) / math.sqrt(3)             # overnight moves with fat tails
    q99 = float(np.quantile(-gaps, 0.99))
    out = {"overnight_gap_99th_pct_loss": 100 * q99}
    for stop in (48.0, 49.0, 49.5):
        stop_dist = (entry - stop) / entry
        pos = equity * risk / stop_dist
        out[f"stop={stop}"] = {"stop_distance_pct": round(100 * stop_dist, 1),
                               "position_pct_of_equity": round(100 * pos / equity, 1),
                               "loss_if_10pct_gap_pct_of_equity": round(100 * pos * 0.10 / equity, 1),
                               "gap_adjusted_position_pct": round(100 * risk / max(stop_dist, q99), 1),
                               "shares_plain/adjusted": (round(pos / entry), round(equity * risk / max(stop_dist, q99) / entry))}
    return out


# 489 ---------------------------------------------------------------------------
def twr(trades, f):
    worst = -min(trades)
    return float(np.prod([1 + f * x / worst for x in trades]))


def best_f(trades):
    fs = np.linspace(0.01, 1.0, 991)
    vals = [twr(trades, f) for f in fs]
    i = int(np.argmax(vals))
    return float(fs[i]), float(vals[i])


def t489_optimal_f():
    trades = [150, -100, 200, -80, 120, -150, 90, 60, -50, 170]
    f1, v1 = best_f(trades)
    without_worst = [x for x in trades if x != -150]
    f2, v2 = best_f(without_worst)
    return {"largest_loss": 150, "optimal_f": f1, "terminal_wealth_multiple_at_optimal_f": v1,
            "twr_at_f=0.2": twr(trades, 0.2), "twr_at_f=0.5": twr(trades, 0.5), "twr_at_f=0.8": twr(trades, 0.8),
            "optimal_f_after_removing_worst_trade": f2, "new_largest_loss": 100}


# 490 ---------------------------------------------------------------------------
def t490_equity_curve_sizing():
    g = rng(55)
    sims = 300
    drift = np.concatenate([np.full(750, 0.0008), np.full(750, -0.0005), np.full(500, 0.0006)])
    res = {"constant": [], "equity_ma_rule": []}
    for _ in range(sims):
        r = drift + g.normal(0, 0.01, len(drift))
        for name in res:
            eq = np.empty(len(r) + 1)
            eq[0] = 1.0
            for t in range(len(r)):
                size = 1.0
                if name == "equity_ma_rule" and t >= 50 and eq[t] < eq[t - 50:t].mean():
                    size = 0.5
                eq[t + 1] = eq[t] * (1 + size * r[t])
            res[name].append((eq[-1], float(max_drawdown(eq))))
    out = {}
    for name, v in res.items():
        v = np.array(v)
        out[name] = {"median_final_equity": round(float(np.median(v[:, 0])), 3), "median_max_dd_pct": round(100 * float(np.median(v[:, 1])), 1),
                     "p95_max_dd_pct": round(100 * float(np.quantile(v[:, 1], 0.95)), 1)}
    return out


# 491 ---------------------------------------------------------------------------
def t491_strategy_allocation_rules():
    g = rng(56)
    vol = np.array([0.08, 0.12, 0.16])
    sharpe_true = 0.8                                          # every strategy has the SAME true Sharpe
    n, sims = 252 * 10, 100
    C = np.linalg.cholesky(np.full((3, 3), 0.2) + 0.8 * np.eye(3))
    out = {k: {"sharpe": [], "turnover": []} for k in ("equal_capital", "inverse_vol", "performance_chasing")}
    for _ in range(sims):
        z = g.normal(size=(n, 3)) @ C.T
        r = sharpe_true * vol / 252 + vol / math.sqrt(252) * z      # annual mean = Sharpe x vol
        for name in out:
            w = np.full(3, 1 / 3)
            pnl, turn = [], 0.0
            for t in range(n):
                if t % 21 == 0 and t >= 126:
                    if name == "equal_capital":
                        new = np.full(3, 1 / 3)
                    elif name == "inverse_vol":
                        new = (1 / vol) / (1 / vol).sum()
                    else:
                        score = np.maximum(r[t - 126:t].mean(0) / r[t - 126:t].std(0), 0) + 1e-9
                        new = score / score.sum()
                    turn += 0.5 * np.abs(new - w).sum()
                    w = new
                pnl.append(w @ r[t])
            pnl = np.array(pnl[126:])
            out[name]["sharpe"].append(pnl.mean() / pnl.std() * math.sqrt(252))
            out[name]["turnover"].append(turn / 10)
    return {k: {"avg_sharpe": round(float(np.mean(v["sharpe"])), 3), "avg_turnover_per_year": round(float(np.mean(v["turnover"])), 2)} for k, v in out.items()}


# 492 ---------------------------------------------------------------------------
def t492_margin_buffer():
    equity, notional, m_now, m_stress, move = 2_000_000, 5_000_000, 0.20, 0.35, -0.08
    free_now = equity - m_now * notional
    loss = notional * move
    free_stress = equity + loss - m_stress * notional * (1 + move)
    g = rng(57)
    sims, days = 4000, 252
    res = {}
    for n_ in (4_000_000, 5_000_000, 6_000_000, 7_000_000):
        r = g.normal(0.0003, 0.20 / math.sqrt(252), (sims, days))
        path = np.cumprod(1 + r, axis=1)
        hike_day = g.integers(20, days, sims)
        hiked = g.random(sims) < 0.10                          # 10% of paths see a margin-rate hike
        rate = np.where((np.arange(days)[None, :] >= hike_day[:, None]) & hiked[:, None], m_stress, m_now)
        eq_path = equity + n_ * (path - 1)
        required = rate * n_ * path
        res[f"notional={n_ / 1e6:.0f}M"] = round(float((eq_path < required).any(1).mean()), 3)
    return {"free_margin_now": free_now, "free_margin_after_8pct_drop_and_margin_hike": free_stress,
            "buffer_needed_to_survive": max(0.0, -free_stress), "prob_margin_call_within_1y": res}


# 493 ---------------------------------------------------------------------------
def t493_pyramiding():
    budget = 1000.0                                            # total open risk allowed (1% of 100k)
    entries = [100, 102, 104, 106]
    atr_mult = 4                                               # stop sits 4 below the latest entry
    qty, rows = [], []
    for k, e in enumerate(entries):
        stop = e - atr_mult
        existing = sum(q * (entries[i] - stop) for i, q in enumerate(qty))
        q = max(0.0, (budget - existing) / (e - stop))
        qty.append(q)
        total = sum(q_ * (entries[i] - stop) for i, q_ in enumerate(qty))
        rows.append({"add": k + 1, "entry": e, "stop_for_all_units": stop, "new_units": round(q, 1),
                     "total_units": round(sum(qty), 1), "total_open_risk": round(total, 1)})
    return {"rows": rows}


# 494 ---------------------------------------------------------------------------
def margin_call_drop(L: float, m: float) -> float:
    return max(0.0, (1 / L - m) / (1 - m))


def t494_margin_call():
    m = 0.10
    g = rng(58)
    sims, days = 20000, 252
    r = g.normal(0.0003, 0.20 / math.sqrt(252), (sims, days))
    worst = np.cumprod(1 + r, axis=1).min(1) - 1                # worst point of the year relative to start
    out = {}
    for L in (2, 3, 5, 8):
        x = margin_call_drop(L, m)
        out[f"leverage={L}"] = {"price_drop_that_triggers_call_pct": round(100 * x, 1),
                                "prob_within_1y_(20%vol)": round(float((worst <= -x).mean()), 3)}
    out["leverage=10 (maintenance 10%)"] = {"price_drop_that_triggers_call_pct": 100 * margin_call_drop(10, m)}
    return out


# 495 ---------------------------------------------------------------------------
def ladder(dd: float) -> float:
    return 0.25 if dd > 0.15 else 0.5 if dd > 0.10 else 0.75 if dd > 0.05 else 1.0


def t495_drawdown_derisking():
    g = rng(59)
    sims, n = 500, 252 * 10
    res = {"no_ladder": [], "ladder": []}
    for _ in range(sims):
        r = g.normal(0.07 / 252, 0.15 / math.sqrt(252), n)
        for name in res:
            eq, peak = 1.0, 1.0
            path = np.empty(n)
            for t in range(n):
                size = ladder(1 - eq / peak) if name == "ladder" else 1.0
                eq *= 1 + size * r[t]
                peak = max(peak, eq)
                path[t] = eq
            res[name].append((path[-1], float(max_drawdown(path))))
    out = {}
    for name, v in res.items():
        v = np.array(v)
        out[name] = {"median_final_equity": round(float(np.median(v[:, 0])), 3), "median_max_dd_pct": round(100 * float(np.median(v[:, 1])), 1),
                     "p95_max_dd_pct": round(100 * float(np.quantile(v[:, 1], 0.95)), 1)}
    return out


# 496 ---------------------------------------------------------------------------
def nav_with_hwm(gross_returns, fee_rate=0.20, start_nav=100.0):
    nav, hwm = start_nav, start_nav
    rows = []
    for gr in gross_returns:
        gross = nav * (1 + gr)
        fee = fee_rate * max(0.0, gross - hwm)
        nav = gross - fee
        hwm = max(hwm, nav)
        rows.append((round(gross, 3), round(fee, 3), round(nav, 3), round(hwm, 3)))
    return rows


def t496_fund_mechanics():
    rows = nav_with_hwm([0.20, -0.10, 0.15])
    no_hwm = 100.0
    for gr in (0.20, -0.10, 0.15):
        gross = no_hwm * (1 + gr)
        no_hwm = gross - 0.20 * max(0.0, gross - no_hwm)            # fee on every up year, ignoring the high-water mark
    return {"year rows (gross NAV, fee, NAV after fee, HWM)": rows, "NAV_if_fee_charged_every_up_year_without_HWM": round(no_hwm, 3)}


ALL = [t485_fixed_fractional, t486_kelly, t487_vol_targeting, t488_risk_per_trade, t489_optimal_f,
       t490_equity_curve_sizing, t491_strategy_allocation_rules, t492_margin_buffer, t493_pyramiding,
       t494_margin_call, t495_drawdown_derisking, t496_fund_mechanics]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
