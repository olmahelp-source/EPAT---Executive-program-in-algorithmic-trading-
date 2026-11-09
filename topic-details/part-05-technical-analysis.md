# Part 5. Technical Analysis: Micro Details (topics 201 to 301)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 5.1 Foundations and philosophy

201. Core assumptions (price discounts everything, trends persist, history repeats) and their critiques
     - Covers: the premises of technical analysis.
     - Details: each assumption is testable. Price may reflect information, but trend persistence and repetition vary by market and period.
     - Pitfall: treating the premises as facts.
     - Build: test one premise (trend persistence) with autocorrelation and variance-ratio tests.

202. Chart types (line, bar, candlestick, Heikin-Ashi, Renko, point-and-figure, Kagi, range bars, volume bars, tick bars)
     - Covers: price representations.
     - Details: time-based charts differ from event-based ones (tick, volume, Renko). Heikin-Ashi smooths prices but changes the values.
     - Pitfall: backtesting on smoothed prices that were not tradable.
     - Build: compute several chart types from the same ticks.

203. Scales (arithmetic vs. logarithmic) and data adjustments (splits, dividends, back-adjusted futures)
     - Covers: display and data adjustment.
     - Details: log scale shows percentage moves consistently over long periods. Adjustments change historical price levels.
     - Pitfall: applying price-level support rules to adjusted data.
     - Build: both raw and adjusted series with a documented use for each.

204. Time frames, bar construction (time, tick, volume, dollar bars), and alignment issues
     - Covers: sampling methods.
     - Details: volume and dollar bars sample by activity and give more stable statistical properties than time bars. Multi-timeframe bars must align.
     - Pitfall: higher-timeframe bar values used before the bar closes.
     - Build: a bar builder with a test that incomplete bars are never used.

205. Price, volume, open interest, and breadth as the four data pillars
     - Covers: inputs for technical analysis.
     - Details: price shows direction, volume shows conviction, open interest shows futures participation, breadth shows market-wide participation.
     - Pitfall: using price only when volume or breadth disagree.
     - Build: a panel combining all four inputs.

206. Technical analysis vs. quantitative systematic rules vs. discretionary reading
     - Covers: levels of rule rigor.
     - Details: systematic rules are testable. Discretionary reading cannot be backtested directly.
     - Pitfall: claiming results for discretionary methods without records.
     - Build: convert one discretionary pattern into a precise rule.

207. Random-walk critique, efficient-markets critique, and empirical evidence for and against
     - Covers: skeptical view.
     - Details: efficient markets imply no predictable pattern after costs. Evidence on trend and momentum is mixed but real in some assets.
     - Pitfall: dismissing or accepting everything without testing.
     - Build: test a simple trend rule against a random-walk simulation.

208. Subjectivity problem: making a pattern rule precise enough to test
     - Covers: formalization.
     - Details: define each pattern with numeric parameters (lookback, thresholds, tolerance).
     - Pitfall: tuning definitions after seeing outcomes.
     - Build: a written rule specification before any backtesting.

## 5.2 Trend analysis

209. Trend definition (higher highs/lows, moving-average slope, regression slope)
     - Covers: measuring trend.
     - Details: regression slope t-stat measures trend strength. Swing structure is rule-based using pivots with a delay.
     - Pitfall: pivots are only known after confirmation bars.
     - Build: a trend classifier with confirmation lag.

210. Trend channels, trendlines, and breakouts (and their false-signal rates)
     - Covers: line-based trend methods.
     - Details: lines drawn from pivots; breakouts need a volatility buffer.
     - Pitfall: lines drawn with hindsight.
     - Build: an automated trendline algorithm with a false-breakout statistic.

211. Moving averages (SMA, EMA, WMA, HMA, KAMA, VIDYA, DEMA, TEMA, ALMA) and lag trade-offs
     - Covers: smoothing variants.
     - Details: EMA weight alpha = 2/(n+1). Lower lag generally increases noise.
     - Pitfall: choosing the average that fits the past best.
     - Build: lag versus whipsaw comparison across averages.

212. Moving-average crossovers, ribbons, and multi-MA systems
     - Covers: crossover rules.
     - Details: fast above slow = long. Ribbons use many averages to show trend alignment.
     - Pitfall: whipsaws in sideways markets.
     - Build: a crossover system with cost-aware testing across parameter grids.

