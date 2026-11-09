# Part 12. Risk Management: Micro Details (topics 497 to 519)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

Worked examples, formulas, and runnable code for every topic here are in [course/part-12-risk-management](../course/part-12-risk-management/README.md).

## 12.1 Pre-trade and real-time controls

497. Pre-trade checks (position, exposure, fat-finger limits)
     - Covers: blocking bad orders before they leave.
     - Details: checks on order size, notional, price versus last or mid, position and exposure limits, and order rate. Failure returns a specific rejection reason.
     - Pitfall: checks applied only in some code paths.
     - Build: a single risk gate that every order must pass, with tests per rule.

498. Real-time P&L and exposure monitoring
     - Covers: live risk view.
     - Details: mark positions to current prices, show P&L by strategy, exposure by instrument and factor, and limit utilization.
     - Pitfall: stale prices or missing positions.
     - Build: a monitor with staleness flags and alert thresholds.

499. Kill switches and circuit breakers
     - Covers: emergency stops.
     - Details: manual and automatic triggers (loss limit, error rate, rejection rate, position mismatch) that halt new orders, cancel open orders, and optionally flatten.
     - Pitfall: a switch that depends on the same component that failed.
     - Build: tested kill switch at the strategy, account, and gateway levels.

## 12.2 Risk measures, stress testing, and exposures

500. VaR methods (historical, parametric, Monte Carlo) and VaR backtesting (Kupiec, Christoffersen)
     - Covers: loss quantile estimates.
     - Details: historical uses past returns, parametric uses a distribution, Monte Carlo simulates scenarios. Kupiec tests exceedance frequency, Christoffersen tests clustering.
     - Pitfall: VaR says nothing about losses beyond the threshold.
     - Build: VaR with daily exceedance tracking and statistical tests.

501. Expected Shortfall
     - Covers: average loss in the tail.
     - Details: ES at 97.5% is the mean loss beyond the 97.5% VaR. It is coherent and captures tail severity.
     - Pitfall: noisy estimates from few tail observations.
     - Build: ES from historical and fitted-tail models.

502. Scenario analysis and historical stress tests
     - Covers: what-if losses.
     - Details: apply past crisis shocks and hypothetical moves (price, volatility, correlation, spread) to current positions.
     - Pitfall: scenarios that omit simultaneous volatility and liquidity shocks.
     - Build: scenario library and a one-click portfolio revaluation.

503. Reverse stress testing
     - Covers: find what breaks you.
     - Details: start from a loss threshold and search for scenarios that cause it.
     - Pitfall: only considering plausible-looking scenarios.
     - Build: an optimizer finding the smallest shock vector leading to a defined loss.

504. Drawdown control and loss-limit rules
     - Covers: loss limits.
     - Details: daily, weekly, and peak-to-trough limits with actions at each level (reduce, pause, review).
     - Pitfall: limits without a defined restart process.
     - Build: tiered limit rules and automated actions.

505. Correlation breakdown and tail risk
     - Covers: dependence in stress.
     - Details: correlations rise in crises, and diversification fails when needed most.
     - Pitfall: using calm-period correlations for risk.
     - Build: stress correlation matrix and its effect on portfolio risk.

506. Liquidity risk and market-impact risk
     - Covers: inability to exit.
     - Details: days to liquidate at a participation rate, spreads in stress, and impact costs.
     - Pitfall: marking at mid when exit costs are far larger.
     - Build: liquidation-time and exit-cost report.

507. Counterparty, settlement, and exchange risk
     - Covers: failure of others.
     - Details: broker insolvency, clearing failure, exchange outages, and settlement fails.
     - Pitfall: concentrating assets with one broker.
     - Build: counterparty exposure table with limits.

508. Model risk and parameter uncertainty
     - Covers: errors from models.
     - Details: wrong model, wrong inputs, or implementation bugs. Use independent validation and parameter-uncertainty bands.
     - Pitfall: relying on one model with no challenger.
     - Build: challenger model and discrepancy monitoring.

509. Concentration and factor-exposure risk
     - Covers: hidden concentrations.
     - Details: exposure to a sector, factor, country, or single name, including indirect exposures.
     - Pitfall: many positions that are really one bet.
     - Build: exposure dashboard by factor and cluster.

510. Risk budgeting and risk attribution
     - Covers: allocating and explaining risk.
     - Details: marginal and component contribution to volatility: RC_i = w_i x (Sigma w)_i / sigma_p.
     - Pitfall: confusing capital weights with risk weights.
     - Build: risk-contribution report by position and strategy.

511. Greeks-based risk for derivatives books
     - Covers: option-book risk.
     - Details: aggregate delta, gamma, vega, theta by underlying and expiry, plus scenario P&L grids across spot and volatility.
     - Pitfall: ignoring gamma and vega changes in large moves.
     - Build: spot-vol shock grid and Greek limits.

512. Gap, overnight, and weekend risk
     - Covers: risk when you cannot trade.
     - Details: price jumps between sessions bypass stops.
     - Pitfall: stop-loss assumptions that ignore gaps.
     - Build: overnight gap distribution and a position cap using gap quantiles.

513. Operational risk and fat-finger scenarios
     - Covers: process and human errors.
     - Details: wrong size, wrong symbol, duplicate orders, stale config. Use a scenario list and controls for each.
     - Pitfall: controls that exist on paper but are untested.
     - Build: a control test calendar with evidence.

514. Risk of ruin
     - Covers: probability of unrecoverable loss.
     - Details: depends on edge, variance, and size. Simulate paths to estimate ruin probability.
     - Pitfall: assuming known edge and independence.
     - Build: simulation of ruin probability under parameter uncertainty.

## 12.3 Margin, leverage, and funding risk

515. Portfolio and margin management
     - Covers: capital usage.
     - Details: track initial and maintenance margin, excess liquidity, and projected margin under shocks.
     - Pitfall: ignoring margin changes during volatile periods.
     - Build: margin projection and automatic reduction rules.

516. SPAN and exchange margin methodology
     - Covers: exchange margin models.
     - Details: SPAN uses scenario arrays of price and volatility moves to set margin, with offsets across related contracts.
     - Pitfall: margin requirements changing at short notice.
     - Build: approximate SPAN scenarios for your key positions.

517. Cross-margining and intraday margin
     - Covers: margin offsets and timing.
     - Details: cross-margining reduces requirements for offsetting positions across products. Intraday margin may differ from overnight.
     - Pitfall: relying on intraday leverage that gets cut at close.
     - Build: overnight versus intraday margin comparison.

518. Broker insolvency and custody risk
     - Covers: asset safety.
     - Details: segregation of client assets, investor-protection schemes, and rehypothecation.
     - Pitfall: unlimited assets at a single broker.
     - Build: broker due-diligence checklist and allocation limits.

519. Funding-liquidity risk and liquidity-adjusted VaR
     - Covers: ability to finance positions.
     - Details: margin calls and funding withdrawals force sales. Liquidity-adjusted VaR adds exit cost.
     - Pitfall: treating positions as instantly liquid.
     - Build: LVaR including spread and impact over the liquidation horizon.
