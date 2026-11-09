"""Runs every Part 11 example and checks the key numbers quoted in the lessons.

Usage:  python3 run_all.py          (about 40 seconds, needs only numpy)
"""
from __future__ import annotations

import ex_11_1_construction as c1
import ex_11_2_book_and_risk_models as c2
import ex_11_3_sizing as c3


def close(a, b, tol):
    assert abs(a - b) <= tol, f"{a} not within {tol} of {b}"


def main() -> None:
    r = c1.t462_mean_variance(); assert r["avg_L1_weight_change_for_0.5pct_mu_noise"] > 0.2
    r = c1.t463_black_litterman(); assert r["view_spread_prior_pct"] < r["view_spread_posterior_pct"] < 2.0
    r = c1.t464_risk_parity(); [close(x, 100 / 3, 0.01) for x in r["correlated_risk_contributions_pct"]]
    r = c1.t465_hrp(); assert set(r["leaf_order"][:3]) in ({0, 1, 2}, {3, 4, 5})
    r = c1.t467_cvar(); assert r["min_cvar99"]["cvar99_pct"] < r["min_variance"]["cvar99_pct"]
    r = c1.t468_resampled(); assert r["avg_weight_std_across_samples_resampled"] < r["avg_weight_std_across_samples_plain"]
    assert r["avg_true_utility_resampled"] > r["avg_true_utility_plain"]
    r = c1.t469_factor_construction(); close(r["neutral_dollar"], 0, 1e-9); close(r["neutral_beta"], 0, 1e-9)
    r = c1.t470_constraints(); assert r["cap15_with_5_assets"].startswith("infeasible")
    r = c1.t471_tcost_aware(); [close(v["closed_form"], v["grid_search"], 1e-3) for k, v in r.items() if k.startswith("w0=")]
    r = c1.t472_multiperiod(); assert r["dynamic_total_utility"] >= r["myopic_total_utility"]
    r = c1.t473_strategy_allocation(); assert all(v["vol_stress_corr_pct"] > v["vol_backtest_corr_pct"] for v in r.values())
    r = c1.t474_regime_allocation(); assert r["hysteresis_(70/30)_flips"] < r["hard_switch_at_50pct_flips"]
    r = c1.t475_rebalancing(); assert r["never"]["rms_weight_drift_pct"] > 5 * r["monthly"]["rms_weight_drift_pct"]
    assert r["band_5pct"]["turnover_per_year_pct"] < r["monthly"]["turnover_per_year_pct"]

    r = c2.t476_ledger(); close(r["total_realized"], 1260, 1e-9); close(r["unrealized_at_54"], 120, 1e-9)
    r = c2.t477_reconciliation(); assert len(r["breaks (symbol, type, local, broker)"]) == 2
    r = c2.t478_risk_model(); close(r["total_variance"], r["check_sum"], 1e-12)
    r = c2.t479_factor_zoo(); assert r["bonferroni_threshold_t"] > 3.5 and r["factors_with_|t|>3"] <= 2
    r = c2.t480_hedging(); close(r["effectiveness_optimal_h"], 0.81, 0.01)
    r = c2.t481_neutral_construction(); close(r["both_neutral_check"][0], 0, 1e-9); close(r["both_neutral_check"][1], 0, 1e-9)
    r = c2.t482_active_measures(); close(r["active_share"], 0.10, 1e-9)

    r = c3.t486_kelly(); close(r["continuous_kelly_leverage"], 2.0, 1e-9); close(r["2.0x_Kelly"]["theory_growth_pct"], 0.0, 1e-9)
    r = c3.t487_vol_targeting(); u, t = r["unscaled_realized_vol_calm/turbulent_pct"], r["targeted_realized_vol_calm/turbulent_pct"]
    assert t[1] < u[1] / 2
    r = c3.t489_optimal_f(); assert 0.3 < r["optimal_f"] < 0.6
    r = c3.t490_equity_curve_sizing(); assert r["equity_ma_rule"]["median_max_dd_pct"] < r["constant"]["median_max_dd_pct"]
    r = c3.t491_strategy_allocation_rules(); assert r["performance_chasing"]["avg_sharpe"] < r["equal_capital"]["avg_sharpe"]
    r = c3.t494_margin_call(); close(r["leverage=5"]["price_drop_that_triggers_call_pct"], 11.1, 0.05)
    r = c3.t495_drawdown_derisking(); assert r["ladder"]["p95_max_dd_pct"] < r["no_ladder"]["p95_max_dd_pct"]
    r = c3.t496_fund_mechanics(); close(r["year rows (gross NAV, fee, NAV after fee, HWM)"][-1][2], 119.248, 1e-9)
    print("all Part 11 checks passed")


if __name__ == "__main__":
    main()
