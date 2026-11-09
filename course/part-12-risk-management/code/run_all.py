"""Runs every Part 12 example and checks the key numbers quoted in the lessons.

Usage:  python3 run_all.py          (about 10 seconds, needs only numpy)
"""
from __future__ import annotations

import ex_12_1_controls_and_measures as r1
import ex_12_2_margin_funding as r2


def close(a, b, tol):
    assert abs(a - b) <= tol, f"{a} not within {tol} of {b}"


def main() -> None:
    r = r1.t497_pretrade_checks()
    assert r["1. normal buy 500 @100.2"] == "ACCEPT"
    assert r["5. buy 900 @100, pos 1500 + 900 working"] == ["projected position above limit"]
    assert r["burst of 5 orders within 0.4 s (limit 3 per second)"][:3] == ["ACCEPT"] * 3
    r = r1.t498_pnl_monitor(); close(r["total_pnl"], 800, 1e-9)
    r = r1.t499_kill_switch(); assert r["loss_trip_minute"] is not None and r["reject_rule_tripped_at_order"] == 22
    r = r1.t500_var_backtest(); assert (r["normal_250d"]["exceptions"], r["historical_250d"]["exceptions"], r["ewma_0.94"]["exceptions"]) == (34, 39, 31)
    r = r1.t501_expected_shortfall(); close(r["normal_sigma1pct_a=0.975"]["ES_pct"], 2.338, 0.001)
    r = r1.t502_scenarios(); close(r["Equity crash -20% (vol +15, credit +150bp, rates -50bp)"]["total"], -1_030_000, 1e-6)
    r = r1.t503_reverse_stress(); close(r["loss=300,000"]["sigma_distance"], 3.33, 0.01)
    r = r1.t504_loss_limits(); assert r["share_of_paths_stuck_halted_at_end (no restart rule)"] > 0.5 and r["halts_per_year (with restart rule)"] < 1
    r = r1.t505_correlation_breakdown(); close(r["rho=0.3"]["portfolio_vol_pct"], 12.17, 0.01)
    r = r1.t506_liquidity(); close(r["B"]["days_to_liquidate_at_10pct"], 5.0, 1e-9)
    r = r1.t507_counterparty(); assert r["equal"]["worst_single_failure_loss"] < r["all_in_broker_1"]["worst_single_failure_loss"]
    assert r["equal"]["expected_annual_loss"] > r["all_in_broker_1"]["expected_annual_loss"]
    r = r1.t508_model_risk(); assert r["normal_bias_vs_truth_pct"] < -5
    r = r1.t509_concentration(); assert r["3 clusters, within 0.8, between 0.2"]["effective_number_of_bets"] < 1.2
    close(r["all assets independent"]["effective_number_of_bets"], 10.0, 1e-6)
    r = r1.t510_risk_budgeting(); [close(a, b, 0.05) for a, b in zip(r["achieved_risk_pct"], r["target_risk_budget_pct"])]
    r = r1.t511_option_book_risk(); assert r["grid (full_reval, delta-gamma-vega, error)"]["spot +0%, vol +0pts"] == (0, 0, 0)
    assert abs(r["grid (full_reval, delta-gamma-vega, error)"]["spot -10%, vol +5pts"][2]) > 100
    r = r1.t512_gap_risk(); assert r["overnight_loss_quantiles_pct"][0.999] > 4 * r["overnight_loss_quantiles_pct"][0.99]
    r = r1.t513_operational_risk(); assert r["controls: half the frequency, 50k cap per event"]["p99"] < r["no_controls"]["p99"] / 4
    r = r1.t514_risk_of_ruin(); assert r["risk_per_trade=2%"]["p_uncertain_U(0.48,0.58)"] > r["risk_per_trade=2%"]["known_p=0.55"] + 0.1

    r = r2.t515_margin_projection(); close(r["share_of_book_to_keep_to_restore_10pct_buffer"], 0.7217, 1e-3)
    r = r2.t516_span(); close(r["offset_credit_pct"], 98.5, 0.05)
    r = r2.t517_cross_margin(); close(r["reduction_pct"], 75.8, 0.1)
    r = r2.t518_custody(); assert r["segregated client assets (LGD 2% from delay costs)"]["loss_if_broker_fails"] == 200_000
    r = r2.t519_liquidity_adjusted_var(); close(r["LVaR/VaR"], 1.64, 0.01)
    print("all Part 12 checks passed")


if __name__ == "__main__":
    main()