213. Donchian channels and the turtle-style breakout
     - Covers: breakout of N-period highs and lows.
     - Details: classic systems used 20-day or 55-day breakouts with ATR-based sizing and stops.
     - Pitfall: ignoring costs and slippage on breakouts.
     - Build: a breakout system tested with realistic slippage.

214. ADX, +DI/-DI, and trend-strength measurement
     - Covers: trend intensity.
     - Details: ADX measures strength, not direction. Values above about 25 are often read as trending.
     - Pitfall: ADX lags and peaks after trends mature.
     - Build: ADX as a filter on a trend system and measure the change.

215. Parabolic SAR and trailing-stop systems
     - Covers: stop-and-reverse logic.
     - Details: SAR accelerates toward price with an acceleration factor.
     - Pitfall: constant whipsaw in ranges.
     - Build: compare SAR with ATR trailing stops.

216. Supertrend and ATR-based trend filters
     - Covers: volatility-adjusted trend bands.
     - Details: bands = midpoint +/- multiplier x ATR with flip rules.
     - Pitfall: parameter overfitting.
     - Build: a plateau analysis of multiplier and period.

217. Aroon, Vortex, and trend-direction indicators
     - Covers: alternative direction measures.
     - Details: Aroon counts time since extremes. Vortex compares upward and downward movement.
     - Pitfall: redundancy with other trend indicators.
     - Build: correlation matrix among trend indicators.

218. Ichimoku Cloud (components, rules, and testing)
     - Covers: multi-line trend system.
     - Details: Tenkan, Kijun, Senkou A/B, Chikou; plotted displacements require care to avoid look-ahead.
     - Pitfall: the shifted lines use future-plotted values incorrectly.
     - Build: an implementation with explicit shift handling and tests.

219. Time-series momentum and its theoretical link to trend following
     - Covers: own-asset momentum.
     - Details: go long if past return over a lookback is positive, short if negative, scaled by volatility.
     - Pitfall: ignoring transaction costs in fast variants.
     - Build: a volatility-targeted time-series momentum across assets.

220. Trend-regime filters (e.g., price versus 200-day average)
     - Covers: regime gating.
     - Details: switch risk on when price is above a long average, off otherwise.
     - Pitfall: frequent switching around the average.
     - Build: add a hysteresis band to reduce flips.

## 5.3 Momentum and oscillators

221. RSI (levels, divergence, failure swings, Connors RSI)
     - Covers: bounded momentum oscillator.
     - Details: RSI = 100 - 100/(1 + RS), RS = average gain / average loss (Wilder smoothing). Common period is 14.
     - Pitfall: using 70/30 as automatic reversal signals in trends.
     - Build: RSI mean-reversion versus momentum testing across assets.

222. Stochastic oscillator (fast, slow, full)
     - Covers: close relative to recent range.
     - Details: %K = (close - lowest low) / (highest high - lowest low) x 100.
     - Pitfall: oversold readings that persist in downtrends.
     - Build: compare stochastic timing with a baseline.

223. MACD (signal line, histogram, divergence)
     - Covers: difference of EMAs.
     - Details: MACD = EMA12 - EMA26; signal = EMA9 of MACD; histogram = MACD - signal.
     - Pitfall: it is a lagging indicator, with many false crosses.
     - Build: MACD cross rule with cost-aware backtest.

224. CCI, Williams %R, Ultimate Oscillator
     - Covers: alternative oscillators.
     - Details: CCI normalizes price deviation from its average. Williams %R is an inverted stochastic.
     - Pitfall: indicators that are near duplicates of each other.
     - Build: measure the information overlap among oscillators.

225. ROC, momentum, TRIX, and PPO
     - Covers: rate-of-change measures.
     - Details: ROC = price / price_n - 1. TRIX is a triple-smoothed EMA's rate of change.
     - Pitfall: different scales make thresholds non-comparable.
     - Build: standardize indicators by their rolling distribution.

226. Awesome Oscillator and Elder-ray
     - Covers: momentum and power measures.
     - Details: AO = SMA(median price, 5) - SMA(median price, 34). Elder-ray measures bull and bear power relative to an EMA.
     - Pitfall: platform-specific definitions.
     - Build: reference implementations validated against a platform.

227. Money Flow Index and volume-weighted oscillators
     - Covers: volume-informed momentum.
     - Details: MFI is a volume-weighted RSI using typical price flows.
     - Pitfall: volume data quality varies, especially in FX.
     - Build: MFI usage only on instruments with reliable volume.

