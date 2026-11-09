"""Section 12.3 worked examples (topics 515 to 519). Run: python3 ex_12_2_margin_funding.py"""
from __future__ import annotations

import math

import numpy as np

from common import ND


# 515 ---------------------------------------------------------------------------
def t515_margin_projection():
    equity = 2_000_000.0
    book = {"index futures long": (4_000_000.0, 0.06, +1), "equities long": (3_000_000.0, 0.25, +1), "equities short": (1_500_000.0, 0.30, -1)}
    margin_now = sum(n * r for n, r, _ in book.values())
    move, hike = -0.10, 1.5
    pnl = sum(n * move * side for n, _, side in book.values())
    margin_stress = sum(n * (1 + move) * r * hike for n, r, _ in book.values())
    eq_after = equity + pnl
    buffer_target = 0.10
    s = (1 - buffer_target) * equity / (margin_stress - pnl)
    return {"margin_now": margin_now, "excess_liquidity_now": equity - margin_now,
            "stress_pnl (market -10%)": pnl, "equity_after": eq_after, "margin_after (rates x1.5, prices moved)": margin_stress,
            "excess_liquidity_after": eq_after - margin_stress,
            "share_of_book_to_keep_to_restore_10pct_buffer": s, "cut_needed_pct": 100 * (1 - s)}


# 516 ---------------------------------------------------------------------------
def span_like(position_notional_front: float, position_notional_back: float, beta_back: float = 0.97,
              scan_range: float = 0.07, extreme_mult: float = 3.0, extreme_cover: float = 0.35) -> dict:
    moves = [0, 1 / 3, -1 / 3, 2 / 3, -2 / 3, 1.0, -1.0]
    losses = []
    for m in moves:
        px = scan_range * m
        pnl = position_notional_front * px + position_notional_back * px * beta_back
        losses.append(-pnl)
    for m in (extreme_mult, -extreme_mult):
        px = scan_range * m
        pnl = position_notional_front * px + position_notional_back * px * beta_back
        losses.append(-pnl * extreme_cover)
    return {"scan_risk": max(0.0, max(losses)), "n_scenarios": len(losses)}


def t516_span():
    N = 250_000.0                                                      # one index future: 5,000 x $50
    outright = span_like(N, 0.0)
    pair = span_like(N, -N, beta_back=0.97)
    short = span_like(-N, 0.0)
    return {"outright_long_1_contract": outright, "outright_short_1_contract": short,
            "long_front_short_back_(beta 0.97)": pair,
            "sum_of_standalone_margins": outright["scan_risk"] + short["scan_risk"],
            "offset_credit_pct": 100 * (1 - pair["scan_risk"] / (outright["scan_risk"] + short["scan_risk"]))}


# 517 ---------------------------------------------------------------------------
def t517_cross_margin():
    z = ND.inv_cdf(0.99)
    a_val, b_val, sa, sb, rho = 1_000_000.0, -900_000.0, 0.012, 0.011, 0.9
    ra, rb = abs(a_val) * sa, abs(b_val) * sb
    standalone = z * (ra + rb)
    port_sd = math.sqrt(ra ** 2 + rb ** 2 + 2 * rho * (a_val * sa) * (b_val * sb))
    cross = z * port_sd
    out = {"standalone_margin_sum": standalone, "cross_margin": cross, "reduction_pct": 100 * (1 - cross / standalone)}
    equity, overnight_rate, intraday_rate = 100_000.0, 0.10, 0.025
    out["max_notional_overnight"] = equity / overnight_rate
    out["max_notional_intraday"] = equity / intraday_rate
    out["forced_cut_at_cutoff_if_holding_intraday_max_pct"] = 100 * (1 - (equity / overnight_rate) / (equity / intraday_rate))
    return out


# 518 ---------------------------------------------------------------------------
def t518_custody():
    amount, pd_, cap = 10_000_000.0, 0.005, 500_000.0
    cases = {"segregated client assets (LGD 2% from delay costs)": (0.02, 0.0),
             "unsegregated or rehypothecated (LGD 40%, 500k protection)": (0.40, cap),
             "unsegregated, no protection scheme (LGD 40%)": (0.40, 0.0)}
    out = {}
    for name, (lgd, prot) in cases.items():
        exposed = max(0.0, amount - prot)
        out[name] = {"expected_annual_loss": pd_ * lgd * exposed, "loss_if_broker_fails": lgd * exposed}
    return out


# 519 ---------------------------------------------------------------------------
def t519_liquidity_adjusted_var():
    V, sigma, adv_value, part = 10_000_000.0, 0.015, 20_000_000.0, 0.10
    z = ND.inv_cdf(0.99)
    var1 = z * sigma * V
    days = int(math.ceil(V / (part * adv_value)))
    remaining = [V * (days - k) / days for k in range(days)]                   # exposure at the start of each liquidation day
    var_liq = z * sigma * math.sqrt(sum(x ** 2 for x in remaining))
    spread_cost = 0.0005 / 2 * V                                               # half of a 5 bp quoted spread on the whole position
    impact = 0.5 * sigma * math.sqrt(V / adv_value) * V
    return {"VaR_1day_99": var1, "days_to_liquidate": days, "exposure_each_day_M": [round(x / 1e6, 1) for x in remaining],
            "VaR_over_liquidation_path": var_liq, "spread_cost": spread_cost, "impact_cost": impact,
            "LVaR": var_liq + spread_cost + impact, "LVaR/VaR": (var_liq + spread_cost + impact) / var1}


ALL = [t515_margin_projection, t516_span, t517_cross_margin, t518_custody, t519_liquidity_adjusted_var]

if __name__ == "__main__":
    for f in ALL:
        print(f"--- {f.__name__}")
        for k, v in f().items():
            print(f"  {k}: {v}")
