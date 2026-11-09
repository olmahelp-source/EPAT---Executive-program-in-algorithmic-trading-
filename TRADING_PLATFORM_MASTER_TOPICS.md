# Master Topic List: Building an Algorithmic Trading Platform

746 topics grouped into 18 parts by type, numbered continuously. Duplicates from earlier drafts were merged.

## Contents

- PART 1. Market Foundations (35 topics)
- PART 2. Quantitative Foundations (43 topics)
- PART 3. Data (18 topics)
- PART 4. Fundamental Analysis (104 topics)
- PART 5. Technical Analysis (101 topics)
- PART 6. Sentiment, News, and Alternative Data (12 topics)
- PART 7. Strategy Design (41 topics)
- PART 8. Artificial Intelligence and Machine Learning (44 topics)
- PART 9. Derivatives and Other Products (36 topics)
- PART 10. Research, Backtesting, and Validation (27 topics)
- PART 11. Portfolio Construction and Capital Allocation (35 topics)
- PART 12. Risk Management (23 topics)
- PART 13. Execution (7 topics)
- PART 14. Costs, Taxes, and Accounting (10 topics)
- PART 15. Performance and Analytics (119 topics)
- PART 16. Architecture, Engineering, and Security (40 topics)
- PART 17. Operations, Governance, Legal, and Business (29 topics)
- PART 18. Human Factors, Case Studies, Emerging Topics, and Prerequisites (22 topics)

## PART 1. Market Foundations

### 1.1 Market structure and asset classes
1. Market structure (exchanges, brokers, ECNs, dark pools, market makers)
2. Asset classes (equities, futures, options, FX, fixed income, crypto)
3. Order book mechanics, bid/ask spread, liquidity
4. Auction mechanisms (opening, closing, volatility halts)

### 1.2 Order types and order handling
5. Order types and order lifecycle (market, limit, stop, IOC/FOK, fills)
6. Bracket, OCO, OTO, and trailing-stop orders
7. Time-in-force variants (GTC, GTD, day, auction-only)
8. Partial fills, rejections, amendments, and cancel/replace races
9. Pegged, hidden, and reserve orders
10. Self-trade prevention and wash-trade guards
11. Order-to-trade ratio limits and exchange throttling rules
12. FIX session management (sequence numbers, resend, heartbeats, drop copy)
13. Cancel-on-disconnect and broker-side kill features
14. RFQ and OTC execution
15. Auction participation strategies (opening, closing, and imbalance trading)
16. Odd lots, fractional shares, and lot-size changes

### 1.3 Calendars, contracts, and exchange rules
17. Trading calendars, sessions, holidays, time zones
18. Contract specifications (tick size, lot size, multipliers)
19. Exchange-specific rules (circuit limits, price bands)
20. Short selling, borrow availability, locate costs
21. Contract rollover handling and expiry-day logic
22. Position limits and regulatory restrictions (short-sale rules, pattern day-trader rules)

### 1.4 Regional and market-specific topics
23. Local market structure and rules (for example NSE/BSE, SEBI, and retail algo regulations)
24. Broker API landscape (Interactive Brokers, Zerodha, Angel One, Alpaca, Binance)
25. Regional circuit breakers, trading hours, and holiday calendars
26. Cross-border trading, capital controls, and foreign-investor limits
27. Local tax and reporting obligations by jurisdiction

### 1.5 Abnormal market conditions
28. Trading halts, limit-up/limit-down, and stale quotes
29. Flash-crash handling and liquidity vacuums
30. Exchange, broker, or data-feed outages (degraded-mode behavior)
31. Fat-finger prints and erroneous trades (busted-trade policy)
32. Index and futures-expiry dislocations
33. Short squeezes and meme-stock dynamics
34. Negative-price events (such as oil in 2020)
35. Circuit-breaker and market-wide halt behavior

## PART 2. Quantitative Foundations

### 2.1 Statistics and probability
36. Descriptive statistics of returns (skewness, kurtosis, fat tails)
37. Probability distributions (normal, Student-t, log-normal, stable, mixtures)
38. Hypothesis testing and p-values in strategy validation
39. Multiple-testing correction (Bonferroni, Benjamini-Hochberg)
40. Deflated Sharpe ratio and probability of backtest overfitting (also as a reporting metric)
41. Bootstrap, jackknife, and resampling
42. Bayesian inference and belief updating
43. Maximum likelihood and method-of-moments estimation
44. Confidence intervals for performance metrics
45. Autocorrelation, partial autocorrelation, Ljung-Box test
46. Stationarity tests (ADF, KPSS, Phillips-Perron)
47. Cointegration (Engle-Granger, Johansen)
48. Regression (OLS, ridge, lasso, elastic net, robust)
49. Heteroscedasticity and Newey-West correction
50. Time-series models (AR, MA, ARIMA, SARIMA, VAR, VECM)
51. Volatility models (EWMA, GARCH, EGARCH, GJR, realized vol, stochastic vol)
52. Regime detection (HMM, Markov switching, change-point detection)
53. Kalman filter and state-space models
54. Extreme value theory
55. Copulas and tail dependence
56. Survival analysis and hazard models

### 2.2 Advanced statistics and validation
57. White's Reality Check, Hansen's SPA test, and data-snooping controls
58. Sharpe ratio under autocorrelation (Lo adjustment) and minimum track record length
59. Ergodicity and why ensemble averages mislead single-account outcomes
60. Causal inference (Granger causality, instrumental variables, double ML) vs. correlation
61. Quantile regression and non-parametric methods
62. Variance ratio test and Hurst exponent
63. Ornstein-Uhlenbeck calibration and half-life of mean reversion
64. Filters and signal processing (low-pass, Hodrick-Prescott, Savitzky-Golay)
65. Effective sample size and overlapping-observation problems

