# Part 15. Performance and Analytics: Micro Details (topics 641 to 759)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 15.1 Return measurement fundamentals

641. Simple vs. log returns, and when each is valid (aggregation across time vs. across assets)
     - Covers: choice of return definition.
     - Details: log returns add across time, simple returns add across assets in a portfolio. r_log = ln(P_t / P_{t-1}).
     - Pitfall: averaging simple returns across time and calling it compound growth.
     - Build: conversion helpers and tests that aggregate each way.

642. Compounding, geometric vs. arithmetic mean, and volatility drag
     - Covers: long-run growth.
     - Details: geometric mean is approx arithmetic mean - sigma^2 / 2. Higher volatility lowers compound growth for the same average.
     - Pitfall: quoting arithmetic average returns as expected growth.
     - Build: simulation showing the gap between arithmetic and geometric means.

643. Annualization conventions (252 vs. 365, calendar vs. trading days, irregular sampling)
     - Covers: scaling statistics to a year.
     - Details: annualized volatility = daily std x sqrt(252). Use the right number of periods for the sampling frequency and market.
     - Pitfall: using 365 for daily trading returns or ignoring irregular gaps.
     - Build: a single annualization function used across the codebase.

644. Time-weighted return (TWR) vs. money-weighted return (MWR/IRR)
     - Covers: flow-adjusted performance.
     - Details: TWR chains sub-period returns between cash flows and measures manager skill. MWR solves for the IRR and reflects investor timing.
     - Pitfall: comparing a TWR to an MWR.
     - Build: both calculations on one account with deposits and withdrawals.

645. Handling cash flows, deposits, and withdrawals in return calculation
     - Covers: flows in performance.
     - Details: value the account right before each flow and chain the sub-period returns.
     - Pitfall: counting a deposit as profit.
     - Build: a daily valuation series with flow adjustments and tests.

646. Gross vs. net returns (before and after costs, fees, and taxes)
     - Covers: reporting levels.
     - Details: label every figure as gross or net. Net includes commissions, slippage, financing, management and performance fees, and taxes where relevant.
     - Pitfall: mixing gross strategy returns with net benchmark returns.
     - Build: a waterfall from gross to net with each cost layer shown.

647. Mark-to-market vs. realized P&L, and unrealized P&L treatment
     - Covers: P&L definitions.
     - Details: realized P&L arises on closing, unrealized on open positions marked at current price. Total = realized + unrealized.
     - Pitfall: reporting only realized P&L and hiding open losses.
     - Build: P&L report splitting realized and unrealized by position.

648. Intraday vs. end-of-day P&L, and valuation price choice (last, mid, settlement, VWAP)
     - Covers: which price values positions.
     - Details: last price can be stale, mid avoids bounce, settlement price is used for futures margin.
     - Pitfall: inconsistent valuation between risk and accounting.
     - Build: documented valuation policy per instrument type.

649. Handling stale prices and illiquid-asset valuation
     - Covers: thin or untraded instruments.
     - Details: use last price with age flags, model-based valuation, or conservative haircuts.
     - Pitfall: smooth returns caused by stale pricing, which understate volatility.
     - Build: staleness flag and valuation fallback rules.

650. Multi-currency returns (local vs. base currency, FX contribution)
     - Covers: currency effects.
     - Details: base return = (1 + local return)(1 + FX return) - 1.
     - Pitfall: ignoring hedge costs and FX contribution.
     - Build: return decomposition into local and FX parts.

651. Return decomposition (price, carry, dividend, financing, FX)
     - Covers: sources of return.
     - Details: total return splits into price change, income, financing, and currency.
     - Pitfall: attributing carry income to skill.
     - Build: decomposition table per instrument type.

652. Leverage-adjusted and notional vs. capital-based return denominators
     - Covers: choice of denominator.
     - Details: return on notional, on capital, and on margin differ greatly for leveraged strategies.
     - Pitfall: quoting return on margin without stating it.
     - Build: all three reported side by side.

