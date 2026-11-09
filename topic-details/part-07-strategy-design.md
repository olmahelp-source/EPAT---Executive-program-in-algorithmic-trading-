# Part 7. Strategy Design: Micro Details (topics 314 to 354)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 7.1 Strategy families

314. Trend following and CTA-style systems
     - Covers: systematic trend capture across markets.
     - Details: signals from breakouts or moving-average rules, sized by inverse volatility, across many liquid futures. Profits come from a few large trends and many small losses.
     - Pitfall: long flat periods and drawdowns that cause investors or traders to abandon the system.
     - Build: a diversified multi-asset trend portfolio with volatility targeting.

315. Mean reversion and statistical arbitrage
     - Covers: betting on temporary deviations.
     - Details: model the spread, enter at a z-score threshold, exit near the mean, and stop out on regime change. Holding period relates to the half-life of reversion.
     - Pitfall: relationships that break and turn small gains into large losses.
     - Build: a z-score entry/exit strategy with a stop and half-life-based time exit.

316. Pairs and basket trading
     - Covers: relative-value trades.
     - Details: select pairs by cointegration or distance, hedge ratio by regression or Kalman filter, and monitor spread stability.
     - Pitfall: selecting many pairs and trading chance relationships.
     - Build: a pairs engine with formation and trading windows and multiple-testing control.

317. Cross-sectional momentum and factor investing
     - Covers: ranking assets against each other.
     - Details: long top deciles and short bottom deciles of a factor such as 12-1 month return, with sector or risk neutralization.
     - Pitfall: momentum crashes after market rebounds.
     - Build: a monthly rebalanced long-short factor portfolio with turnover reporting.

318. Carry strategies
     - Covers: earning the yield differential.
     - Details: examples are FX interest differentials, futures roll yield, and bond roll-down. Carry has negative skew, with occasional sharp losses.
     - Pitfall: harvesting carry without tail-risk controls.
     - Build: a carry portfolio with a drawdown and crash-scenario test.

319. Volatility strategies
     - Covers: trading volatility itself.
     - Details: selling volatility earns a risk premium but has crash risk, buying volatility pays in stress but bleeds in calm.
     - Pitfall: short-vol strategies that look like steady income until a spike.
     - Build: a volatility strategy with explicit loss limits and spike scenario analysis.

320. Event-driven and earnings strategies
     - Covers: trading around scheduled or unscheduled events.
     - Details: pre-event positioning, post-event drift, and implied-versus-realized move trading.
     - Pitfall: small samples and event-date errors.
     - Build: an event database with confirmed dates and an event-study framework.

321. Index, ETF, and basis arbitrage
     - Covers: price differences between related instruments.
     - Details: compare ETF price with NAV, futures with spot plus carry, and index with constituents.
     - Pitfall: ignoring borrow, financing, and execution risk across legs.
     - Build: a basis monitor with transaction-cost-adjusted entry thresholds.

322. Market-neutral and long-short
     - Covers: reducing market exposure.
     - Details: match long and short exposure by dollars, beta, or sector. Residual risk is factor exposure and stock selection.
     - Pitfall: hidden factor exposures, crowding, and short squeezes.
     - Build: a neutralization routine and an exposure report.

323. Intraday, scalping, opening-range strategies
     - Covers: short-horizon trading.
     - Details: very cost-sensitive, with edge measured in ticks. Needs accurate fill modeling and queue assumptions.
     - Pitfall: backtests that assume impossible fills.
     - Build: a cost break-even analysis per trade before building the strategy.

324. Market making
     - Covers: providing liquidity.
     - Details: earn spread, manage inventory, and avoid adverse selection. Quotes adjust to inventory and volatility.
     - Pitfall: being picked off by informed flow during news or fast moves.
     - Build: a simulated quoting strategy with inventory limits and adverse-selection measurement.

325. Tail-hedging and convex strategies
     - Covers: paying a small cost for crash protection.
     - Details: long out-of-the-money puts or trend-following overlays. The cost is a continuous drag.
     - Pitfall: hedges abandoned before the crash because of bleed.
     - Build: evaluate cost versus protection across historical crises.

326. Systematic macro and cross-asset
     - Covers: trading macro themes with rules.
     - Details: signals from growth, inflation, rates, and positioning across equities, bonds, currencies, and commodities.
     - Pitfall: few independent bets, with correlated macro exposures.
     - Build: a risk-budgeted cross-asset portfolio with an exposure map.