228. Divergence detection (regular and hidden) and quantifying it algorithmically
     - Covers: price-indicator disagreement.
     - Details: define swing points, compare slopes, and require a confirmation lag.
     - Pitfall: look-ahead through swing detection.
     - Build: a divergence detector with delayed confirmation and an out-of-sample test.

229. Overbought/oversold fallacy in trending markets
     - Covers: misuse of extremes.
     - Details: strong trends keep oscillators extreme for long periods.
     - Pitfall: fading a strong trend.
     - Build: condition oscillator signals on a trend-regime filter.

230. Oscillator parameter dependence and adaptive-length versions
     - Covers: parameter sensitivity.
     - Details: adaptive-length versions vary the window with volatility or cycle estimates.
     - Pitfall: added complexity without added edge.
     - Build: compare fixed and adaptive versions out of sample.

## 5.4 Volatility and range indicators

231. ATR, true range, and volatility-normalized stops
     - Covers: range-based volatility.
     - Details: true range = max(high - low, |high - prev close|, |low - prev close|). ATR is its smoothed average.
     - Pitfall: stops tighter than normal noise.
     - Build: stop distances in ATR multiples with a stop-out frequency analysis.

232. Bollinger Bands, %B, bandwidth, and squeeze setups
     - Covers: standard-deviation bands.
     - Details: bands = SMA +/- k x std (k = 2 by default). %B shows position within the bands; bandwidth shows compression.
     - Pitfall: treating band touches as automatic reversals.
     - Build: a test of band touch behavior in trend and range regimes.

233. Keltner and STARC bands
     - Covers: ATR-based bands.
     - Details: Keltner uses EMA +/- multiple x ATR, which reacts differently from standard deviation.
     - Pitfall: confusing band types across platforms.
     - Build: compare squeeze definitions using Bollinger inside Keltner.

234. Standard-deviation channels and linear-regression channels
     - Covers: statistical channels.
     - Details: regression line with parallel bands at k standard errors.
     - Pitfall: recomputed channels repaint as new data arrive.
     - Build: use only channels computed with data available at each bar.

235. Historical, realized, and implied-volatility comparison
     - Covers: volatility measures.
     - Details: realized vs. implied gap is the volatility risk premium.
     - Pitfall: different annualization and windows make comparisons wrong.
     - Build: a consistent realized-vs-implied series.

236. Volatility breakouts and compression-expansion cycles
     - Covers: volatility clustering.
     - Details: low-volatility periods often precede high-volatility ones, but direction is unknown.
     - Pitfall: assuming a squeeze gives a direction.
     - Build: volatility-breakout rules paired with direction filters.

237. Chaikin volatility and Ulcer-index-style measures
     - Covers: alternative volatility gauges.
     - Details: Chaikin volatility tracks change in the high-low range. Ulcer index measures downside depth and duration.
     - Pitfall: redundancy with ATR.
     - Build: compare information content versus ATR.

238. Volatility regime classification for strategy switching
     - Covers: regime-dependent strategies.
     - Details: classify low, medium, and high volatility with thresholds based on rolling quantiles.
     - Pitfall: using full-sample quantiles that leak the future.
     - Build: an expanding-window volatility regime and performance by regime.

## 5.5 Volume, order flow, and market breadth

239. Volume analysis basics (volume confirmation, climaxes, dry-ups)
     - Covers: volume interpretation.
     - Details: moves on rising volume are treated as stronger. Volume climaxes may mark exhaustion.
     - Pitfall: volume is not comparable across sessions without normalization.
     - Build: relative-volume scores by time of day.

240. OBV, accumulation/distribution, Chaikin Money Flow
     - Covers: volume-flow indicators.
     - Details: OBV adds volume on up days and subtracts on down days. A/D weights volume by close location in the range.
     - Pitfall: cumulative indicators depend on the start date.
     - Build: use changes or normalized versions, not raw cumulative levels.

241. VWAP, anchored VWAP, and volume-weighted bands
     - Covers: volume-weighted average price.
     - Details: VWAP = sum(price x volume) / sum(volume) from the anchor point. Used as an execution benchmark and a fair-value reference.
     - Pitfall: VWAP resets daily by default and is path dependent.
     - Build: anchored VWAP from earnings or swing points.