653. Return on margin vs. return on capital vs. return on risk
     - Covers: alternative return bases.
     - Details: return on risk divides by a risk measure such as volatility or maximum drawdown.
     - Pitfall: using inconsistent bases across strategies.
     - Build: a standard report that states the base explicitly.

## 15.2 Risk-adjusted performance metrics

654. Sharpe ratio and its assumptions (normality, i.i.d., stationarity)
     - Covers: excess return per unit of volatility.
     - Details: SR = (mean return - risk-free) / std. Annualize by sqrt(periods) only under i.i.d. returns.
     - Pitfall: ignoring skew, kurtosis, and autocorrelation.
     - Build: Sharpe with confidence interval and non-normality adjustments.

655. Sortino ratio and the choice of minimum acceptable return
     - Covers: downside-only risk.
     - Details: Sortino = (mean - MAR) / downside deviation. MAR choice changes the ranking.
     - Pitfall: different downside-deviation definitions.
     - Build: Sortino at several MARs.

656. Calmar, Sterling, and Burke ratios
     - Covers: drawdown-based ratios.
     - Details: Calmar = annualized return / maximum drawdown. Sterling and Burke use average or squared drawdowns.
     - Pitfall: unstable ratios over short periods with one large drawdown.
     - Build: rolling Calmar with a stated window.

657. Information ratio and tracking error
     - Covers: active performance.
     - Details: IR = annualized active return / annualized tracking error.
     - Pitfall: wrong benchmark.
     - Build: IR against several benchmarks.

658. Treynor ratio and Jensen's alpha
     - Covers: CAPM-based measures.
     - Details: Treynor = excess return / beta. Jensen's alpha is intercept of the excess-return regression.
     - Pitfall: unstable beta estimates.
     - Build: alpha and beta with standard errors.

659. Omega ratio and Kappa ratios
     - Covers: distribution-based ratios.
     - Details: Omega = gains above a threshold / losses below it. Kappa generalizes to higher lower-partial moments.
     - Pitfall: sensitivity to threshold.
     - Build: Omega curve across thresholds.

660. Ulcer Index, Martin ratio, and pain ratio
     - Covers: drawdown depth and duration.
     - Details: Ulcer Index = sqrt(mean of squared percentage drawdowns). Martin ratio = excess return / Ulcer Index.
     - Pitfall: drawdown measure depends on the starting point.
     - Build: Ulcer Index from the equity curve.

661. Tail ratio, gain-to-pain ratio, and profit factor
     - Covers: simple payoff measures.
     - Details: tail ratio = 95th percentile / |5th percentile|. Profit factor = gross profit / gross loss.
     - Pitfall: profit factor ignores sizing and timing.
     - Build: report with all three and sample size.

662. Higher-moment-adjusted metrics (skew and kurtosis-aware)
     - Covers: adjusting for non-normality.
     - Details: adjusted Sharpe or Cornish-Fisher VaR incorporate skew and kurtosis.
     - Pitfall: unreliable higher-moment estimates in short samples.
     - Build: adjusted metrics with bootstrap intervals.

663. Risk-adjusted metric disagreement: why rankings change across metrics
     - Covers: metric choice effects.
     - Details: strategies with negative skew look good on Sharpe but poor on drawdown measures.
     - Pitfall: picking the metric that favors your strategy.
     - Build: rank table across metrics for several strategies.

664. Metric gaming: how each metric can be inflated (selling tails, smoothing, short track records)
     - Covers: manipulation of metrics.
     - Details: selling options, smoothing returns, or showing only favorable windows boosts ratios.
     - Pitfall: trusting any single ratio.
     - Build: a checklist of manipulation tests (skew, autocorrelation, track length).

## 15.3 Drawdown and path analysis