327. Multi-asset and multi-venue arbitrage
     - Covers: price differences across assets or venues.
     - Details: triangular FX, cross-exchange crypto, and ETF-versus-basket. Requires speed, funding, and transfer capability.
     - Pitfall: edges disappear after transfer fees, latency, and legging risk.
     - Build: a net-of-cost opportunity scanner with latency simulation.

## 7.2 Instrument selection and scoring

328. Universe construction and screening
     - Covers: choosing what is tradable.
     - Details: filters on liquidity, price, market cap, listing status, and data history, applied as of each date.
     - Pitfall: building the universe from today's survivors.
     - Build: a point-in-time universe function with tests.

329. Liquidity filters (ADV, spread, depth)
     - Covers: tradability screens.
     - Details: average daily value traded, typical spread in bps, and depth at best prices. Cap your order size as a fraction of ADV.
     - Pitfall: using volume of a single day or a stale average.
     - Build: a liquidity score and a maximum-position rule tied to ADV.

330. Technical and momentum scoring
     - Covers: price-based ranking.
     - Details: trailing return, trend strength, and relative strength combined into a score, often skipping the most recent month to avoid short-term reversal.
     - Pitfall: ranking on noisy short windows.
     - Build: a score and rank-stability analysis.

331. Multi-factor composite scores and z-score normalization
     - Covers: combining signals into one score.
     - Details: cross-sectional z-score per factor, winsorize outliers, then weight. z = (x - mean) / std across the universe.
     - Pitfall: normalizing with future data or mixing sector effects.
     - Build: a normalization pipeline with a no-look-ahead test.

332. Cross-sectional ranking and long-short construction
     - Covers: turning ranks into positions.
     - Details: long top quantile, short bottom quantile, weight equally, by score, or by inverse volatility.
     - Pitfall: concentration in a few extreme names.
     - Build: portfolio construction with weight caps and turnover limits.

333. Pair and basket selection (distance, cointegration, clustering)
     - Covers: choosing related instruments.
     - Details: distance method uses normalized price distance. Cointegration tests relationships. Clustering groups similar assets.
     - Pitfall: pairs found by brute-force search without correction.
     - Build: a selection pipeline with out-of-sample pair survival statistics.

334. Sector and industry rotation
     - Covers: choosing sectors.
     - Details: rank by relative strength, fundamentals, or macro regime, with defined rebalance rules.
     - Pitfall: frequent switching and crowded sectors.
     - Build: a rotation model with transaction costs.

335. Futures contract selection (roll rules, continuous contracts, carry)
     - Covers: which contract to trade.
     - Details: trade the most liquid contract, roll before expiry by volume or date, and consider the term-structure carry.
     - Pitfall: continuous-contract series that hide roll gaps or use unrealistic prices.
     - Build: a roll scheduler and a carry calculation per contract.

336. Option contract selection (strike, expiry, delta targeting, liquidity)
     - Covers: choosing options to trade.
     - Details: choose by delta, days to expiry, implied volatility rank, bid-ask spread, and open interest.
     - Pitfall: selecting illiquid strikes with wide spreads.
     - Build: a contract selector with liquidity filters and cost estimates.

337. Dynamic universe changes, delisting, survivorship handling
     - Covers: changes over time.
     - Details: handle additions, removals, delistings, mergers, and symbol changes, with proper delisting returns.
     - Pitfall: dropping delisted names and inflating backtest returns.
     - Build: a universe history table and a survivorship-bias check.

## 7.3 Trade management and strategy logic

338. Entry, exit, stop-loss, and take-profit logic design
     - Covers: complete trade rules.
     - Details: define entry trigger, order type, stop, target, time exit, and rules after partial fills.
     - Pitfall: unspecified edge cases such as what happens on gaps.
     - Build: a rule state machine with tests for each branch.

339. Time-based, volatility-based, and signal-reversal exits
     - Covers: exit alternatives.
     - Details: time exit after N bars, volatility exit when risk rises, reversal exit on opposite signal.
     - Pitfall: stacking exits that interact unexpectedly.
     - Build: exit-comparison study measuring expectancy and holding time.

340. Signal-to-order translation (target-position vs. delta-order models)
     - Covers: converting signals into orders.
     - Details: target-position approach computes desired position and sends the difference. This is easier to reconcile than sending incremental orders.
     - Pitfall: duplicate orders when signals repeat.
     - Build: a target-position engine with idempotent order generation.