242. Volume profile (POC, value area, HVN/LVN) and market profile (TPO)
     - Covers: price-by-volume distribution.
     - Details: point of control is the price with most volume. Value area typically covers about 70% of volume.
     - Pitfall: profile depends on session definition and data quality.
     - Build: compute daily profiles and test reactions at POC and value-area edges.

243. Footprint charts, delta, cumulative delta, and absorption
     - Covers: order-flow detail.
     - Details: delta = volume at ask - volume at bid. Needs tick data with trade-side classification.
     - Pitfall: misclassified trade sides distort delta.
     - Build: tick-rule or quote-based classification with accuracy checks.

244. Order-book heatmaps and DOM reading (with the spoofing caveat)
     - Covers: depth visualization.
     - Details: shows resting liquidity, which can be pulled quickly.
     - Pitfall: spoofed orders create false signals.
     - Build: track cancellation rates of large displayed orders.

245. Open interest and futures positioning interpretation
     - Covers: futures participation.
     - Details: rising price and rising open interest suggests new longs. Rising price with falling open interest suggests short covering.
     - Pitfall: open interest is reported daily and often with delay.
     - Build: a four-state price-OI table with forward returns.

246. Breadth indicators (advance/decline line, McClellan, TRIN, % above moving average, new highs/new lows)
     - Covers: market participation.
     - Details: narrowing breadth can accompany late-stage rallies.
     - Pitfall: breadth data composition changes over time.
     - Build: breadth indicators for your index and their forward-return relation.

247. Sector and index participation analysis
     - Covers: breadth by group.
     - Details: examine whether gains are concentrated in few names or sectors.
     - Pitfall: cap-weighted index hides equal-weight weakness.
     - Build: equal-weight versus cap-weight divergence tracking.

248. Put/call ratios, VIX-term structure, and sentiment-based contrarian indicators
     - Covers: sentiment via derivatives.
     - Details: high put/call and steep VIX backwardation indicate fear.
     - Pitfall: contrarian signals can fire early in persistent stress.
     - Build: test sentiment extremes with a time-delay confirmation.

## 5.6 Price patterns

249. Support, resistance, and role reversal; zone vs. line formulation
     - Covers: price levels.
     - Details: define zones with width based on ATR, not exact lines. Count touches and recency.
     - Pitfall: seeing levels everywhere after the fact.
     - Build: an objective level-detection algorithm and a bounce statistic.

250. Candlestick patterns (doji, hammer, engulfing, morning/evening star, etc.) and statistical performance
     - Covers: candle formations.
     - Details: define each by ratios of body and shadows. Test forward returns with controls.
     - Pitfall: most patterns show no edge after costs.
     - Build: pattern-frequency and forward-return table with significance.

251. Classical chart patterns (head-and-shoulders, double top/bottom, triangles, flags, wedges, rectangles, cup-and-handle)
     - Covers: geometric formations.
     - Details: formal rules need pivot detection, tolerance, and breakout confirmation.
     - Pitfall: subjective pattern recognition.
     - Build: rule-based detectors with parameters fixed before testing.

252. Gaps (common, breakaway, runaway, exhaustion) and gap-fill behavior
     - Covers: price discontinuities.
     - Details: gap-fill probability depends on size, volume, and context.
     - Pitfall: ignoring that gaps are often news-driven.
     - Build: gap-fill statistics by gap size and news flag.

253. Pivot points (classic, Fibonacci, Camarilla, Woodie)
     - Covers: formula-based levels.
     - Details: classic pivot = (H + L + C) / 3 from the prior session, with support and resistance derived from it.
     - Pitfall: using different session definitions.
     - Build: test price reaction near pivot levels.

254. Opening-range, initial-balance, and previous-day-high/low levels
     - Covers: intraday reference levels.
     - Details: opening range is the first N minutes' high and low.
     - Pitfall: different results by market and time of year.
     - Build: opening-range breakout with time-of-day filters.

255. Round-number and psychological levels
     - Covers: clustering at round prices.
     - Details: orders tend to cluster at round numbers in some markets.
     - Pitfall: tick-size changes affect the clustering.
     - Build: order and trade density near round numbers.

256. Swing-point detection algorithms (zigzag, fractals, rolling extremes)
     - Covers: pivot identification.
     - Details: a swing high requires N lower highs after it, so it is known only N bars later.
     - Pitfall: plotting a zigzag at the original bar creates look-ahead.
     - Build: a detector that records confirmation time.

