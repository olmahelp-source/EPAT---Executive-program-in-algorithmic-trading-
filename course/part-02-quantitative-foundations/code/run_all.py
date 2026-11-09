"""Runs every Part 2 example and checks the key numbers quoted in the lessons.

Usage:  python3 run_all.py          (about 5 seconds, needs only numpy)
"""
from __future__ import annotations

import math

import ex_2_1_statistics as s1
import ex_2_2_advanced as s2
import ex_2_3_mathematics as s3


def close(a, b, tol):
    assert abs(a - b) <= tol, f"{a} not within {tol} of {b}"


def main() -> None:
    r = s1.t38_ttest(); close(r["p_two_sided"], 0.429, 0.01)
    r = s1.t39_multiple_testing(); assert (r["naive_rejections_5pct"], r["bonferroni_rejections"], r["bh_rejections"]) == (5, 1, 3)
    r = s1.t40_deflated_sharpe(); close(r["deflated_sharpe"], 0.654, 0.01); assert r["deflated_sharpe"] < 0.95
    r = s1.t41_bootstrap(); assert r["boot_se_block20"] > r["boot_se_iid"]
    r = s1.t42_bayes(); close(r["posterior_mean"], 0.00013043, 1e-7)
    r = s1.t43_mle(); close(r["var_mle"], 4.0, 1e-9); close(r["var_unbiased"], 32 / 7, 1e-9)
    r = s1.t44_sharpe_ci(); close(r["se_annual_iid"], 0.4477, 0.001)
    r = s1.t45_autocorr(); assert r["ljung_box_Q5"] > r["chi2_5pct_crit_df5"]
    r = s1.t46_stationarity(); assert r["reject_unit_root_random_walk"] < 0.10 and r["reject_unit_root_AR(0.5)"] > 0.95
    r = s1.t47_cointegration(); assert r["EG_reject_independent_RWs"] < 0.08 and r["EG_reject_when_cointegrated"] > 0.95
    r = s1.t51_vol_models(); close(r["ewma_vol_pct"], 1.0863, 0.001); close(r["garch_var_next"], 1.24e-4, 1e-9)
    r = s1.t53_kalman(); assert r["rmse_kalman_Q=0.0001"] < r["rmse_kalman_Q=1e-06"]
    r = s1.t54_evt(); assert 0.045 < r["VaR99.9_gpd"] < 0.06 and r["VaR99.9_normal"] < 0.035
    r = s1.t56_survival(); close(r["km_steps (t, at_risk, events, S)"][-1][3], 0.2, 1e-9)

    r = s2.t57_reality_check(); assert r["reality_check_p"] > 0.05 > r["naive_p_best"]
    r = s2.t58_lo_and_mintrl(); close(r["min_track_record_years"], 2.81, 0.02)
    r = s2.t59_ergodicity(); close(r["time_average_growth_per_round"], math.sqrt(0.9) - 1, 1e-9)
    r = s2.t60_granger(); assert r["F_x_causes_y"] > 3.01 > r["F_y_causes_x"]
    r = s2.t64_filter_lookahead(); assert abs(r["corr(EMA_slope, next_return)"]) < 0.02 < r["corr(centered_slope, next_return)"]
    r = s2.t65_effective_sample_size(); close(r["inflation_factor_sqrt"], r["theory_sqrt_factor"], 0.15)

    r = s3.t66_pca(); close(sum(r["eigenvalues"]), 3.0, 1e-3)
    r = s3.t67_covariance_shrinkage(); assert r["avg_realized_daily_vol_shrunk_minvar_pct"] < r["avg_realized_daily_vol_sample_minvar_pct"]
    r = s3.t69_optimization(); assert min(r["unconstrained_weights"]) < 0 and min(r["long_only_weights"]) >= 0
    r = s3.t72_monte_carlo_option(); close(r["mc_antithetic"], r["black_scholes"], 4 * r["mc_antithetic_se"])
    r = s3.t75_game_theory(); close(r["P(MM quotes Tight)"], 0.25, 1e-9); close(r["P(informed Trades)"], 1 / 3, 1e-9)
    r = s3.t76_dynamic_programming(); assert r["lambda=0.0"]["schedule"] == [2, 2, 2, 2, 2]
    r = s3.t78_fractional_differentiation(); assert not r["results"]["d=0.0"]["passes_5pct"] and r["results"]["d=0.2"]["passes_5pct"]
    print("all Part 2 checks passed")


if __name__ == "__main__":
    main()