665. Maximum drawdown, average drawdown, and drawdown duration
     - Covers: loss from peak.
     - Details: drawdown_t = equity_t / running max - 1. Report depth, duration, and time to recover.
     - Pitfall: using closing equity only and missing intraday drawdown.
     - Build: drawdown table of the top five episodes.

666. Time to recovery and underwater curves
     - Covers: how long to recover.
     - Details: underwater plot shows drawdown over time. Recovery time matters more psychologically and financially.
     - Pitfall: ignoring unrecovered drawdowns at the end of the sample.
     - Build: underwater chart and recovery stats.

667. Drawdown distribution via Monte Carlo and bootstrap
     - Covers: possible drawdowns.
     - Details: resample returns or trades to get a distribution of maximum drawdown.
     - Pitfall: i.i.d. resampling that underestimates clustering.
     - Build: block-bootstrap drawdown percentiles.

668. Expected maximum drawdown under different return models
     - Covers: theory of drawdown.
     - Details: expected maximum drawdown grows with volatility and horizon, and shrinks with higher Sharpe.
     - Pitfall: using a short sample to judge long-horizon drawdowns.
     - Build: simulation of expected drawdown versus Sharpe and horizon.

669. Drawdown clustering and conditional drawdown
     - Covers: drawdown timing.
     - Details: losses cluster in time, so expect sequences of bad periods.
     - Pitfall: assuming independent bad days.
     - Build: drawdown clustering test.

670. Equity-curve smoothness and linearity (R-squared of the equity curve)
     - Covers: curve quality.
     - Details: R-squared of log equity versus time shows consistency of growth.
     - Pitfall: smoothness from illiquid valuation.
     - Build: log-equity regression statistics.

671. Rolling windows (rolling Sharpe, volatility, drawdown, beta)
     - Covers: time-varying metrics.
     - Details: choose window length relative to the strategy's horizon.
     - Pitfall: overlapping windows that look more significant than they are.
     - Build: rolling metrics dashboard.

672. Path dependence and order-of-returns risk
     - Covers: sequence effects.
     - Details: with withdrawals or leverage, early losses hurt far more than later ones.
     - Pitfall: judging only the average return.
     - Build: simulation with different return orderings.

## 15.4 Trade-level analytics

673. Win rate, average win/loss, payoff ratio, and expectancy
     - Covers: trade statistics.
     - Details: expectancy = win rate x average win - loss rate x average loss. Payoff ratio = average win / average loss.
     - Pitfall: high win rate with a few large losses.
     - Build: expectancy table with confidence intervals.

674. Trade distribution (histograms, outlier dependence, fat-tail contribution)
     - Covers: shape of trade results.
     - Details: look at skew, tails, and dependence on outliers.
     - Pitfall: average profit driven by a few trades.
     - Build: histogram and percent of profit from the top trades.

675. Reliance on top-N trades (what the P&L looks like without the best 5 trades)
     - Covers: concentration of profits.
     - Details: remove the best few trades and recompute results.
     - Pitfall: strategies that need rare lucky trades.
     - Build: P&L with top trades excluded.

676. MAE/MFE analysis and exit-efficiency analysis
     - Covers: trade path quality.
     - Details: maximum adverse excursion shows how far trades went against you, maximum favorable excursion shows unrealized gain.
     - Pitfall: stops tuned from MAE without out-of-sample checks.
     - Build: MAE/MFE scatter and exit-efficiency stat.

677. Holding-period analysis and time-in-market
     - Covers: durations.
     - Details: returns by holding time show where edge lies, and time in market affects capital use.
     - Pitfall: ignoring capital tied up in long trades.
     - Build: return per day of capital use.

678. Streak analysis (consecutive wins/losses) and serial dependence of trades
     - Covers: sequence behavior.
     - Details: test whether wins and losses cluster more than chance.
     - Pitfall: seeing patterns in randomness.
     - Build: runs test on trade outcomes.