257. Algorithmic pattern recognition (template matching, dynamic time warping, CNN-based detection)
     - Covers: automated pattern search.
     - Details: template matching measures similarity to a prototype, DTW handles time stretching, and CNNs learn patterns from images or series.
     - Pitfall: overfitted detectors with high false-positive rates.
     - Build: a detector evaluated on held-out periods.

258. Pattern failure rates, measured-move targets, and statistical edge verification
     - Covers: pattern outcomes.
     - Details: measure hit rate, payoff, and expectancy with costs, plus failure rate.
     - Pitfall: published target rules without out-of-sample proof.
     - Build: expectancy table with confidence intervals.

## 5.7 Fibonacci, wave, and geometric methods (critical evaluation)

259. Fibonacci retracement, extension, and clusters
     - Covers: ratio-based levels.
     - Details: common ratios 38.2%, 50%, 61.8%. Choice of swing anchors drives results.
     - Pitfall: so many levels that something always matches.
     - Build: compare reactions at Fibonacci levels to random levels.

260. Elliott Wave counting and its non-falsifiability problem
     - Covers: wave theory.
     - Details: counts can be revised after the fact, making testing difficult.
     - Pitfall: unfalsifiable wave labels.
     - Build: only test mechanical, rule-based wave definitions.

261. Gann angles, squares, and time cycles
     - Covers: geometric price-time relationships.
     - Details: scale-dependent angles and cycle counts with limited statistical support.
     - Pitfall: fitting angles to past data.
     - Build: test against randomized anchors.

262. Harmonic patterns (Gartley, Bat, Butterfly, Crab)
     - Covers: ratio-defined patterns.
     - Details: patterns defined by Fibonacci ratios between legs with tolerance.
     - Pitfall: large tolerance leads to many false matches.
     - Build: a strict-tolerance detector and out-of-sample results.

263. Wyckoff method (accumulation, distribution, springs, upthrusts)
     - Covers: market-cycle structure.
     - Details: phases of accumulation and distribution with volume behavior.
     - Pitfall: discretionary labeling of phases.
     - Build: convert one phase concept into measurable volume and range rules.

264. Dow Theory and its modern interpretation
     - Covers: trend confirmation.
     - Details: confirmation between indexes, primary and secondary trends.
     - Pitfall: slow signals.
     - Build: a simple rule for index confirmation.

265. Cycle analysis (Fourier, wavelet, Hilbert transform, dominant-cycle detection)
     - Covers: periodic components.
     - Details: spectral methods need stationarity and enough cycles in the sample.
     - Pitfall: spurious cycles from noise.
     - Build: significance test versus surrogate data.

266. Fractals, Hurst exponent, and multifractal market models
     - Covers: scaling behavior.
     - Details: Hurst H estimated by R/S or DFA. Multifractal models allow changing scaling.
     - Pitfall: estimator bias in finite samples.
     - Build: estimate H with confidence intervals using simulated benchmarks.

267. Testing geometric methods statistically (and why many fail)
     - Covers: evaluation framework.
     - Details: randomized benchmarks, out-of-sample periods, and multiple-testing control.
     - Pitfall: stopping after a good-looking result.
     - Build: a template for testing any geometric method against random alternatives.

## 5.8 Multi-timeframe, intermarket, and relative analysis

268. Top-down multi-timeframe alignment (higher-timeframe filter, lower-timeframe entry)
     - Covers: combining horizons.
     - Details: use the last completed higher-timeframe bar for the filter.
     - Pitfall: using the still-forming higher-timeframe bar.
     - Build: a MTF framework with completed-bar-only access.

269. Relative strength and ratio charts (stock vs. index, sector vs. market)
     - Covers: relative performance.
     - Details: price ratio or relative return versus benchmark ranks leaders and laggards.
     - Pitfall: benchmark choice drives results.
     - Build: relative-strength rankings with a rebalance schedule.

270. Intermarket relationships (stocks, bonds, dollar, commodities)
     - Covers: cross-asset linkages.
     - Details: correlations change across regimes, such as stock-bond correlation sign.
     - Pitfall: assuming stable correlation.
     - Build: rolling correlations with regime annotations.

271. Sector rotation using relative-strength ranking
     - Covers: tactical sector allocation.
     - Details: rank sectors on trailing return and hold the top ones, rebalancing monthly.
     - Pitfall: high turnover and crowded trades.
     - Build: a rotation backtest with costs and a lag parameter.