### 2.3 Mathematics
66. Linear algebra (eigen decomposition, SVD, PCA)
67. Covariance estimation (Ledoit-Wolf shrinkage, random matrix denoising)
68. Calculus and numerical differentiation
69. Convex and non-convex optimization (quadratic, conic, gradient-based, evolutionary)
70. Stochastic calculus (Brownian motion, Ito's lemma)
71. Stochastic differential equations and simulation
72. Numerical methods (finite differences, trees, Monte Carlo, quasi-Monte Carlo)
73. Information theory (entropy, mutual information)
74. Fourier and wavelet analysis, spectral methods
75. Game theory
76. Optimal control and dynamic programming
77. Graph theory and network analysis of correlations
78. Fractional differentiation and memory-preserving stationarity

## PART 3. Data

### 3.1 Market data engineering
79. Real-time feeds (WebSocket, FIX/FAST, exchange APIs)
80. Historical data sourcing and cleaning
81. Corporate actions (splits, dividends, mergers, spin-offs) and adjustments
82. Tick, bar, and order-book storage (TimescaleDB, kdb+, QuestDB, ClickHouse)
83. Data normalization and symbology mapping
84. Handling gaps, bad ticks, and outliers
85. Point-in-time and bitemporal data
86. Clock synchronization (PTP/NTP) and timestamping
87. Data vendor selection, licensing, and cost
88. Data quality dashboards and lineage

### 3.2 Fundamental data engineering
89. Sources (exchange filings, XBRL, vendors, company websites, regulators)
90. Parsing and normalizing filings (XBRL tagging, PDF extraction, NLP on text)
91. Ticker, identifier, and corporate-structure mapping (mergers, renames, delistings)
92. Handling currency, unit, and fiscal-year-end differences
93. Estimates data (consensus, revisions, point-in-time snapshots)
94. Survivorship-free and delisting-return-inclusive datasets
95. Data-vendor discrepancies and reconciliation
96. Fundamental-to-price alignment (lags, announcement vs. effective dates)

## PART 4. Fundamental Analysis

### 4.1 Financial statement foundations
97. Income statement structure and line-item quality (revenue recognition, operating vs. non-operating items)
98. Balance sheet structure (assets, liabilities, equity, off-balance-sheet items)
99. Cash flow statement (operating, investing, financing, and the indirect vs. direct method)
100. Articulation between the three statements
101. Accounting standards differences (GAAP vs. IFRS vs. local standards such as Ind AS)
102. Segment reporting and geographic breakdowns
103. Footnotes, MD&A, and risk-factor sections
104. Quarterly vs. annual vs. trailing-twelve-month (TTM) data, seasonality adjustment
105. Restatements, reclassifications, and amended filings
106. Standardizing and normalizing financials across companies and sectors
107. Point-in-time fundamentals (reporting lag, avoiding look-ahead on filing dates)

### 4.2 Ratio analysis
108. Profitability ratios (gross, operating, net margin, ROE, ROA, ROIC, ROCE)
109. DuPont decomposition (3-step and 5-step)
110. Liquidity ratios (current, quick, cash)
111. Leverage and solvency ratios (debt/equity, net debt/EBITDA, interest coverage, Altman Z)
112. Efficiency ratios (asset turnover, inventory days, receivable days, payable days, cash conversion cycle)
113. Growth metrics (revenue, EPS, FCF, book value growth; CAGR; consistency and acceleration)
114. Per-share metrics and dilution effects (EPS, diluted EPS, buybacks, ESOPs)
115. Industry-specific metrics (banks: NIM, NPA, CASA, CAR; insurers: combined ratio; REITs: FFO; retail: same-store sales; SaaS: ARR, churn, NRR; airlines: RASK/CASK)
116. Ratio comparability problems (sector, size, and accounting differences)

### 4.3 Valuation
117. Discounted cash flow (FCFF vs. FCFE, explicit period, terminal value)
118. Cost of capital (CAPM, WACC, beta estimation, size and country premia)
119. Terminal-value sensitivity and why DCF is fragile
120. Relative valuation multiples (P/E, P/B, P/S, EV/EBITDA, EV/Sales, EV/EBIT, PEG, P/FCF)
121. Multiple selection by sector and lifecycle stage
122. Dividend discount models and payout sustainability
123. Residual income and economic value added (EVA)
124. Sum-of-the-parts and asset-based valuation (NAV, replacement cost, liquidation value)
125. Reverse DCF (what does the market price imply?)
126. Scenario and probability-weighted valuation
127. Real options and valuation of growth optionality
128. Valuation of financials, cyclicals, commodity producers, and loss-making firms
129. Earnings normalization and cycle-adjusted multiples (Shiller CAPE)
130. Margin of safety concept and its quantitative implementation
131. Valuation percentiles vs. own history and vs. peers
132. Value traps and when cheap stays cheap

### 4.4 Earnings quality and forensic analysis
133. Accruals analysis (Sloan accrual anomaly)
134. Cash earnings vs. accounting earnings divergence
135. Beneish M-score and manipulation screens
136. Piotroski F-score
137. Altman Z-score and distress prediction (Ohlson, Merton distance-to-default)
138. Revenue-recognition red flags and channel stuffing
139. Working-capital manipulation and capitalization of expenses
140. Related-party transactions and governance red flags
141. Auditor changes, qualifications, and resignations
142. Insider ownership, pledging, and promoter-holding patterns
143. One-time item abuse and recurring "non-recurring" charges
144. Goodwill and intangible impairment risk
145. Debt covenant stress and refinancing risk

### 4.5 Business and industry analysis
146. Competitive advantage (moats: network effects, switching costs, scale, brand, regulation)
147. Porter's five forces and industry structure
148. Market share dynamics and total addressable market
149. Unit economics and operating leverage
150. Pricing power and cost pass-through
151. Capital intensity and return on incremental capital
152. Management quality, capital allocation record, and incentive alignment
153. Corporate governance scoring
154. Business-cycle sensitivity and cyclicality classification
155. Supply chain, customer, and supplier concentration risk
156. Regulatory and policy exposure
157. Disruption risk and technology shifts
158. ESG and sustainability factors as fundamental risk

### 4.6 Fundamental factor signals (systematic)
159. Value factor (book-to-market, earnings yield, FCF yield, EV/EBITDA) and its variants
160. Quality factor (profitability, stability, low leverage, earnings quality)
161. Growth and growth-at-reasonable-price factors
162. Low-volatility, low-beta, and defensive factors
163. Dividend yield, shareholder yield, and buyback factors
164. Investment factor (asset growth) and profitability factor (Fama-French five-factor)
165. Earnings momentum, estimate revisions, analyst surprise, and standardized unexpected earnings (SUE)
166. Post-earnings-announcement drift (PEAD)
167. Analyst coverage, dispersion, and recommendation-change signals
168. Insider-buying and institutional-holding-change signals
169. Short-interest and borrow-cost signals
170. Combining fundamental factors (z-scoring, sector-neutralization, winsorization, ranking)
171. Factor timing vs. static exposure and factor-cyclicality
172. Factor decay, crowding, and the post-publication performance decline

### 4.7 Macro fundamentals
173. GDP, PMI, industrial production, retail sales, employment, and inflation data
174. Leading, coincident, and lagging indicators
175. Monetary policy, policy-rate expectations, balance-sheet effects, and central bank communication
176. Yield curve shape, inversion, and credit spreads as regime signals
177. Currency, commodity, and terms-of-trade effects
178. Fiscal policy, government debt, and election cycles
179. Global liquidity, dollar cycle, and capital flows
180. Nowcasting and surprise indices
181. Macro-to-micro transmission (which sectors react to which indicators)
182. Geopolitical and commodity shock mapping

### 4.8 Event and corporate action fundamentals
183. Earnings calendar, guidance, and surprise-reaction modeling
184. M&A, spin-offs, restructurings, and merger-arbitrage spreads
185. Dividend declarations, ex-dates, special dividends, and stock-split effects
186. Rights issues, QIPs, secondary offerings, and dilution events
187. Credit rating changes and outlook revisions
188. Regulatory approvals, litigation outcomes, and sector-specific catalysts (e.g., drug trials)
189. Management changes and activist involvement

### 4.9 Positioning, flows, and special situations
190. Commitment of Traders (COT) and 13F positioning data
191. Options flow, dark-pool prints, and ETF flow data
192. Index rebalancing, inclusion/exclusion, and ETF creation/redemption effects
193. IPOs, buybacks, secondary offerings, and lock-up expiries
194. Cross-listings, ADRs, and dual-listed arbitrage

### 4.10 Devil's advocate on fundamental analysis
195. Why most fundamental signals are slow and often priced in
196. Value-factor long drawdowns and the "value is dead" debate
197. Accounting-based signal degradation from intangibles-heavy economies
198. Reported-data timing risk (stale information, late filers)
199. Model sensitivity: small input changes produce huge valuation changes
200. Narrative bias vs. numbers and anchoring on analyst consensus

## PART 5. Technical Analysis

### 5.1 Foundations and philosophy
201. Core assumptions (price discounts everything, trends persist, history repeats) and their critiques
202. Chart types (line, bar, candlestick, Heikin-Ashi, Renko, point-and-figure, Kagi, range bars, volume bars, tick bars)
203. Scales (arithmetic vs. logarithmic) and data adjustments (splits, dividends, back-adjusted futures)
204. Time frames, bar construction (time, tick, volume, dollar bars), and alignment issues
205. Price, volume, open interest, and breadth as the four data pillars
206. Technical analysis vs. quantitative systematic rules vs. discretionary reading
207. Random-walk critique, efficient-markets critique, and empirical evidence for and against
208. Subjectivity problem: making a pattern rule precise enough to test

### 5.2 Trend analysis
209. Trend definition (higher highs/lows, moving-average slope, regression slope)
210. Trend channels, trendlines, and breakouts (and their false-signal rates)
211. Moving averages (SMA, EMA, WMA, HMA, KAMA, VIDYA, DEMA, TEMA, ALMA) and lag trade-offs
212. Moving-average crossovers, ribbons, and multi-MA systems
213. Donchian channels and the turtle-style breakout
214. ADX, +DI/-DI, and trend-strength measurement
215. Parabolic SAR and trailing-stop systems
216. Supertrend and ATR-based trend filters
217. Aroon, Vortex, and trend-direction indicators
218. Ichimoku Cloud (components, rules, and testing)
219. Time-series momentum and its theoretical link to trend following
220. Trend-regime filters (e.g., price versus 200-day average)

### 5.3 Momentum and oscillators
221. RSI (levels, divergence, failure swings, Connors RSI)
222. Stochastic oscillator (fast, slow, full)
223. MACD (signal line, histogram, divergence)
224. CCI, Williams %R, Ultimate Oscillator
225. ROC, momentum, TRIX, and PPO
226. Awesome Oscillator and Elder-ray
227. Money Flow Index and volume-weighted oscillators
228. Divergence detection (regular and hidden) and quantifying it algorithmically
229. Overbought/oversold fallacy in trending markets
230. Oscillator parameter dependence and adaptive-length versions

### 5.4 Volatility and range indicators
231. ATR, true range, and volatility-normalized stops
232. Bollinger Bands, %B, bandwidth, and squeeze setups
233. Keltner and STARC bands
234. Standard-deviation channels and linear-regression channels
235. Historical, realized, and implied-volatility comparison
236. Volatility breakouts and compression-expansion cycles
237. Chaikin volatility and Ulcer-index-style measures
238. Volatility regime classification for strategy switching

### 5.5 Volume, order flow, and market breadth
239. Volume analysis basics (volume confirmation, climaxes, dry-ups)
240. OBV, accumulation/distribution, Chaikin Money Flow
241. VWAP, anchored VWAP, and volume-weighted bands
242. Volume profile (POC, value area, HVN/LVN) and market profile (TPO)
243. Footprint charts, delta, cumulative delta, and absorption
244. Order-book heatmaps and DOM reading (with the spoofing caveat)
245. Open interest and futures positioning interpretation
246. Breadth indicators (advance/decline line, McClellan, TRIN, % above moving average, new highs/new lows)
247. Sector and index participation analysis
248. Put/call ratios, VIX-term structure, and sentiment-based contrarian indicators

### 5.6 Price patterns
249. Support, resistance, and role reversal; zone vs. line formulation
250. Candlestick patterns (doji, hammer, engulfing, morning/evening star, etc.) and statistical performance
251. Classical chart patterns (head-and-shoulders, double top/bottom, triangles, flags, wedges, rectangles, cup-and-handle)
252. Gaps (common, breakaway, runaway, exhaustion) and gap-fill behavior
253. Pivot points (classic, Fibonacci, Camarilla, Woodie)
254. Opening-range, initial-balance, and previous-day-high/low levels
255. Round-number and psychological levels
256. Swing-point detection algorithms (zigzag, fractals, rolling extremes)
257. Algorithmic pattern recognition (template matching, dynamic time warping, CNN-based detection)
258. Pattern failure rates, measured-move targets, and statistical edge verification

### 5.7 Fibonacci, wave, and geometric methods (critical evaluation)
259. Fibonacci retracement, extension, and clusters
260. Elliott Wave counting and its non-falsifiability problem
261. Gann angles, squares, and time cycles
262. Harmonic patterns (Gartley, Bat, Butterfly, Crab)
263. Wyckoff method (accumulation, distribution, springs, upthrusts)
264. Dow Theory and its modern interpretation
265. Cycle analysis (Fourier, wavelet, Hilbert transform, dominant-cycle detection)
266. Fractals, Hurst exponent, and multifractal market models
267. Testing geometric methods statistically (and why many fail)

### 5.8 Multi-timeframe, intermarket, and relative analysis
268. Top-down multi-timeframe alignment (higher-timeframe filter, lower-timeframe entry)
269. Relative strength and ratio charts (stock vs. index, sector vs. market)
270. Intermarket relationships (stocks, bonds, dollar, commodities)
271. Sector rotation using relative-strength ranking
272. Cross-asset confirmation and divergences
273. Correlation regime changes and their impact on technical signals
274. Seasonality, calendar effects, and time-of-day patterns (turn-of-month, expiry week, intraday U-shape)

### 5.9 Systematic implementation of technical rules
275. Converting indicators to rules (entry, exit, filter, and position-sizing logic)
276. Signal definition pitfalls (repainting indicators, look-ahead in pivots, current-bar leakage)
277. Indicator parameter selection and overfitting risk (parameter plateaus, walk-forward optimization)
278. Combining indicators (redundancy, multicollinearity among oscillators, confirmation vs. diversification)
279. Stop-loss and trailing-stop design (fixed, ATR, chandelier, structure-based)
280. Profit-target design and scaling-out rules
281. Technical signals as ML features (indicator feature engineering, stationarity, scaling)
282. Technical analysis for intraday vs. swing vs. position horizons
283. Technical rules by asset class and instrument behavior (futures, FX, equities, crypto)
284. Library and implementation inconsistencies (TA-Lib vs. pandas-ta vs. platform-native outputs)
285. Auditing indicator correctness against reference platforms

### 5.10 Evidence, testing, and critique of technical analysis
286. Academic evidence (Brock-Lakonishok-LeBaron, Lo-Mamaysky-Wang, and subsequent replications)
287. Data-snooping across thousands of technical rules (White's Reality Check applied to TA)
288. Transaction-cost sensitivity of high-turnover technical systems
289. Regime dependence (trend systems vs. mean-reverting regimes)
290. Self-fulfilling-prophecy hypothesis and crowding at popular levels
291. Survivorship in published technical-analysis "successes"
292. Behavioral explanations (anchoring, herding, disposition effect, under-reaction)
293. Technical analysis in algorithmic markets: who is on the other side?

### 5.11 Combining fundamental and technical analysis
294. Fundamental screen, technical timing (quality/value universe with momentum entry)
295. Technical filter as a risk overlay on fundamental portfolios
296. Combining value and momentum (negative correlation and diversification benefits)
297. Event-driven entries (earnings, catalysts) with technical confirmation
298. Fundamental regime plus technical signal (macro state gates technical systems)
299. Multi-signal scoring frameworks and weighting schemes
300. Evaluating whether the combination adds incremental alpha (ablation and marginal contribution)
301. Conflict-resolution rules when fundamental and technical signals disagree

## PART 6. Sentiment, News, and Alternative Data

### 6.1 Text, news, and alternative-data signals
302. News ingestion pipelines (wires, RSS, APIs, social media)
303. Entity recognition and ticker mapping
304. Event detection (earnings, M&A, guidance, central bank, macro releases)
305. Sentiment scoring (lexicon, FinBERT, LLM-based)
306. Social media signals (Twitter/X, Reddit, StockTwits, Telegram)
307. Earnings call and SEC filing analysis (10-K, 10-Q, 8-K)
308. Economic calendar ingestion and macro-surprise modeling
309. Alternative data (satellite, web traffic, app data, card spend, shipping, job postings)
310. Search trends and attention measures
311. News latency, timestamp accuracy, point-in-time handling
312. Signal decay and crowding for sentiment strategies
313. Fake news, manipulation, and bot filtering

## PART 7. Strategy Design

### 7.1 Strategy families
314. Trend following and CTA-style systems
315. Mean reversion and statistical arbitrage
316. Pairs and basket trading
317. Cross-sectional momentum and factor investing
318. Carry strategies
319. Volatility strategies
320. Event-driven and earnings strategies
321. Index, ETF, and basis arbitrage
322. Market-neutral and long-short
323. Intraday, scalping, opening-range strategies
324. Market making
325. Tail-hedging and convex strategies
326. Systematic macro and cross-asset
327. Multi-asset and multi-venue arbitrage

### 7.2 Instrument selection and scoring
328. Universe construction and screening
329. Liquidity filters (ADV, spread, depth)
330. Technical and momentum scoring
331. Multi-factor composite scores and z-score normalization
332. Cross-sectional ranking and long-short construction
333. Pair and basket selection (distance, cointegration, clustering)
334. Sector and industry rotation
335. Futures contract selection (roll rules, continuous contracts, carry)
336. Option contract selection (strike, expiry, delta targeting, liquidity)
337. Dynamic universe changes, delisting, survivorship handling

### 7.3 Trade management and strategy logic
338. Entry, exit, stop-loss, and take-profit logic design
339. Time-based, volatility-based, and signal-reversal exits
340. Signal-to-order translation (target-position vs. delta-order models)
341. Strategy parameter management and regime-dependent parameters
342. Strategy SDK and plugin interface (a uniform contract for all strategies)
343. Scheduler, event bus, and session lifecycle (pre-open, open, close, post-close)
344. Manual override and human-in-the-loop controls (four-eyes approval)
345. Alpha combination and signal blending (ensemble, stacking)

### 7.4 Market microstructure and market theory (MMT)
346. Market Microstructure Theory (Kyle, Glosten-Milgrom, Almgren-Chriss)
347. Order flow imbalance, VPIN, toxicity
348. Bid-ask bounce and effective spread decomposition
349. Queue position and limit order book dynamics
350. Market impact models (square-root law, permanent vs. temporary)
351. Inventory models for market making (Avellaneda-Stoikov)
352. Adverse selection and latency arbitrage
353. Modern Portfolio Theory, its critiques, and the Adaptive Market Hypothesis
354. Efficient Market Hypothesis and behavioral finance

## PART 8. Artificial Intelligence and Machine Learning

### 8.1 Machine learning
355. Supervised learning (linear models, SVM, k-NN)
356. Tree ensembles (Random Forest, XGBoost, LightGBM, CatBoost)
357. Unsupervised learning (k-means, hierarchical, DBSCAN, GMM)
358. Dimensionality reduction (PCA, ICA, autoencoders, t-SNE, UMAP)
359. Financial labeling (triple barrier, meta-labeling)
360. Sample weighting, uniqueness, sequential bootstrap
361. Purged/embargoed and combinatorial purged cross-validation
362. Feature engineering, selection, and importance (MDI, MDA, SHAP)
363. Hyperparameter optimization and its overfitting danger
364. Class imbalance and probability calibration
365. Concept drift, model decay, retraining policy
366. Online and incremental learning
367. Explainability and model governance
368. MLOps (feature stores, model registry, monitoring, reproducibility)

### 8.2 Deep learning
369. Feed-forward networks and regularization
370. RNN, LSTM, GRU for sequences
371. Temporal CNNs and WaveNet-style models
372. Transformers and attention for time series
373. Temporal Fusion Transformer, N-BEATS, PatchTST
374. Deep learning on limit order books (DeepLOB)
375. Graph neural networks for asset relationships
376. Generative models (GANs, VAEs, diffusion) for synthetic data
377. Autoencoders for anomaly detection and denoising
378. Foundation and pretrained time-series models
379. Uncertainty estimation (MC dropout, ensembles, conformal prediction)
380. Training under low signal-to-noise ratio

### 8.3 Reinforcement learning
381. MDP formulation for trading (state, action, reward design)
382. Q-learning and DQN
383. Policy gradient, A2C, PPO, SAC, DDPG, TD3
384. Reward shaping (risk-adjusted, drawdown-penalized, cost-aware)
385. Trading environment simulation (Gym-style, realistic fills)
386. RL for optimal execution
387. RL for market making
388. RL for portfolio allocation and dynamic hedging
389. Multi-agent RL and market simulation
390. Sim-to-real gap and non-stationarity
391. Offline RL and safe/constrained RL

### 8.4 Generative AI and LLM agents
392. LLMs for financial text understanding
393. Retrieval-augmented generation over filings and research
394. LLM agents for research, strategy ideation, and code generation
395. Agentic trading workflows with guardrails and human approval
396. Prompt design, evaluation, hallucination control
397. Backtesting LLM signals without look-ahead (knowledge-cutoff leakage)
398. Cost, latency, and reproducibility of LLM pipelines

## PART 9. Derivatives and Other Products

### 9.1 Options
399. Black-Scholes-Merton and its assumptions
400. Greeks (delta, gamma, vega, theta, rho, vanna, volga, charm)
401. Implied volatility surfaces, smile, skew
402. Volatility models (local vol, SABR, Heston, SVI)
403. Binomial/trinomial trees, PDE and Monte Carlo pricing
404. American options and early exercise
405. Delta and gamma hedging, dynamic hedging costs
406. Volatility trading (straddles, strangles, variance swaps, dispersion)
407. Spread strategies (verticals, calendars, butterflies, condors, ratios)
408. Income strategies (covered calls, cash-secured puts, wheel)
409. Volatility risk premium and term structure
410. Skew, term-structure, and calendar arbitrage
411. Put-call parity and arbitrage checks
412. Options on futures and index options (settlement, European vs. American)
413. Expiry mechanics, pin risk, assignment risk
414. Margin and portfolio margin for options
415. Exotics and structured products (barriers, Asians, digitals)

### 9.2 Futures, fixed income, and FX
416. Futures, forwards, swaps (basis, carry, contango, backwardation)
417. Fixed income and rates (duration, convexity, yield curves)
418. FX specifics (carry, triangular arbitrage, forwards, rollover)

### 9.3 Additional asset classes and products
419. Commodities (storage, seasonality, delivery, and physical-settlement risk)
420. ETFs and ETNs (tracking error, premium/discount, leveraged ETF decay)
421. Volatility products (VIX futures, VIX ETPs, roll-yield decay)
422. Credit (bonds, CDS, spreads, and default modeling)
423. Convertibles and warrants
424. Prediction markets
425. Weekly and zero-days-to-expiry options (0DTE) behavior

### 9.4 Crypto and DeFi
426. Crypto derivatives (perpetuals, funding rates, liquidations)
427. Crypto specifics (DEX/CEX integration, custody, on-chain data)
428. AMM mechanics, impermanent loss, and LP strategies
429. MEV, front-running, and sandwich attacks
430. Stablecoin depeg risk
431. Bridge and smart-contract risk
432. Exchange proof-of-reserves and counterparty risk
433. Tokenized assets and 24/7 market dynamics
434. On-chain order books and settlement finality

## PART 10. Research, Backtesting, and Validation

### 10.1 Research process
435. Hypothesis-driven research workflow
436. Experiment tracking and reproducibility
437. Strategy lifecycle (idea, prototype, incubation, live, retirement)

### 10.2 Backtesting
438. Backtesting engines (event-driven, vectorized)
439. Avoiding bias (look-ahead, survivorship, overfitting, data leakage)
440. Slippage, fees, and market-impact modeling
441. Walk-forward analysis, cross-validation, Monte Carlo simulation
442. Signal decay, turnover, and capacity analysis
443. Crowding and capacity estimation

### 10.3 Simulation and pre-production validation
444. Agent-based market simulation
445. Synthetic and bootstrapped price-path generation
446. Fill-model calibration against live execution data
447. Historical replay and deterministic simulation
448. Shadow trading and canary deployment
449. Gradual capital ramp-up and champion/challenger live testing
450. Backtest-to-live code parity (a single codebase for research and production)

### 10.4 Statistical robustness of reported results
451. Out-of-sample vs. in-sample reporting separation
452. Parameter sensitivity and robustness surfaces (heatmaps, plateau vs. spike)
453. Performance stability across subperiods
454. Monte Carlo reshuffling of trades and returns
455. Bootstrap confidence bands on equity curves and on the Sharpe ratio itself
456. Number-of-trials accounting and selection-bias disclosure
457. Statistical significance of alpha (t-stats and their limits)
458. Regime-robustness checks (crisis periods, low-vol periods, rate regimes)
459. Cost-sensitivity analysis (performance under doubled slippage and fees)
460. Capacity-sensitivity analysis (performance as AUM scales)
461. Latency-sensitivity analysis

## PART 11. Portfolio Construction and Capital Allocation

### 11.1 Portfolio construction and optimization
462. Mean-variance optimization (Markowitz) and its instability
463. Black-Litterman model
464. Risk parity and equal risk contribution
465. Hierarchical Risk Parity and HERC
466. Minimum variance and maximum diversification
467. CVaR and CDaR optimization
468. Robust and resampled optimization
469. Factor-based construction (CAPM, Fama-French, APT, custom factors)
470. Constraints (turnover, sector, leverage, cardinality, liquidity)
471. Transaction-cost-aware optimization
472. Multi-period and dynamic optimization
473. Strategy-level allocation (portfolio of strategies)
474. Capital allocation across asset classes and regimes
475. Rebalancing policy (calendar, threshold, tactical)

### 11.2 Position keeping and reconciliation
476. Position keeping, accounting, P&L attribution
477. Reconciliation with broker statements

### 11.3 Factor and risk-model concepts
478. Risk models (Barra-style fundamental, statistical, and hybrid factor models)
479. Factor zoo problem and factor-crowding risk
480. Hedging (minimum-variance hedge ratio, beta, cross-hedging, basis risk)
481. Dollar-, beta-, and sector-neutral construction
482. Tracking error, active share, and information ratio
483. Smart beta and index methodology
484. ESG integration and constraints

### 11.4 Position sizing and fund allocation
485. Fixed fractional and fixed ratio sizing
486. Kelly criterion, fractional Kelly, multi-asset Kelly
487. Volatility targeting and ATR-based sizing
488. Risk-per-trade and stop-distance sizing
489. Optimal f (Vince)
490. Equity-curve-based sizing and anti-martingale scaling
491. Capital allocation across strategies (static, dynamic, performance-weighted)
492. Cash and margin buffer policy
493. Pyramiding, scaling in and out
494. Leverage policy and margin-call avoidance
495. Drawdown-dependent de-risking
496. Fund-level mechanics (subscriptions, redemptions, NAV, fees, high-water mark)

## PART 12. Risk Management

### 12.1 Pre-trade and real-time controls
497. Pre-trade checks (position, exposure, fat-finger limits)
498. Real-time P&L and exposure monitoring
499. Kill switches and circuit breakers

### 12.2 Risk measures, stress testing, and exposures
500. VaR methods (historical, parametric, Monte Carlo) and VaR backtesting (Kupiec, Christoffersen)
501. Expected Shortfall
502. Scenario analysis and historical stress tests
503. Reverse stress testing
504. Drawdown control and loss-limit rules
505. Correlation breakdown and tail risk
506. Liquidity risk and market-impact risk
507. Counterparty, settlement, and exchange risk
508. Model risk and parameter uncertainty
509. Concentration and factor-exposure risk
510. Risk budgeting and risk attribution
511. Greeks-based risk for derivatives books
512. Gap, overnight, and weekend risk
513. Operational risk and fat-finger scenarios
514. Risk of ruin

### 12.3 Margin, leverage, and funding risk
515. Portfolio and margin management
516. SPAN and exchange margin methodology
517. Cross-margining and intraday margin
518. Broker insolvency and custody risk
519. Funding-liquidity risk and liquidity-adjusted VaR

## PART 13. Execution

### 13.1 Execution engine
520. Order Management System (OMS)
521. Execution Management System (EMS)
522. Smart order routing and execution algos (TWAP, VWAP, POV, iceberg)
523. Broker and exchange connectivity (FIX, REST, WebSocket)
524. Order state machine, retries, idempotency, reconciliation
525. Paper trading and simulated exchange
526. High-frequency and low-latency optimization (FPGA, kernel bypass)

## PART 14. Costs, Taxes, and Accounting

### 14.1 Costs, taxes, and accounting
527. Funding, financing, and margin costs
528. Commission structures, brokerage tiers, and exchange fees
529. Maker-taker rebates and fee-tier optimization
530. Taxes (transaction taxes such as STT, capital gains, GST, stamp duty)
531. Borrow fees and short-rebate economics
532. Total cost of ownership (data, infrastructure, staff, and compliance)
533. Multi-currency accounting, FX conversion, and base-currency reporting
534. Cash management, interest accrual, and margin interest
535. Settlement cycles (T+1/T+2), settlement fails, custody, and clearing
536. Time-weighted vs. money-weighted returns, log vs. simple returns, annualization conventions

## PART 15. Performance and Analytics

### 15.1 Return measurement fundamentals
537. Simple vs. log returns, and when each is valid (aggregation across time vs. across assets)
538. Compounding, geometric vs. arithmetic mean, and volatility drag
539. Annualization conventions (252 vs. 365, calendar vs. trading days, irregular sampling)
540. Time-weighted return (TWR) vs. money-weighted return (MWR/IRR)
541. Handling cash flows, deposits, and withdrawals in return calculation
542. Gross vs. net returns (before and after costs, fees, and taxes)
543. Mark-to-market vs. realized P&L, and unrealized P&L treatment
544. Intraday vs. end-of-day P&L, and valuation price choice (last, mid, settlement, VWAP)
545. Handling stale prices and illiquid-asset valuation
546. Multi-currency returns (local vs. base currency, FX contribution)
547. Return decomposition (price, carry, dividend, financing, FX)
548. Leverage-adjusted and notional vs. capital-based return denominators
549. Return on margin vs. return on capital vs. return on risk

### 15.2 Risk-adjusted performance metrics
550. Sharpe ratio and its assumptions (normality, i.i.d., stationarity)
551. Sortino ratio and the choice of minimum acceptable return
552. Calmar, Sterling, and Burke ratios
553. Information ratio and tracking error
554. Treynor ratio and Jensen's alpha
555. Omega ratio and Kappa ratios
556. Ulcer Index, Martin ratio, and pain ratio
557. Tail ratio, gain-to-pain ratio, and profit factor
558. Higher-moment-adjusted metrics (skew and kurtosis-aware)
559. Risk-adjusted metric disagreement: why rankings change across metrics
560. Metric gaming: how each metric can be inflated (selling tails, smoothing, short track records)

### 15.3 Drawdown and path analysis
561. Maximum drawdown, average drawdown, and drawdown duration
562. Time to recovery and underwater curves
563. Drawdown distribution via Monte Carlo and bootstrap
564. Expected maximum drawdown under different return models
565. Drawdown clustering and conditional drawdown
566. Equity-curve smoothness and linearity (R-squared of the equity curve)
567. Rolling windows (rolling Sharpe, volatility, drawdown, beta)
568. Path dependence and order-of-returns risk

### 15.4 Trade-level analytics
569. Win rate, average win/loss, payoff ratio, and expectancy
570. Trade distribution (histograms, outlier dependence, fat-tail contribution)
571. Reliance on top-N trades (what the P&L looks like without the best 5 trades)
572. MAE/MFE analysis and exit-efficiency analysis
573. Holding-period analysis and time-in-market
574. Streak analysis (consecutive wins/losses) and serial dependence of trades
575. Trade clustering by time of day, weekday, month, and event
576. Entry and exit timing quality (edge ratio, entry efficiency)
577. Slippage per trade and fill-quality statistics
578. Long vs. short side contribution and asymmetry
579. Per-instrument, per-sector, and per-strategy contribution
580. Turnover and trade frequency vs. net return relationship

### 15.5 Performance attribution
581. Brinson attribution (allocation, selection, interaction)
582. Factor-based attribution (market, size, value, momentum, quality, low-vol)
583. Alpha vs. beta decomposition and residual alpha significance
584. Strategy-level and signal-level attribution
585. Risk-contribution attribution (marginal and component risk)
586. Timing vs. selection vs. sizing attribution
587. Carry, roll, and convexity attribution for futures and options
588. Greeks-based P&L attribution for options (delta, gamma, vega, theta, and unexplained residual)
589. Cost attribution (commissions, spread, impact, financing, taxes)
590. Regime-conditional attribution (performance by volatility, trend, and macro regime)
591. Attribution across multi-currency books
592. Reconciling attribution to actual P&L (the unexplained residual and what it signals)

### 15.6 Benchmarking and comparison
593. Benchmark selection (market, peer, risk-matched, custom blended)
594. Beta-adjusted and style-adjusted benchmarks
595. Correlation to benchmarks, strategies, and common risk factors
596. Up-capture and down-capture ratios
597. Peer-group and universe comparison
598. Replication and naive-baseline comparison (does the strategy beat buy-and-hold, equal-weight, or a simple trend rule?)
599. Hurdle rates, risk-free rate selection, and cash comparison

### 15.7 Live monitoring and degradation detection
600. Live vs. backtest vs. paper tracking-error dashboards
601. Expected-vs-realized distribution tests (is the live drawdown within the backtest envelope?)
602. Change-point detection on strategy returns (CUSUM, Bayesian)
603. Alpha-decay monitoring, half-life estimation, and alpha capture
604. Execution-quality drift (slippage, fill rate, reject rate over time)
605. Model and signal drift metrics (feature distribution shift, PSI, KS tests)
606. Hit-rate and information-coefficient (IC) decay tracking
607. Automated strategy health scores and traffic-light rules
608. Strategy retirement and throttling criteria based on analytics
609. Alert thresholds and false-alarm control

### 15.8 Execution and cost analytics (TCA)
610. Implementation shortfall decomposition
611. Arrival-price, VWAP, TWAP, and close benchmarks
612. Spread capture, adverse selection, and markout analysis
613. Market-impact estimation from own trades
614. Fill-rate, passive vs. aggressive mix, and venue analysis
615. Broker and algo comparison
616. Latency analytics (signal-to-order, order-to-ack, ack-to-fill)
617. Opportunity cost and unfilled-order analysis
618. Pre-trade cost estimates vs. realized cost reconciliation

### 15.9 Portfolio-level analytics
619. Exposure analytics (gross, net, long, short, beta-adjusted, sector, country, currency)
620. Concentration metrics (top-N weights, Herfindahl index, effective number of bets)
621. Correlation structure and diversification ratio over time
622. Risk decomposition (systematic vs. idiosyncratic, factor risk)
623. Liquidity profile (days to liquidate, ADV participation)
624. Leverage, margin utilization, and buying-power history
625. Turnover, holding-period, and capacity analytics
626. Greeks and scenario exposure dashboards for derivative books
627. Realized vs. forecast volatility and risk-model calibration checks
628. VaR and Expected Shortfall exceedance reporting

### 15.10 Signal and model analytics
629. Information coefficient (IC), rank IC, and IC information ratio
630. Quantile (decile) return analysis and monotonicity checks
631. Signal turnover, autocorrelation, and decay curves
632. Signal correlation matrix and marginal contribution to the blend
633. Feature importance stability over time
634. Prediction calibration and reliability diagrams
635. Hit rate vs. magnitude accuracy (directional vs. sizing quality)
636. Error analysis (when and where does the model fail)
637. Ablation studies and incremental-value tests

### 15.11 Reporting and communication
638. Tear sheets (standard one-page strategy and portfolio summaries)
639. Daily, weekly, and monthly reporting cadences and content
640. Investor, board, and risk-committee reports
641. Regulatory and audit reporting packs
642. Honest-disclosure standards (GIPS-style composites, hypothetical vs. live labeling)
643. Visualization best practices (equity curve on log scale, underwater plots, heatmaps, return histograms)
644. Interactive drill-down dashboards (portfolio to strategy to trade to fill)
645. Narrative commentary: explaining why performance happened, not just what
646. Report reproducibility, versioning, and traceability to source data
647. Tax-lot and tax-aware performance reporting

### 15.12 Analytics infrastructure
648. Analytics data model (fills, orders, positions, P&L, prices, reference data)
649. Point-in-time P&L engine and position reconstruction
650. Reconciliation of analytics with broker and exchange records
651. Metric definition registry (one agreed definition per metric across the firm)
652. Batch vs. streaming analytics pipelines
653. Data lineage and audit trail for every reported number
654. Performance-calculation unit testing and golden-dataset validation
655. Analytics library selection and its pitfalls (differing Sharpe or drawdown conventions across libraries)

## PART 16. Architecture, Engineering, and Security

### 16.1 System architecture and infrastructure
656. Architecture styles (monolith, microservices, event-driven)
657. Latency vs. throughput trade-offs
658. Messaging and streaming (Kafka, Redis Streams, ZeroMQ)
659. Language choices (Python, C++, Rust, Java)
660. Deployment (Docker, Kubernetes, cloud, co-location)
661. API design (REST, gRPC, WebSocket) and rate limiting
662. Databases (relational, time-series, caches)
663. Concurrency, async programming, fault tolerance
664. Configuration and secrets management

### 16.2 Advanced systems engineering
665. Event sourcing, CQRS, snapshots, and state recovery
666. Serialization and schema evolution (Protobuf, Avro, SBE)
667. Order-book data structures and algorithmic complexity
668. Lock-free structures, memory management, garbage-collection pauses, and profiling
669. Numerical precision (floating point vs. decimal arithmetic for money)
670. Time handling (leap seconds, DST, monotonic clocks)
671. Idempotent messaging, exactly-once vs. at-least-once semantics
672. Feature flags, versioned APIs, and configuration drift
673. Multi-tenancy, scalability, and cost control in the cloud
674. Vendor lock-in and broker abstraction layers

### 16.3 Software engineering practices
675. Version control, branching strategy, and code review
676. Reproducible environments and dependency management
677. Property-based testing, fuzzing, and backtest regression testing
678. Exchange simulator conformance testing
679. Technical-debt management and documentation standards
680. Domain-driven design for trading systems

### 16.4 Frontend and user experience
681. Dashboards (charts, order entry, blotters, positions)
682. Real-time UI (React, WebSockets, charting libraries)
683. Alerts and notifications
684. Strategy configuration and monitoring UIs
685. Visualization and interactive research notebooks

### 16.5 Reliability and operations (technical)
686. Monitoring, logging, observability (Prometheus, Grafana, ELK)
687. Incident response and alerting
688. Disaster recovery, failover, high availability
689. Testing (unit, integration, replay, chaos)
690. CI/CD and safe release practices

### 16.6 Security
691. Authentication, authorization, API key management
692. Encryption in transit and at rest
693. Secure credential storage
694. Access control, audit logs, fraud prevention
695. Threat modeling for trading systems

## PART 17. Operations, Governance, Legal, and Business

### 17.1 Operations and desk processes
696. Runbooks, on-call rotations, and post-mortems
697. Change management and release approvals
698. Middle- and back-office workflows (confirmations, reconciliation, breaks)
699. Corporate-action elections and proxy handling
700. Business continuity planning and key-person risk
701. Vendor and service-level agreement management

### 17.2 Regulation, compliance, and audit
702. Regulation and compliance (MiFID II, SEC/FINRA, KYC/AML, audit trails)
703. Ethics and manipulation boundaries (spoofing, layering, wash trading)
704. Record retention and best-execution evidence
705. Market-abuse surveillance (self-monitoring for spoofing and layering)
706. SOC 2, ISO 27001, and audit readiness
707. GDPR and data privacy
708. Intellectual property protection for strategies and open-source licensing
709. Insurance (errors and omissions, cyber, fidelity)
710. AI governance (explainability requirements, model-risk regulation, and AI regulatory frameworks)

### 17.3 Governance and model oversight
711. Model validation and independent review
712. Investment and risk committee processes
713. Documentation and decision logs

### 17.4 Business and legal structure
714. Legal structure (prop, fund, RIA, CTA, CPO)
715. Counterparty and prime brokerage selection
716. Business model, fees, licensing
717. Capital raising and investor relations

### 17.5 Product and platform features (if multi-user)
718. User roles, permissions, and tenant isolation
719. Customer onboarding, suitability checks, and disclosures
720. Strategy marketplace, copy trading, and social trading
721. White-label and broker-integration marketplace
722. Billing, subscriptions, and customer support
723. Mobile and notification delivery reliability
724. Terms of service and liability limits

## PART 18. Human Factors, Case Studies, Emerging Topics, and Prerequisites

### 18.1 Behavioral considerations
725. Trader psychology and discipline (discretionary or hybrid systems)
726. Behavioral biases and market anomalies

### 18.2 Case studies in failure
727. Knight Capital (deployment and kill-switch failure)
728. LTCM (leverage and correlation risk)
729. 2007 Quant Quake and crowded quant positions
730. 2010 Flash Crash
731. Volmageddon (2018 short-volatility collapse)
732. Archegos (hidden leverage and concentrated swaps)
733. GameStop and short-squeeze dynamics
734. Terra/Luna and FTX collapses (crypto custody and design failures)
735. Common pattern analysis (leverage, crowding, no kill switch, untested assumptions)

### 18.3 Emerging topics
736. T+0 settlement and tokenized securities
737. Quantum computing for optimization
738. Synthetic data and privacy-preserving research
739. Federated and decentralized data sharing
740. Hardware acceleration beyond FPGA (GPU-based simulation and inference)

### 18.4 Prerequisites and learning path
741. Python, NumPy, pandas, and SQL fundamentals
742. Linux, Git, and cloud basics
743. Probability and linear algebra refresher
744. Financial accounting basics
745. Capstone project design (end-to-end paper-trading system)
746. Reading list (core quant textbooks, papers, and post-mortems)


## Suggested Build Order
1. Parts 1, 3, 16: foundations, data, and infrastructure.
2. Parts 2, 10: statistical rigor, backtesting, and validation.
3. Parts 4, 5, 6, 7: fundamental, technical, and alternative-data signals, then strategy design.
4. Parts 11, 12, 14: portfolio, sizing, risk, and costs.
5. Part 13: execution.
6. Part 15: performance and analytics, with live monitoring.
7. Parts 8, 9: ML/DL/RL/LLMs and derivatives, added after a simple baseline exists.
8. Parts 17, 18: operations, governance, case studies, and prerequisites.