679. Trade clustering by time of day, weekday, month, and event
     - Covers: timing analysis.
     - Details: results grouped by time features, with significance tests.
     - Pitfall: finding patterns by slicing many ways.
     - Build: grouped results with multiple-testing adjustment.

680. Entry and exit timing quality (edge ratio, entry efficiency)
     - Covers: timing skill.
     - Details: compare entry and exit prices with the best available within the trade window.
     - Pitfall: hindsight-based interpretation.
     - Build: efficiency metrics per trade.

681. Slippage per trade and fill-quality statistics
     - Covers: execution cost.
     - Details: difference between decision price and fill price.
     - Pitfall: measuring against a non-tradable benchmark.
     - Build: slippage distribution by size and time.

682. Long vs. short side contribution and asymmetry
     - Covers: side attribution.
     - Details: separate long and short performance and risk.
     - Pitfall: short side relying on a bull market hedge.
     - Build: side-by-side performance.

683. Per-instrument, per-sector, and per-strategy contribution
     - Covers: sources of P&L.
     - Details: contribution = P&L divided by total P&L.
     - Pitfall: ignoring that many small instruments hide concentration risk.
     - Build: contribution table with concentration measure.

684. Turnover and trade frequency vs. net return relationship
     - Covers: cost drag.
     - Details: higher turnover requires higher gross edge per trade.
     - Pitfall: cost assumptions that do not scale with turnover.
     - Build: net return as a function of turnover.

## 15.5 Performance attribution

685. Brinson attribution (allocation, selection, interaction)
     - Covers: benchmark-relative attribution.
     - Details: allocation effect from over- or underweights, selection from stock choice within segments, and interaction.
     - Pitfall: inconsistent sector definitions.
     - Build: Brinson-Fachler table for a portfolio versus benchmark.

686. Factor-based attribution (market, size, value, momentum, quality, low-vol)
     - Covers: explaining returns by factors.
     - Details: regress returns on factor returns and attribute to loadings times factor returns.
     - Pitfall: unstable loadings.
     - Build: factor attribution report over time.

687. Alpha vs. beta decomposition and residual alpha significance
     - Covers: skill versus exposure.
     - Details: beta return from market exposure, alpha is residual. Test with robust standard errors.
     - Pitfall: calling beta exposure alpha.
     - Build: regression-based decomposition with t-stats.

688. Strategy-level and signal-level attribution
     - Covers: which strategy or signal contributes.
     - Details: tag trades by signal and aggregate P&L.
     - Pitfall: trades with multiple signals double counted.
     - Build: signal tags and attribution rules.

689. Risk-contribution attribution (marginal and component risk)
     - Covers: sources of risk.
     - Details: component risk of a position = weight x marginal risk contribution.
     - Pitfall: confusing capital and risk contribution.
     - Build: risk-contribution table.

690. Timing vs. selection vs. sizing attribution
     - Covers: skill components.
     - Details: compare actual with versions using equal sizing or random timing.
     - Pitfall: assuming skill without these comparisons.
     - Build: counterfactual comparisons.

691. Carry, roll, and convexity attribution for futures and options
     - Covers: derivative-specific returns.
     - Details: futures return splits into spot change and roll yield.
     - Pitfall: treating roll yield as alpha.
     - Build: futures return decomposition.

692. Greeks-based P&L attribution for options (delta, gamma, vega, theta, and unexplained residual)
     - Covers: option P&L explanation.
     - Details: P&L approx = delta dS + 0.5 gamma dS^2 + vega dVol + theta dt + residual.
     - Pitfall: large unexplained residual hides model or data errors.
     - Build: daily Greek P&L explain with residual alert.

693. Cost attribution (commissions, spread, impact, financing, taxes)
     - Covers: cost sources.
     - Details: break total costs into components.
     - Pitfall: only tracking commissions.
     - Build: cost waterfall per period.