272. Cross-asset confirmation and divergences
     - Covers: confirmation signals.
     - Details: e.g., equities rising while credit spreads widen.
     - Pitfall: many possible divergences, few reliable.
     - Build: pre-register a small set of divergences and test them.

273. Correlation regime changes and their impact on technical signals
     - Covers: instability of relationships.
     - Details: signals that rely on correlation fail when the regime shifts.
     - Pitfall: static assumptions about co-movement.
     - Build: regime-conditional performance of each signal.

274. Seasonality, calendar effects, and time-of-day patterns (turn-of-month, expiry week, intraday U-shape)
     - Covers: time-based patterns.
     - Details: volume and volatility follow intraday U-shape. Turn-of-month and holiday effects exist in some markets.
     - Pitfall: calendar effects that vanish after publication.
     - Build: time-of-day return and volatility maps with significance tests.

## 5.9 Systematic implementation of technical rules

275. Converting indicators to rules (entry, exit, filter, and position-sizing logic)
     - Covers: specification.
     - Details: define signal timing, execution price, order type, exit conditions, and sizing in writing.
     - Pitfall: ambiguous rules lead to inconsistent implementations.
     - Build: a rule specification template.

276. Signal definition pitfalls (repainting indicators, look-ahead in pivots, current-bar leakage)
     - Covers: data-leakage traps.
     - Details: indicators that change past values repaint. Using the current bar's close to trade at its open is leakage.
     - Pitfall: backtests that pass because of leakage.
     - Build: shift tests that confirm signals use only past data.

277. Indicator parameter selection and overfitting risk (parameter plateaus, walk-forward optimization)
     - Covers: choosing parameters.
     - Details: choose parameters from broad plateaus of performance, not isolated peaks.
     - Pitfall: optimizing on the same data used for evaluation.
     - Build: heatmaps of performance versus parameters and a walk-forward test.

278. Combining indicators (redundancy, multicollinearity among oscillators, confirmation vs. diversification)
     - Covers: multi-indicator systems.
     - Details: many indicators are transformations of the same price data.
     - Pitfall: adding correlated indicators and thinking it is confirmation.
     - Build: correlation matrix of signals and marginal-contribution tests.

279. Stop-loss and trailing-stop design (fixed, ATR, chandelier, structure-based)
     - Covers: exit design.
     - Details: chandelier exit = highest high - k x ATR. Stop distance and position size are linked.
     - Pitfall: stops inside normal noise.
     - Build: compare stop types by drawdown and expectancy.

280. Profit-target design and scaling-out rules
     - Covers: exits at gains.
     - Details: targets cap winners, so check effect on the payoff distribution.
     - Pitfall: cutting winners while letting losers run.
     - Build: compare fixed targets with trailing exits.

281. Technical signals as ML features (indicator feature engineering, stationarity, scaling)
     - Covers: features for models.
     - Details: use stationary transformations, rank or z-score normalization, and avoid raw price levels.
     - Pitfall: leakage through normalization using future statistics.
     - Build: an expanding-window normalization pipeline.

282. Technical analysis for intraday vs. swing vs. position horizons
     - Covers: horizon-specific behavior.
     - Details: cost sensitivity increases at shorter horizons.
     - Pitfall: using daily-bar logic for intraday execution.
     - Build: cost break-even holding period per strategy.

283. Technical rules by asset class and instrument behavior (futures, FX, equities, crypto)
     - Covers: instrument-specific adaptation.
     - Details: trading hours, volatility, gaps, and volume reliability differ.
     - Pitfall: copying parameters across assets.
     - Build: per-asset parameter ranges and tests.

284. Library and implementation inconsistencies (TA-Lib vs. pandas-ta vs. platform-native outputs)
     - Covers: indicator implementation differences.
     - Details: smoothing methods (Wilder vs. EMA) and warm-up periods differ between libraries.
     - Pitfall: live signals differ from backtests due to implementation.
     - Build: cross-library comparison on the same data.

285. Auditing indicator correctness against reference platforms
     - Covers: verification.
     - Details: compare your values with a trusted platform after the warm-up period.
     - Pitfall: unnoticed small differences that change signals.
     - Build: automated test comparing indicator values to reference files.

## 5.10 Evidence, testing, and critique of technical analysis