341. Strategy parameter management and regime-dependent parameters
     - Covers: configuration control.
     - Details: store parameters in versioned config, with ranges and ownership. Regime-dependent sets need documented switching rules.
     - Pitfall: editing parameters live without tracking.
     - Build: versioned configs and an audit log of changes.

342. Strategy SDK and plugin interface (a uniform contract for all strategies)
     - Covers: common strategy API.
     - Details: define callbacks for data, timers, fills, and lifecycle, plus standard access to positions and risk limits.
     - Pitfall: strategies that reach into internals and break portability between backtest and live.
     - Build: an interface specification and a sample strategy that runs in both modes.

343. Scheduler, event bus, and session lifecycle (pre-open, open, close, post-close)
     - Covers: timing and orchestration.
     - Details: tasks per phase, such as data checks pre-open, trading during the session, reconciliation post-close.
     - Pitfall: tasks scheduled in local time without time-zone handling.
     - Build: a calendar-aware scheduler with phase hooks.

344. Manual override and human-in-the-loop controls (four-eyes approval)
     - Covers: human intervention.
     - Details: pause, flatten, resize, and parameter changes require authorization and logging, and large changes need a second approver.
     - Pitfall: overrides that bypass risk checks.
     - Build: override commands routed through the same risk layer with audit entries.

345. Alpha combination and signal blending (ensemble, stacking)
     - Covers: merging multiple signals.
     - Details: weights by equal, inverse variance, or regression with constraints. Check signal correlation first.
     - Pitfall: stacking weights fitted on in-sample data.
     - Build: blend with walk-forward weight estimation.

## 7.4 Market microstructure and market theory (MMT)

346. Market Microstructure Theory (Kyle, Glosten-Milgrom, Almgren-Chriss)
     - Covers: models of price formation and trading.
     - Details: Kyle's lambda measures price impact per unit of order flow. Glosten-Milgrom explains spreads from adverse selection. Almgren-Chriss trades off impact and risk in execution.
     - Pitfall: using model parameters without calibration.
     - Build: estimate impact and spread components from your data.

347. Order flow imbalance, VPIN, toxicity
     - Covers: signed flow measures.
     - Details: imbalance = buy volume - sell volume. VPIN estimates the probability of informed trading using volume buckets.
     - Pitfall: classification errors and parameter sensitivity.
     - Build: imbalance and VPIN series, and their relation to short-term volatility.

348. Bid-ask bounce and effective spread decomposition
     - Covers: spread components.
     - Details: quoted spread, effective spread = 2 x |price - mid|, realized spread, and price impact components.
     - Pitfall: bounce creates false negative autocorrelation.
     - Build: spread decomposition per instrument and time of day.

349. Queue position and limit order book dynamics
     - Covers: passive-order fill modeling.
     - Details: fill probability depends on queue position, order arrival, and cancellation rates.
     - Pitfall: assuming a limit order at the touch fills as soon as price trades there.
     - Build: a queue-aware fill simulator.

350. Market impact models (square-root law, permanent vs. temporary)
     - Covers: price effect of trading.
     - Details: impact scales roughly with sigma x sqrt(Q / ADV) for metaorders. Split into temporary and permanent parts.
     - Pitfall: linear impact assumptions at large size.
     - Build: calibrate impact from your own fills.

351. Inventory models for market making (Avellaneda-Stoikov)
     - Covers: quoting under inventory risk.
     - Details: reservation price shifts away from mid as inventory grows, with spread depending on volatility and risk aversion.
     - Pitfall: model assumptions of constant volatility and Poisson arrivals.
     - Build: a simulation of the model against a noisy order-flow process.

352. Adverse selection and latency arbitrage
     - Covers: trading against better-informed or faster flow.
     - Details: stale quotes are picked off after price moves on another venue.
     - Pitfall: ignoring that slow quotes subsidize fast participants.
     - Build: measure how often your quotes are hit just before a price change.

353. Modern Portfolio Theory, its critiques, and the Adaptive Market Hypothesis
     - Covers: portfolio theory context.
     - Details: mean-variance optimization is sensitive to estimation error. The adaptive hypothesis says efficiency varies as participants adapt.
     - Pitfall: treating historical estimates as true parameters.
     - Build: compare mean-variance and simple heuristics out of sample.

354. Efficient Market Hypothesis and behavioral finance
     - Covers: market-efficiency debate.
     - Details: forms (weak, semi-strong, strong) and documented anomalies and biases.
     - Pitfall: using behavioral narratives without testable predictions.
     - Build: a list of testable behavioral hypotheses with data.