694. Regime-conditional attribution (performance by volatility, trend, and macro regime)
     - Covers: when the strategy earns.
     - Details: group P&L by regime classified without look-ahead.
     - Pitfall: regimes defined with future information.
     - Build: regime table.

695. Attribution across multi-currency books
     - Covers: currency complexity.
     - Details: attribute local return, FX, and hedge P&L separately.
     - Pitfall: double counting FX.
     - Build: multi-currency attribution test with known answers.

696. Reconciling attribution to actual P&L (the unexplained residual and what it signals)
     - Covers: completeness.
     - Details: sum of components should equal total P&L within tolerance.
     - Pitfall: a growing residual signals data or logic errors.
     - Build: residual tracking with thresholds.

## 15.6 Benchmarking and comparison

697. Benchmark selection (market, peer, risk-matched, custom blended)
     - Covers: choosing a benchmark.
     - Details: benchmark should match investable universe and risk.
     - Pitfall: easy benchmark that flatters performance.
     - Build: documented benchmark rationale.

698. Beta-adjusted and style-adjusted benchmarks
     - Covers: fair comparison.
     - Details: scale benchmark to your beta or style.
     - Pitfall: ignoring exposure differences.
     - Build: beta-adjusted benchmark returns.

699. Correlation to benchmarks, strategies, and common risk factors
     - Covers: independence.
     - Details: low correlation with known risk sources shows diversification.
     - Pitfall: correlation measured in calm periods only.
     - Build: correlation matrix with stress periods.

700. Up-capture and down-capture ratios
     - Covers: asymmetry versus the benchmark.
     - Details: capture ratio = strategy return / benchmark return in up (or down) periods.
     - Pitfall: ratio depends on period definition.
     - Build: capture ratios by month.

701. Peer-group and universe comparison
     - Covers: relative ranking.
     - Details: compare with similar strategies and share-class fees.
     - Pitfall: survivorship in peer databases.
     - Build: percentile ranks.

702. Replication and naive-baseline comparison (does the strategy beat buy-and-hold, equal-weight, or a simple trend rule?)
     - Covers: sanity tests.
     - Details: complex strategies must beat simple ones net of costs.
     - Pitfall: not testing baselines.
     - Build: baseline comparison table.

703. Hurdle rates, risk-free rate selection, and cash comparison
     - Covers: minimum acceptable return.
     - Details: pick a risk-free proxy matching the currency and horizon.
     - Pitfall: using zero risk-free rate in a high-rate period.
     - Build: documented risk-free series.

## 15.7 Live monitoring and degradation detection

704. Live vs. backtest vs. paper tracking-error dashboards
     - Covers: expectations versus reality.
     - Details: compare live results to backtest and paper on the same period.
     - Pitfall: ignoring persistent differences.
     - Build: tracking-error chart and analysis.

705. Expected-vs-realized distribution tests (is the live drawdown within the backtest envelope?)
     - Covers: statistical consistency.
     - Details: compare live metrics to simulated distribution.
     - Pitfall: no rule for when to act.
     - Build: percentile of live outcome in simulation.

706. Change-point detection on strategy returns (CUSUM, Bayesian)
     - Covers: detecting shifts.
     - Details: CUSUM accumulates deviations from expected return and flags a regime change.
     - Pitfall: false alarms.
     - Build: CUSUM with tuned threshold.

707. Alpha-decay monitoring, half-life estimation, and alpha capture
     - Covers: edge erosion.
     - Details: track information coefficient over time and fit a decay curve.
     - Pitfall: confusing temporary underperformance with decay.
     - Build: rolling IC with trend test.

708. Execution-quality drift (slippage, fill rate, reject rate over time)
     - Covers: execution degradation.
     - Details: time series of execution metrics with alerts.
     - Pitfall: unnoticed rising costs.
     - Build: weekly execution quality report.

