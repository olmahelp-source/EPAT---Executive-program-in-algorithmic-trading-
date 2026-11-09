# Part 11. Portfolio Construction and Capital Allocation: Micro Details (topics 462 to 496)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

Worked examples, formulas, and runnable code for every topic here are in [course/part-11-portfolio-capital-allocation](../course/part-11-portfolio-capital-allocation/README.md).

## 11.1 Portfolio construction and optimization

462. Mean-variance optimization (Markowitz) and its instability
     - Covers: classic optimization.
     - Details: maximize w'mu - (lambda/2) w'Sigma w, subject to constraints. Small changes in expected returns produce large weight changes (error maximization).
     - Pitfall: extreme, concentrated weights.
     - Build: sensitivity test that perturbs inputs and measures weight changes.

463. Black-Litterman model
     - Covers: combining equilibrium returns with views.
     - Details: start from market-implied returns, blend investor views weighted by confidence, and obtain stable posterior returns.
     - Pitfall: poorly specified view uncertainty.
     - Build: a Black-Litterman implementation with two or three views.

464. Risk parity and equal risk contribution
     - Covers: allocating by risk.
     - Details: weights such that each asset contributes equally to portfolio volatility. Often needs leverage to hit return targets.
     - Pitfall: heavy bond exposure and interest-rate regime risk.
     - Build: equal-risk-contribution solver and risk-contribution report.

465. Hierarchical Risk Parity and HERC
     - Covers: clustering-based allocation.
     - Details: cluster assets by correlation distance, then allocate recursively. It avoids inverting the covariance matrix.
     - Pitfall: clustering instability.
     - Build: HRP compared with mean-variance out of sample.

466. Minimum variance and maximum diversification
     - Covers: variance-focused portfolios.
     - Details: minimum variance ignores expected returns. Maximum diversification maximizes weighted average volatility over portfolio volatility.
     - Pitfall: concentration in low-volatility sectors.
     - Build: weight caps and sector constraints.

467. CVaR and CDaR optimization
     - Covers: tail-risk objectives.
     - Details: minimize conditional value-at-risk or conditional drawdown-at-risk, solvable as linear programs from scenarios.
     - Pitfall: too few scenarios in the tail.
     - Build: CVaR optimization using historical and simulated scenarios.

468. Robust and resampled optimization
     - Covers: handling estimation error.
     - Details: robust optimization uses uncertainty sets, and resampling averages optimized portfolios over perturbed inputs.
     - Pitfall: over-conservative portfolios that hold cash-like assets.
     - Build: resampled efficient frontier.

469. Factor-based construction (CAPM, Fama-French, APT, custom factors)
     - Covers: factor exposures as the building blocks.
     - Details: target exposures to factors and control unintended ones. Estimate loadings via regression.
     - Pitfall: unstable loadings and factor definitions.
     - Build: exposure-controlled optimization with factor constraints.

470. Constraints (turnover, sector, leverage, cardinality, liquidity)
     - Covers: real-world limits.
     - Details: add constraints for turnover, position size, sector, gross and net exposure, number of names, and liquidity as a fraction of ADV.
     - Pitfall: infeasible or conflicting constraints.
     - Build: constraint set with infeasibility diagnostics.

471. Transaction-cost-aware optimization
     - Covers: including trading costs.
     - Details: add a cost penalty to the objective, such as linear spread plus quadratic impact. Trade only if benefit exceeds cost.
     - Pitfall: rebalancing every period without a cost-benefit rule.
     - Build: optimization with turnover penalty and a no-trade zone.

472. Multi-period and dynamic optimization
     - Covers: planning over time.
     - Details: account for how today's trades affect future costs and opportunities.
     - Pitfall: computational complexity and model dependence.
     - Build: a two-period model compared with myopic optimization.

473. Strategy-level allocation (portfolio of strategies)
     - Covers: allocating among strategies.
     - Details: treat each strategy's returns as an asset, estimate correlations, and allocate by risk contribution or Sharpe.
     - Pitfall: backtest correlations that understate stress correlations.
     - Build: portfolio of three strategies with stress-correlation overlay.

474. Capital allocation across asset classes and regimes
     - Covers: top-level allocation.
     - Details: strategic weights with tactical tilts based on regimes, within risk budgets.
     - Pitfall: frequent regime switching.
     - Build: regime-dependent allocation table with switching costs.

475. Rebalancing policy (calendar, threshold, tactical)
     - Covers: when to rebalance.
     - Details: calendar (monthly), threshold (drift beyond a band), or a hybrid, trading off tracking error and costs.
     - Pitfall: rebalancing into falling positions without risk limits.
     - Build: comparison of policies by cost and tracking error.

## 11.2 Position keeping and reconciliation

476. Position keeping, accounting, P&L attribution
     - Covers: books and records.
     - Details: track quantity, cost basis (FIFO, average), realized and unrealized P&L, and fees by strategy and instrument.
     - Pitfall: positions that disagree between systems.
     - Build: a position ledger with trade-level audit trail.

477. Reconciliation with broker statements
     - Covers: verifying records.
     - Details: compare positions, cash, trades, and fees to broker data daily and investigate breaks.
     - Pitfall: ignoring small persistent breaks.
     - Build: automated reconciliation with a break report and aging.

## 11.3 Factor and risk-model concepts

478. Risk models (Barra-style fundamental, statistical, and hybrid factor models)
     - Covers: covariance via factors.
     - Details: Sigma = B F B' + D, with factor exposures B, factor covariance F, and specific variance D. Reduces dimensionality and noise.
     - Pitfall: factor sets missing relevant risks.
     - Build: a simple factor risk model and variance decomposition.