286. Academic evidence (Brock-Lakonishok-LeBaron, Lo-Mamaysky-Wang, and subsequent replications)
     - Covers: research record.
     - Details: early studies found some predictive power for simple rules, later work found it weakened after costs and data-snooping control.
     - Pitfall: citing early positive results only.
     - Build: replicate a classic study on recent data.

287. Data-snooping across thousands of technical rules (White's Reality Check applied to TA)
     - Covers: selection bias in rule search.
     - Details: with thousands of rules, some win by chance.
     - Pitfall: reporting the best rule.
     - Build: reality-check on a large rule family.

288. Transaction-cost sensitivity of high-turnover technical systems
     - Covers: cost drag.
     - Details: gross edge per trade must exceed spread, commission, and impact.
     - Pitfall: backtests at zero cost.
     - Build: performance as a function of cost per trade.

289. Regime dependence (trend systems vs. mean-reverting regimes)
     - Covers: when systems work.
     - Details: trend systems profit in sustained trends and lose in choppy ranges.
     - Pitfall: judging a system by one regime.
     - Build: performance by volatility and trend regime.

290. Self-fulfilling-prophecy hypothesis and crowding at popular levels
     - Covers: reflexivity.
     - Details: widely watched levels may attract orders, and stop clusters can be targeted.
     - Pitfall: assuming popularity equals edge.
     - Build: test behavior near widely used levels such as the 200-day average.

291. Survivorship in published technical-analysis "successes"
     - Covers: publication bias.
     - Details: only successful examples get shared.
     - Pitfall: judging a method by testimonials.
     - Build: demand full trade lists and failures.

292. Behavioral explanations (anchoring, herding, disposition effect, under-reaction)
     - Covers: why patterns could exist.
     - Details: under-reaction supports momentum, overreaction supports reversal.
     - Pitfall: using a story to defend a failing test.
     - Build: map each rule to a testable behavioral hypothesis.

293. Technical analysis in algorithmic markets: who is on the other side?
     - Covers: counterparty reasoning.
     - Details: much liquidity is provided by fast firms; ask what your edge is against them.
     - Pitfall: assuming slower public rules capture value from faster participants.
     - Build: write the counterparty hypothesis for each strategy.

## 5.11 Combining fundamental and technical analysis

294. Fundamental screen, technical timing (quality/value universe with momentum entry)
     - Covers: two-step selection.
     - Details: screen for quality or value, then enter on trend confirmation.
     - Pitfall: timing rules that remove most of the value edge.
     - Build: compare screen-only with screen plus timing.

295. Technical filter as a risk overlay on fundamental portfolios
     - Covers: downside protection.
     - Details: reduce exposure when price falls below a long-term average.
     - Pitfall: whipsaw costs.
     - Build: overlay test on drawdown and turnover.

296. Combining value and momentum (negative correlation and diversification benefits)
     - Covers: factor pairing.
     - Details: value and momentum returns are negatively correlated, so combining improves risk-adjusted return.
     - Pitfall: momentum crashes.
     - Build: 50/50 factor combination and drawdown comparison.

297. Event-driven entries (earnings, catalysts) with technical confirmation
     - Covers: event plus price confirmation.
     - Details: wait for price reaction to confirm the event narrative.
     - Pitfall: delay forfeits part of the move.
     - Build: confirmation-lag sensitivity test.

298. Fundamental regime plus technical signal (macro state gates technical systems)
     - Covers: regime gating.
     - Details: switch strategies according to macro states like growth and inflation.
     - Pitfall: using data not yet available.
     - Build: point-in-time macro regime with technical strategy results by regime.

299. Multi-signal scoring frameworks and weighting schemes
     - Covers: composite scores.
     - Details: weights by equal, inverse-volatility, or learned values.
     - Pitfall: learned weights that overfit.
     - Build: compare equal and learned weights out of sample.

300. Evaluating whether the combination adds incremental alpha (ablation and marginal contribution)
     - Covers: added-value testing.
     - Details: drop each component and measure the loss.
     - Pitfall: components that look good alone but add nothing together.
     - Build: ablation table.

301. Conflict-resolution rules when fundamental and technical signals disagree
     - Covers: disagreement handling.
     - Details: options include reduced size, skipping, or priority to one signal.
     - Pitfall: ad hoc overrides.
     - Build: documented rule and a test of its performance.