709. Model and signal drift metrics (feature distribution shift, PSI, KS tests)
     - Covers: input drift.
     - Details: Population Stability Index and Kolmogorov-Smirnov test compare live features with training.
     - Pitfall: tests too sensitive with large samples.
     - Build: drift dashboard with thresholds.

710. Hit-rate and information-coefficient (IC) decay tracking
     - Covers: predictive quality.
     - Details: track IC by period and its confidence interval.
     - Pitfall: noisy short windows.
     - Build: IC time series with intervals.

711. Automated strategy health scores and traffic-light rules
     - Covers: summary status.
     - Details: combine metrics into green, amber, red with documented thresholds.
     - Pitfall: unclear actions per color.
     - Build: health score and action table.

712. Strategy retirement and throttling criteria based on analytics
     - Covers: stopping rules.
     - Details: predefined conditions to reduce size or stop.
     - Pitfall: ad hoc decisions after losses.
     - Build: documented retirement criteria.

713. Alert thresholds and false-alarm control
     - Covers: alert quality.
     - Details: tune thresholds for acceptable false-alarm rate.
     - Pitfall: alert fatigue.
     - Build: alert review process.

## 15.8 Execution and cost analytics (TCA)

714. Implementation shortfall decomposition
     - Covers: total cost of implementation.
     - Details: shortfall = paper return - actual return, split into delay, impact, and opportunity cost.
     - Pitfall: no decision-price timestamps.
     - Build: shortfall decomposition per order.

715. Arrival-price, VWAP, TWAP, and close benchmarks
     - Covers: comparison prices.
     - Details: arrival price is the mid at decision time. VWAP benchmarks the day.
     - Pitfall: gaming VWAP benchmarks.
     - Build: multiple benchmarks per order.

716. Spread capture, adverse selection, and markout analysis
     - Covers: fill quality.
     - Details: markout = price some time after fill versus fill price.
     - Pitfall: ignoring adverse selection on passive fills.
     - Build: markout curves.

717. Market-impact estimation from own trades
     - Covers: empirical impact.
     - Details: regress slippage on participation rate.
     - Pitfall: small sample sizes.
     - Build: impact model with intervals.

718. Fill-rate, passive vs. aggressive mix, and venue analysis
     - Covers: execution style.
     - Details: fill probability and cost by style and venue.
     - Pitfall: judging passive orders only on filled ones.
     - Build: fill-rate table including unfilled orders.

719. Broker and algo comparison
     - Covers: choosing providers.
     - Details: compare matched order samples.
     - Pitfall: unmatched samples.
     - Build: matched-sample comparison method.

720. Latency analytics (signal-to-order, order-to-ack, ack-to-fill)
     - Covers: timing stages.
     - Details: stage latencies with percentiles.
     - Pitfall: clock mismatch.
     - Build: latency histogram per stage.

721. Opportunity cost and unfilled-order analysis
     - Covers: missed trades.
     - Details: value of orders that did not fill.
     - Pitfall: ignoring cost of missed alpha.
     - Build: unfilled-order report.

722. Pre-trade cost estimates vs. realized cost reconciliation
     - Covers: model validation.
     - Details: compare predicted and actual costs.
     - Pitfall: persistent bias.
     - Build: bias and error report.

## 15.9 Portfolio-level analytics

723. Exposure analytics (gross, net, long, short, beta-adjusted, sector, country, currency)
     - Covers: exposure views.
     - Details: gross = long + |short|, net = long - |short|.
     - Pitfall: missing indirect exposures.
     - Build: exposure dashboard.

724. Concentration metrics (top-N weights, Herfindahl index, effective number of bets)
     - Covers: concentration.
     - Details: HHI = sum of squared weights, effective names = 1 / HHI.
     - Pitfall: ignoring correlation.
     - Build: concentration report.

725. Correlation structure and diversification ratio over time
     - Covers: diversification.
     - Details: diversification ratio = weighted average volatility / portfolio volatility.
     - Pitfall: unstable correlation estimates.
     - Build: rolling diversification ratio.