479. Factor zoo problem and factor-crowding risk
     - Covers: proliferation of factors.
     - Details: hundreds of published factors, many from data mining. Crowded factors crash together.
     - Pitfall: adding factors without economic rationale.
     - Build: require a stated mechanism and out-of-sample evidence per factor.

480. Hedging (minimum-variance hedge ratio, beta, cross-hedging, basis risk)
     - Covers: reducing exposures.
     - Details: hedge ratio h = Cov(spot, hedge) / Var(hedge). Cross-hedges leave basis risk.
     - Pitfall: stale ratios during regime changes.
     - Build: rolling hedge ratio and hedge effectiveness measure.

481. Dollar-, beta-, and sector-neutral construction
     - Covers: neutralization methods.
     - Details: dollar-neutral matches long and short value, beta-neutral matches market sensitivity, sector-neutral matches industry exposure.
     - Pitfall: neutral on one dimension but exposed on others.
     - Build: a neutralization step and exposure report.

482. Tracking error, active share, and information ratio
     - Covers: benchmark-relative measures.
     - Details: tracking error is the standard deviation of active returns. Information ratio = active return / tracking error. Active share is the fraction of holdings differing from benchmark.
     - Pitfall: tracking error measured over short windows.
     - Build: monthly tracking-error report.

483. Smart beta and index methodology
     - Covers: rules-based factor indexes.
     - Details: index rules for selection, weighting, and rebalancing affect turnover and capacity.
     - Pitfall: ignoring rebalance timing effects.
     - Build: a rules-based index construction pipeline.

484. ESG integration and constraints
     - Covers: sustainability in portfolios.
     - Details: exclusions, tilts, and score constraints with data-provider differences.
     - Pitfall: inconsistent scores across providers.
     - Build: ESG constraints implemented in the optimizer with source documentation.

## 11.4 Position sizing and fund allocation

485. Fixed fractional and fixed ratio sizing
     - Covers: simple sizing rules.
     - Details: fixed fractional risks a set percentage of equity per trade. Fixed ratio increases size after fixed profit increments.
     - Pitfall: ignoring correlation among simultaneous positions.
     - Build: sizing function with simulation of drawdowns.

486. Kelly criterion, fractional Kelly, multi-asset Kelly
     - Covers: growth-optimal sizing.
     - Details: f* = (p b - q) / b for binary bets, or mu / sigma^2 for continuous. Full Kelly has large drawdowns, so half or quarter Kelly is common.
     - Pitfall: overestimating edge, which makes full Kelly dangerous.
     - Build: simulation of Kelly fractions with edge estimation error.

487. Volatility targeting and ATR-based sizing
     - Covers: size scaled to risk.
     - Details: position = target risk / (volatility x price). Equalizes risk across instruments and time.
     - Pitfall: leverage spikes when volatility is temporarily low.
     - Build: volatility-target sizing with leverage cap.

488. Risk-per-trade and stop-distance sizing
     - Covers: loss-limited sizing.
     - Details: shares = (equity x risk fraction) / (entry - stop). Ensures a stop-out costs a fixed percentage.
     - Pitfall: gap risk exceeding the stop distance.
     - Build: sizing with a gap-risk adjustment.

489. Optimal f (Vince)
     - Covers: growth-based fraction from historical trades.
     - Details: finds fraction maximizing terminal wealth from the trade history. Highly sensitive to the worst loss.
     - Pitfall: extreme drawdowns and sensitivity to the sample.
     - Build: optimal f calculation and sensitivity to dropping the worst trade.

490. Equity-curve-based sizing and anti-martingale scaling
     - Covers: sizing as a function of performance.
     - Details: increase size after gains and reduce after losses, usually through a moving average of the equity curve.
     - Pitfall: delayed reduction in sharp drawdowns.
     - Build: equity-curve filter compared to constant sizing.

491. Capital allocation across strategies (static, dynamic, performance-weighted)
     - Covers: allocating capital to strategies.
     - Details: static weights are stable, performance-weighted chase recent returns.
     - Pitfall: performance chasing amplifies drawdowns.
     - Build: allocation rule comparison with turnover.

492. Cash and margin buffer policy
     - Covers: liquidity reserves.
     - Details: hold a buffer for margin changes, drawdowns, and withdrawals.
     - Pitfall: using all available margin.
     - Build: policy specifying minimum free margin and automatic de-risking trigger.

493. Pyramiding, scaling in and out
     - Covers: adding or reducing positions.
     - Details: scale in on confirmation, scale out at targets. Total risk should stay within limits.
     - Pitfall: pyramiding into rising risk.
     - Build: rule-based scale-in with aggregate stop.

494. Leverage policy and margin-call avoidance
     - Covers: leverage control.
     - Details: set maximum gross and net leverage and stress margin under gap moves.
     - Pitfall: leverage based on average, not peak, margin needs.
     - Build: margin stress test under shocked prices.

495. Drawdown-dependent de-risking
     - Covers: reducing risk as losses grow.
     - Details: scale down exposure at defined drawdown levels, with rules for re-entry.
     - Pitfall: de-risking at the bottom, locking in losses.
     - Build: drawdown ladder tested in simulation.

496. Fund-level mechanics (subscriptions, redemptions, NAV, fees, high-water mark)
     - Covers: pooled-capital operations.
     - Details: NAV per unit, equalization for fee fairness, performance fee only above the high-water mark, redemption notice periods.
     - Pitfall: fee calculation errors and liquidity mismatch with redemption terms.
     - Build: NAV and fee calculator with high-water mark tests.