726. Risk decomposition (systematic vs. idiosyncratic, factor risk)
     - Covers: risk sources.
     - Details: total variance = factor variance + specific variance.
     - Pitfall: omitted factors.
     - Build: variance decomposition.

727. Liquidity profile (days to liquidate, ADV participation)
     - Covers: exit capacity.
     - Details: days to liquidate = position / (participation x ADV).
     - Pitfall: using average volume in stress.
     - Build: liquidity ladder.

728. Leverage, margin utilization, and buying-power history
     - Covers: capital usage.
     - Details: track leverage and margin over time.
     - Pitfall: surprise margin calls.
     - Build: margin utilization chart.

729. Turnover, holding-period, and capacity analytics
     - Covers: trading intensity.
     - Details: turnover = traded value / average capital.
     - Pitfall: ignoring costs scale.
     - Build: turnover and cost report.

730. Greeks and scenario exposure dashboards for derivative books
     - Covers: option-book view.
     - Details: aggregate Greeks and scenario grids.
     - Pitfall: missing correlations among underlyings.
     - Build: Greeks and shock dashboard.

731. Realized vs. forecast volatility and risk-model calibration checks
     - Covers: model accuracy.
     - Details: compare predicted risk with realized.
     - Pitfall: persistent underprediction.
     - Build: bias statistics.

732. VaR and Expected Shortfall exceedance reporting
     - Covers: backtesting risk.
     - Details: count exceedances and test frequency.
     - Pitfall: ignoring clustering.
     - Build: exceedance chart and tests.

## 15.10 Signal and model analytics

733. Information coefficient (IC), rank IC, and IC information ratio
     - Covers: predictive power.
     - Details: IC = correlation between signal and forward return. Rank IC uses ranks. IC IR = mean IC / std IC.
     - Pitfall: overlapping forward returns inflate significance.
     - Build: IC time series with confidence bands.

734. Quantile (decile) return analysis and monotonicity checks
     - Covers: signal shape.
     - Details: average forward return by signal decile, checking monotonic pattern.
     - Pitfall: non-monotonic effects hidden by averages.
     - Build: decile bar chart and spread.

735. Signal turnover, autocorrelation, and decay curves
     - Covers: signal dynamics.
     - Details: autocorrelation shows persistence and implies turnover.
     - Pitfall: high-turnover signals with small edge.
     - Build: decay curve and turnover estimate.

736. Signal correlation matrix and marginal contribution to the blend
     - Covers: signal overlap.
     - Details: add-one and drop-one analyses.
     - Pitfall: redundant signals.
     - Build: correlation and marginal-contribution table.

737. Feature importance stability over time
     - Covers: model understanding.
     - Details: rankings should be stable across folds.
     - Pitfall: unstable importance indicates noise.
     - Build: importance rank stability chart.

738. Prediction calibration and reliability diagrams
     - Covers: probability quality.
     - Details: predicted versus observed frequencies.
     - Pitfall: miscalibration misleads sizing.
     - Build: reliability diagram.

739. Hit rate vs. magnitude accuracy (directional vs. sizing quality)
     - Covers: types of accuracy.
     - Details: direction hit rate and magnitude error measure different skills.
     - Pitfall: high hit rate with small gains.
     - Build: both metrics reported.

740. Error analysis (when and where does the model fail)
     - Covers: failure analysis.
     - Details: group errors by regime, instrument, and time.
     - Pitfall: ignoring systematic failure pockets.
     - Build: error breakdown table.

741. Ablation studies and incremental-value tests
     - Covers: component value.
     - Details: remove each component and measure impact.
     - Pitfall: only testing the full model.
     - Build: ablation table.

## 15.11 Reporting and communication

742. Tear sheets (standard one-page strategy and portfolio summaries)
     - Covers: summary reports.
     - Details: key metrics, equity curve, drawdowns, monthly returns, exposures.
     - Pitfall: inconsistent definitions across reports.
     - Build: tear-sheet template.

743. Daily, weekly, and monthly reporting cadences and content
     - Covers: report schedule.
     - Details: daily operations and risk, weekly performance, monthly investor.
     - Pitfall: unclear audience.
     - Build: report calendar.

744. Investor, board, and risk-committee reports
     - Covers: audience tailoring.
     - Details: different depth and metrics per audience.
     - Pitfall: overloading with numbers.
     - Build: audience templates.

745. Regulatory and audit reporting packs
     - Covers: compliance reporting.
     - Details: required fields, retention, and evidence.
     - Pitfall: missing records.
     - Build: audit-ready export.

746. Honest-disclosure standards (GIPS-style composites, hypothetical vs. live labeling)
     - Covers: transparent reporting.
     - Details: label backtested or hypothetical results clearly and include costs.
     - Pitfall: presenting backtests as live.
     - Build: disclosure language and labeling rules.

747. Visualization best practices (equity curve on log scale, underwater plots, heatmaps, return histograms)
     - Covers: charts.
     - Details: log scale for long histories, consistent colors, labeled axes.
     - Pitfall: misleading scales.
     - Build: chart style guide.

748. Interactive drill-down dashboards (portfolio to strategy to trade to fill)
     - Covers: exploration.
     - Details: click from summary to trade-level detail.
     - Pitfall: slow queries.
     - Build: drill-down dashboard.

749. Narrative commentary: explaining why performance happened, not just what
     - Covers: explanation.
     - Details: link results to market events and drivers.
     - Pitfall: post-hoc stories.
     - Build: commentary template.

750. Report reproducibility, versioning, and traceability to source data
     - Covers: traceable reports.
     - Details: version code and data used for each report.
     - Pitfall: irreproducible numbers.
     - Build: report metadata.

751. Tax-lot and tax-aware performance reporting
     - Covers: tax view.
     - Details: lot selection methods and wash-sale rules.
     - Pitfall: ignoring tax drag.
     - Build: lot-level tax report.

## 15.12 Analytics infrastructure

752. Analytics data model (fills, orders, positions, P&L, prices, reference data)
     - Covers: schema.
     - Details: normalized tables with consistent keys and timestamps.
     - Pitfall: ad hoc tables.
     - Build: documented schema.

753. Point-in-time P&L engine and position reconstruction
     - Covers: rebuilding history.
     - Details: reconstruct positions and P&L at any time from event logs.
     - Pitfall: overwritten history.
     - Build: event-sourced P&L engine.

754. Reconciliation of analytics with broker and exchange records
     - Covers: verification.
     - Details: compare calculated P&L and positions with statements.
     - Pitfall: ignoring small breaks.
     - Build: daily reconciliation.

755. Metric definition registry (one agreed definition per metric across the firm)
     - Covers: consistency.
     - Details: central definitions with code references.
     - Pitfall: multiple Sharpe definitions.
     - Build: registry document and library.

756. Batch vs. streaming analytics pipelines
     - Covers: processing modes.
     - Details: streaming for live monitoring, batch for deep analysis.
     - Pitfall: inconsistent results between modes.
     - Build: shared computation code.

757. Data lineage and audit trail for every reported number
     - Covers: traceability.
     - Details: record inputs, code version, and time of each metric.
     - Pitfall: no way to explain a number.
     - Build: lineage metadata.

758. Performance-calculation unit testing and golden-dataset validation
     - Covers: correctness.
     - Details: test against hand-computed datasets.
     - Pitfall: untested edge cases such as zero returns or flows.
     - Build: golden tests.

759. Analytics library selection and its pitfalls (differing Sharpe or drawdown conventions across libraries)
     - Covers: third-party libraries.
     - Details: conventions for annualization, risk-free rate, and drawdown differ.
     - Pitfall: unexamined library defaults.
     - Build: library comparison on a known dataset.
