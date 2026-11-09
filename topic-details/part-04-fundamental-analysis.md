# Part 4. Fundamental Analysis: Micro Details (topics 97 to 200)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 4.1 Financial statement foundations

97. Income statement structure and line-item quality (revenue recognition, operating vs. non-operating items)
    - Covers: revenue down to net income.
    - Details: separate operating profit from financing, tax, and one-off items. Revenue recognition policy drives timing.
    - Pitfall: using net income that includes gains or losses unrelated to the core business.
    - Build: a standardized income statement template that splits recurring and non-recurring items.

98. Balance sheet structure (assets, liabilities, equity, off-balance-sheet items)
    - Covers: financial position at a date.
    - Details: current vs. non-current split, working capital, leases, contingent liabilities, and special-purpose structures.
    - Pitfall: ignoring off-balance-sheet obligations.
    - Build: an adjusted balance sheet adding lease and pension obligations.

99. Cash flow statement (operating, investing, financing, and the indirect vs. direct method)
    - Covers: cash movements by activity.
    - Details: the indirect method starts from net income and adjusts for non-cash items and working-capital changes. Free cash flow = operating cash flow - capital expenditure.
    - Pitfall: classifying capitalized costs as investing to inflate operating cash flow.
    - Build: a free-cash-flow calculation checked against reported cash change.

100. Articulation between the three statements
     - Covers: how the statements tie together.
     - Details: net income flows to retained earnings, cash flow ties to the change in cash, working-capital changes tie to balance-sheet items.
     - Pitfall: a model whose statements do not reconcile.
     - Build: a three-statement integrity check that flags non-balancing periods.

101. Accounting standards differences (GAAP vs. IFRS vs. local standards such as Ind AS)
     - Covers: rule differences that change reported numbers.
     - Details: inventory methods, development-cost capitalization, lease treatment, and impairment reversals differ.
     - Pitfall: comparing companies reporting under different standards without adjustment.
     - Build: a list of the standard-specific adjustments you apply per market.

102. Segment reporting and geographic breakdowns
     - Covers: breakdown of revenue and profit by business or region.
     - Details: reveals the mix of growth and margin drivers and exposure to specific currencies or economies.
     - Pitfall: segment definitions change and break comparability.
     - Build: a segment time series with mapping across definition changes.

103. Footnotes, MD&A, and risk-factor sections
     - Covers: narrative and detail disclosures.
     - Details: footnotes show accounting policies, debt terms, contingencies, and related-party items. MD&A explains management's view.
     - Pitfall: reading only the statements and skipping the footnotes.
     - Build: a checklist of footnote items to extract each quarter.

104. Quarterly vs. annual vs. trailing-twelve-month (TTM) data, seasonality adjustment
     - Covers: time-window choices.
     - Details: TTM = sum of the last four quarters. Seasonal businesses need year-over-year comparison, not sequential.
     - Pitfall: comparing a seasonal quarter with the previous quarter.
     - Build: TTM and YoY calculation functions with fiscal-calendar handling.

105. Restatements, reclassifications, and amended filings
     - Covers: changes to previously reported numbers.
     - Details: store original and restated values with dates. Restatements can signal accounting problems.
     - Pitfall: backtesting on restated numbers not known at the time.
     - Build: a store keeping each filing version with its filing date.

106. Standardizing and normalizing financials across companies and sectors
     - Covers: making companies comparable.
     - Details: map line items to a common chart of accounts. Adjust for leases, one-offs, and stock compensation.
     - Pitfall: vendor standardization that hides sector-specific items.
     - Build: a mapping table with sector overrides and a documented adjustment list.

107. Point-in-time fundamentals (reporting lag, avoiding look-ahead on filing dates)
     - Covers: availability timing.
     - Details: data becomes usable on the filing date plus processing lag, not on the fiscal period end.
     - Pitfall: using Q4 numbers in January when they were filed in March.
     - Build: a point-in-time dataset with a test that no field is used before its filing date.

## 4.2 Ratio analysis

108. Profitability ratios (gross, operating, net margin, ROE, ROA, ROIC, ROCE)
     - Covers: how efficiently a company earns profit.
     - Details: ROIC = NOPAT / invested capital. ROE = net income / equity. Compare ROIC with the cost of capital.
     - Pitfall: ROE inflated by leverage or buybacks that shrink equity.
     - Build: a ratio panel with ROIC vs. WACC spread.

109. DuPont decomposition (3-step and 5-step)
     - Covers: breaking ROE into drivers.
     - Details: 3-step: ROE = net margin x asset turnover x equity multiplier. 5-step adds tax burden and interest burden.
     - Pitfall: attributing ROE changes to operations when leverage changed.
     - Build: a DuPont table across years for one company.

110. Liquidity ratios (current, quick, cash)
     - Covers: ability to pay short-term obligations.
     - Details: current = current assets / current liabilities. Quick excludes inventory.
     - Pitfall: using one threshold for all sectors.
     - Build: sector-relative liquidity percentiles.

111. Leverage and solvency ratios (debt/equity, net debt/EBITDA, interest coverage, Altman Z)
     - Covers: debt burden and survival risk.
     - Details: interest coverage = EBIT / interest expense. Net debt/EBITDA shows years of earnings to repay debt.
     - Pitfall: ignoring lease and off-balance-sheet debt.
     - Build: a leverage dashboard including lease-adjusted debt.

112. Efficiency ratios (asset turnover, inventory days, receivable days, payable days, cash conversion cycle)
     - Covers: working-capital management.
     - Details: cash conversion cycle = inventory days + receivable days - payable days.
     - Pitfall: year-end window dressing distorts the ratios.
     - Build: trend charts of each day-count over eight quarters.

113. Growth metrics (revenue, EPS, FCF, book value growth; CAGR; consistency and acceleration)
     - Covers: pace and quality of growth.
     - Details: CAGR = (end / start)^(1/years) - 1. Look at consistency and second derivative (acceleration).
     - Pitfall: growth from acquisitions presented as organic growth.
     - Build: organic vs. total growth split where disclosed.

114. Per-share metrics and dilution effects (EPS, diluted EPS, buybacks, ESOPs)
     - Covers: per-share accounting.
     - Details: diluted EPS includes options and convertibles. Buybacks raise EPS even with flat net income.
     - Pitfall: EPS growth driven by share count reduction funded by debt.
     - Build: EPS growth split into net-income growth and share-count change.

115. Industry-specific metrics (banks: NIM, NPA, CASA, CAR; insurers: combined ratio; REITs: FFO; retail: same-store sales; SaaS: ARR, churn, NRR; airlines: RASK/CASK)
     - Covers: sector KPIs.
     - Details: generic ratios mislead for banks, insurers, and asset-heavy sectors. Use the metrics that drive each business.
     - Pitfall: applying industrial ratios to financials.
     - Build: a KPI definition sheet per sector you cover.

116. Ratio comparability problems (sector, size, and accounting differences)
     - Covers: limits to cross-company comparison.
     - Details: compare within sector, similar size, and same accounting standard where possible.
     - Pitfall: ranking all stocks on one raw ratio.
     - Build: sector-neutral z-scores of each ratio.

## 4.3 Valuation

117. Discounted cash flow (FCFF vs. FCFE, explicit period, terminal value)
     - Covers: intrinsic value from future cash flows.
     - Details: FCFF discounted at WACC gives enterprise value, FCFE at cost of equity gives equity value. Terminal value usually dominates.
     - Pitfall: terminal value above 70% of the total with aggressive growth.
     - Build: a DCF model with explicit assumptions and a terminal-value share display.

118. Cost of capital (CAPM, WACC, beta estimation, size and country premia)
     - Covers: discount rates.
     - Details: cost of equity = rf + beta x ERP. WACC weights equity and after-tax debt costs by market values.
     - Pitfall: using book values for weights and unstable single-regression betas.
     - Build: beta estimates with confidence intervals and a WACC sensitivity table.

119. Terminal-value sensitivity and why DCF is fragile
     - Covers: input sensitivity.
     - Details: small changes in discount rate or terminal growth swing value by large percentages.
     - Pitfall: presenting a single point value as precise.
     - Build: a WACC x terminal-growth sensitivity grid.

120. Relative valuation multiples (P/E, P/B, P/S, EV/EBITDA, EV/Sales, EV/EBIT, PEG, P/FCF)
     - Covers: pricing versus peers.
     - Details: enterprise multiples need enterprise-value numerators (EV = market cap + net debt + other claims).
     - Pitfall: mixing equity and enterprise numerators and denominators.
     - Build: a multiples table with consistent definitions.

121. Multiple selection by sector and lifecycle stage
     - Covers: choosing the right multiple.
     - Details: P/B for banks, EV/EBITDA for capital-intensive firms, EV/Sales for early growth, P/E for stable earners.
     - Pitfall: using P/E for firms with negative or cyclical-peak earnings.
     - Build: a sector-to-multiple mapping with rationale.

122. Dividend discount models and payout sustainability
     - Covers: valuing dividend payers.
     - Details: Gordon growth: P = D1 / (r - g). Check payout ratio versus free cash flow.
     - Pitfall: g close to r makes value explode.
     - Build: a DDM with a payout-coverage check.

123. Residual income and economic value added (EVA)
     - Covers: value above the capital charge.
     - Details: residual income = net income - cost of equity x book equity. EVA = NOPAT - WACC x capital.
     - Pitfall: unreliable book values and accounting distortions.
     - Build: a residual-income valuation compared with DCF.

124. Sum-of-the-parts and asset-based valuation (NAV, replacement cost, liquidation value)
     - Covers: valuing diversified and asset-heavy firms.
     - Details: value each segment with its own multiple, then subtract holding-company costs and net debt.
     - Pitfall: stacking optimistic multiples on every part.
     - Build: an SOTP template with a conglomerate-discount input.

125. Reverse DCF (what does the market price imply?)
     - Covers: solving for implied expectations.
     - Details: fix the price, solve for growth or margin that justifies it, then judge plausibility.
     - Pitfall: not comparing implied numbers with history and peers.
     - Build: a solver returning implied growth for a given price.

126. Scenario and probability-weighted valuation
     - Covers: explicit uncertainty.
     - Details: bull, base, and bear cases with probabilities. Expected value = sum of probability x value.
     - Pitfall: arbitrary probabilities that match a desired answer.
     - Build: three-scenario model with documented drivers.

127. Real options and valuation of growth optionality
     - Covers: value from flexibility.
     - Details: options to expand, delay, or abandon add value beyond static DCF, valued with option-pricing logic.
     - Pitfall: using real options to justify any price.
     - Build: a simple binomial real-option example.

128. Valuation of financials, cyclicals, commodity producers, and loss-making firms
     - Covers: special cases.
     - Details: banks (P/B vs. ROE), cyclicals (normalized earnings), commodity firms (reserve value at price decks), loss-makers (revenue multiples and path to profit).
     - Pitfall: peak-earnings multiples on cyclicals.
     - Build: a normalized-earnings calculation using a full-cycle average.

129. Earnings normalization and cycle-adjusted multiples (Shiller CAPE)
     - Covers: removing cycle effects.
     - Details: CAPE = price / average of 10 years of inflation-adjusted earnings.
     - Pitfall: using CAPE as a short-term timing tool.
     - Build: CAPE for your market compared with its own history.

130. Margin of safety concept and its quantitative implementation
     - Covers: buffer between price and value.
     - Details: margin of safety = (intrinsic value - price) / intrinsic value. Size the required margin to valuation uncertainty.
     - Pitfall: a margin computed from a single fragile estimate.
     - Build: a rule requiring a larger margin when valuation sensitivity is high.

131. Valuation percentiles vs. own history and vs. peers
     - Covers: relative cheapness.
     - Details: rank current multiples within history and the peer group. Account for structural changes.
     - Pitfall: assuming mean reversion when the business has changed.
     - Build: percentile bands with structural-break flags.

132. Value traps and when cheap stays cheap
     - Covers: low multiples that don't revert.
     - Details: declining margins, obsolete products, high debt, and poor capital allocation keep stocks cheap.
     - Pitfall: screening on valuation alone.
     - Build: combine valuation with quality and momentum filters and compare results.

## 4.4 Earnings quality and forensic analysis

133. Accruals analysis (Sloan accrual anomaly)
     - Covers: non-cash portion of earnings.
     - Details: accruals = net income - operating cash flow (scaled by assets). High accruals tend to precede lower future returns.
     - Pitfall: industry differences in normal accrual levels.
     - Build: sector-adjusted accrual ratios and a backtest of the signal.

134. Cash earnings vs. accounting earnings divergence
     - Covers: gap between profit and cash.
     - Details: persistent net income above operating cash flow suggests aggressive recognition or working-capital build.
     - Pitfall: ignoring timing differences in growth phases.
     - Build: a rolling ratio of operating cash flow to net income.

135. Beneish M-score and manipulation screens
     - Covers: statistical manipulation flag.
     - Details: eight-variable model including receivables index, gross margin index, and accruals. A score above about -1.78 flags possible manipulation.
     - Pitfall: false positives for fast-growing firms.
     - Build: compute the M-score and review flagged names manually.

136. Piotroski F-score
     - Covers: nine-point financial-strength score.
     - Details: tests profitability, leverage and liquidity, and efficiency changes. A score of 8 or 9 is strong, 0 or 1 is weak.
     - Pitfall: it was designed for value stocks, not for all universes.
     - Build: F-score on a low price-to-book universe and its forward returns.

137. Altman Z-score and distress prediction (Ohlson, Merton distance-to-default)
     - Covers: bankruptcy risk.
     - Details: Altman Z combines five ratios. Merton distance-to-default uses equity value and volatility.
     - Pitfall: using the manufacturing formula for non-manufacturers.
     - Build: a distress score table and a check of past defaults.

138. Revenue-recognition red flags and channel stuffing
     - Covers: sales inflation tactics.
     - Details: receivables growing faster than sales, rising days sales outstanding, and large year-end sales.
     - Pitfall: normal growth in receivables from longer credit terms.
     - Build: a DSO-vs-revenue-growth alert.

139. Working-capital manipulation and capitalization of expenses
     - Covers: shifting costs and cash timing.
     - Details: capitalizing costs raises profit now. Stretching payables boosts cash flow temporarily.
     - Pitfall: missing rising capitalized-cost-to-sales ratios.
     - Build: a capitalization-ratio trend with peer comparison.

140. Related-party transactions and governance red flags
     - Covers: dealings with insiders.
     - Details: loans to promoters, transactions with affiliates, and unusual contracts that shift value.
     - Pitfall: ignoring the footnote disclosures.
     - Build: a related-party transaction size relative to revenue.

141. Auditor changes, qualifications, and resignations
     - Covers: audit-quality signals.
     - Details: sudden auditor resignations, qualified opinions, or frequent changes are warning signs.
     - Pitfall: not tracking events as they occur.
     - Build: an event feed of audit-related filings.

142. Insider ownership, pledging, and promoter-holding patterns
     - Covers: insider alignment and stress.
     - Details: high pledging of insider shares signals financing stress and forced-sale risk.
     - Pitfall: reading insider selling without context (taxes, diversification).
     - Build: a pledged-share ratio tracker.

143. One-time item abuse and recurring "non-recurring" charges
     - Covers: adjusted earnings credibility.
     - Details: if "one-time" items recur every year, they are part of the business.
     - Pitfall: accepting management's adjusted earnings without checking history.
     - Build: count years in which each adjustment appears.

144. Goodwill and intangible impairment risk
     - Covers: acquisition-related balance-sheet risk.
     - Details: goodwill/equity ratio and price below book value raise impairment risk.
     - Pitfall: impairment charges are non-cash but signal a failed acquisition.
     - Build: goodwill-to-equity screens.

145. Debt covenant stress and refinancing risk
     - Covers: debt terms and maturity.
     - Details: maturity wall, covenant headroom, floating-rate exposure, and refinancing conditions.
     - Pitfall: looking at total debt without its maturity profile.
     - Build: a debt-maturity ladder and covenant headroom table.

## 4.5 Business and industry analysis

146. Competitive advantage (moats: network effects, switching costs, scale, brand, regulation)
     - Covers: durable profit sources.
     - Details: signs include stable high ROIC, pricing power, and low customer churn.
     - Pitfall: calling any large company a moat business.
     - Build: a moat checklist with evidence fields.

147. Porter's five forces and industry structure
     - Covers: industry profitability drivers.
     - Details: rivalry, entrants, substitutes, buyer power, supplier power.
     - Pitfall: qualitative scoring with no data.
     - Build: a five-forces scorecard supported by industry metrics.

148. Market share dynamics and total addressable market
     - Covers: growth room.
     - Details: share trends show competitiveness. TAM estimates are uncertain and often inflated.
     - Pitfall: top-down TAM that assumes tiny share equals big revenue.
     - Build: a bottom-up TAM estimate from units and price.

149. Unit economics and operating leverage
     - Covers: per-unit profitability and cost structure.
     - Details: contribution margin = price - variable cost. Operating leverage = contribution margin / operating profit.
     - Pitfall: ignoring that high operating leverage also magnifies downturns.
     - Build: a unit-economics model with breakeven volume.

150. Pricing power and cost pass-through
     - Covers: ability to raise prices.
     - Details: evidence from gross margin stability during input-cost inflation.
     - Pitfall: confusing demand surges with pricing power.
     - Build: gross-margin response to input-cost changes.

151. Capital intensity and return on incremental capital
     - Covers: capital needs of growth.
     - Details: incremental ROIC = change in NOPAT / change in invested capital.
     - Pitfall: ignoring maintenance capex.
     - Build: capex-to-depreciation and incremental ROIC trends.

152. Management quality, capital allocation record, and incentive alignment
     - Covers: people and decisions.
     - Details: track acquisitions, buyback timing, dividend policy, and pay metrics.
     - Pitfall: judging from presentations instead of results.
     - Build: a capital-allocation scorecard over ten years.

153. Corporate governance scoring
     - Covers: structure and shareholder protection.
     - Details: board independence, dual-class shares, audit committee quality, and takeover defenses.
     - Pitfall: box-ticking scores that lack predictive power.
     - Build: a score tested against future returns or restatements.

154. Business-cycle sensitivity and cyclicality classification
     - Covers: exposure to the economy.
     - Details: measure earnings beta to GDP or industry indicators.
     - Pitfall: valuing cyclicals at peak earnings.
     - Build: cyclicality scores from earnings drawdowns in past recessions.

155. Supply chain, customer, and supplier concentration risk
     - Covers: dependency risk.
     - Details: large customers, single-source suppliers, and geographic concentration.
     - Pitfall: not reading disclosed customer concentration.
     - Build: a concentration table from filings.

156. Regulatory and policy exposure
     - Covers: sensitivity to rules and policy.
     - Details: price controls, licensing, tariffs, and subsidy dependence.
     - Pitfall: pricing in no change when reform is likely.
     - Build: a policy-exposure map with scenario impacts.

157. Disruption risk and technology shifts
     - Covers: threats to the business model.
     - Details: incumbent models threatened by new technology, substitutes, or new distribution.
     - Pitfall: assuming the past business model persists.
     - Build: a disruption watchlist per sector.

158. ESG and sustainability factors as fundamental risk
     - Covers: non-financial risk factors.
     - Details: environmental liabilities, labor issues, and governance failures can hit cash flows.
     - Pitfall: inconsistent ratings across providers.
     - Build: map ESG items to financial line-items affected.

## 4.6 Fundamental factor signals (systematic)

159. Value factor (book-to-market, earnings yield, FCF yield, EV/EBITDA) and its variants
     - Covers: cheapness signals.
     - Details: composite value uses several ratios to reduce noise. Industry-neutralize to avoid sector bets.
     - Pitfall: value defined only by book-to-market is weak for intangible-heavy firms.
     - Build: a composite value score with sector neutralization.

160. Quality factor (profitability, stability, low leverage, earnings quality)
     - Covers: high-quality company signals.
     - Details: combine ROE, gross profitability, earnings stability, low leverage, and low accruals.
     - Pitfall: overlapping definitions that double count.
     - Build: a quality composite with documented components.

161. Growth and growth-at-reasonable-price factors
     - Covers: growth signals.
     - Details: growth measured by revenue and EPS growth, GARP adds a price constraint such as PEG.
     - Pitfall: extrapolating high growth indefinitely.
     - Build: a GARP score that penalizes extreme valuations.

162. Low-volatility, low-beta, and defensive factors
     - Covers: lower-risk stock premium.
     - Details: low-beta stocks historically earn higher risk-adjusted returns. Often needs leverage to match market risk.
     - Pitfall: hidden sector and interest-rate exposures.
     - Build: a low-vol portfolio with sector caps.

163. Dividend yield, shareholder yield, and buyback factors
     - Covers: cash return signals.
     - Details: shareholder yield = dividend yield + net buyback yield.
     - Pitfall: high yield from a falling price signals distress.
     - Build: yield signals combined with payout-sustainability checks.

164. Investment factor (asset growth) and profitability factor (Fama-French five-factor)
     - Covers: conservative investment and robust profitability premiums.
     - Details: firms with low asset growth tend to outperform those with high asset growth.
     - Pitfall: mis-measuring profitability across industries.
     - Build: construct the factors and regress returns on them.

165. Earnings momentum, estimate revisions, analyst surprise, and standardized unexpected earnings (SUE)
     - Covers: changes in earnings expectations.
     - Details: SUE = (actual EPS - expected EPS) / standard deviation of past surprises. Revision momentum is a strong short-horizon signal.
     - Pitfall: estimate data that is not point-in-time.
     - Build: a revision-breadth signal using point-in-time estimates.

166. Post-earnings-announcement drift (PEAD)
     - Covers: continued drift after earnings surprises.
     - Details: prices underreact to surprises, with drift for weeks to months, stronger in small illiquid stocks.
     - Pitfall: capacity limits and transaction costs in small caps.
     - Build: an event study of returns after SUE decile announcements.

167. Analyst coverage, dispersion, and recommendation-change signals
     - Covers: sell-side information.
     - Details: high dispersion tends to precede lower returns. Recommendation upgrades carry short-term signal.
     - Pitfall: herding and stale revisions.
     - Build: dispersion and revision signals with decay curves.

168. Insider-buying and institutional-holding-change signals
     - Covers: informed-participant behavior.
     - Details: cluster insider purchases are more informative than sales. Holdings data arrive with lag.
     - Pitfall: using holdings that were not yet public.
     - Build: an event study around insider-filing dates.

169. Short-interest and borrow-cost signals
     - Covers: bearish positioning.
     - Details: high short interest and high borrow cost predict lower returns on average but raise squeeze risk.
     - Pitfall: stale short-interest reports.
     - Build: short-interest ratio signal with a squeeze-risk cap.

170. Combining fundamental factors (z-scoring, sector-neutralization, winsorization, ranking)
     - Covers: composite construction.
     - Details: winsorize outliers, z-score within sector, and weight by stability or risk contribution.
     - Pitfall: hidden correlation among factors.
     - Build: a pipeline producing a composite score with a stability test.

171. Factor timing vs. static exposure and factor-cyclicality
     - Covers: whether to time factors.
     - Details: evidence for timing is weak and fragile. Diversifying across factors is more reliable.
     - Pitfall: timing rules fitted to past regimes.
     - Build: compare static equal-weight with a timing rule out of sample.

172. Factor decay, crowding, and the post-publication performance decline
     - Covers: fading premiums.
     - Details: returns often fall after publication due to arbitrage, data mining, and crowding.
     - Pitfall: expecting backtested premiums in full.
     - Build: compare pre- and post-publication performance of known factors.

## 4.7 Macro fundamentals

173. GDP, PMI, industrial production, retail sales, employment, and inflation data
     - Covers: core macro indicators.
     - Details: releases are revised and lagged. Know the release schedule, revision size, and market reaction.
     - Pitfall: using revised data in backtests.
     - Build: a release-calendar database with first-release values.

174. Leading, coincident, and lagging indicators
     - Covers: timing of the cycle.
     - Details: leading indicators include PMI new orders, yield curve, and credit spreads.
     - Pitfall: indicators that lose reliability after structural change.
     - Build: a cycle dashboard classifying each indicator.

175. Monetary policy, policy-rate expectations, balance-sheet effects, and central bank communication
     - Covers: central bank drivers.
     - Details: rate-futures imply market-expected path. Quantitative tightening drains liquidity.
     - Pitfall: trading the decision and not the surprise relative to expectations.
     - Build: expected versus actual rate-decision surprise series.

176. Yield curve shape, inversion, and credit spreads as regime signals
     - Covers: bond-market information.
     - Details: 10y-2y spread inversion has preceded recessions with variable lead times.
     - Pitfall: treating inversion as a precise timing signal.
     - Build: a regime indicator from curve slope and spreads.

177. Currency, commodity, and terms-of-trade effects
     - Covers: external drivers.
     - Details: commodity exporters benefit from price increases, importers suffer. Currency moves change foreign-earnings translation.
     - Pitfall: ignoring hedging.
     - Build: sensitivities of sectors to FX and commodity moves.

178. Fiscal policy, government debt, and election cycles
     - Covers: government actions.
     - Details: spending, taxes, deficits, and policy uncertainty around elections.
     - Pitfall: over-reading single events.
     - Build: event-study around budget and election dates.

179. Global liquidity, dollar cycle, and capital flows
     - Covers: cross-border funding conditions.
     - Details: a strong dollar tightens conditions for emerging markets.
     - Pitfall: using one liquidity measure.
     - Build: a composite liquidity indicator.

180. Nowcasting and surprise indices
     - Covers: real-time estimates and surprises.
     - Details: nowcasts combine many indicators for current-quarter growth. Surprise indices measure data versus consensus.
     - Pitfall: noisy and revised inputs.
     - Build: a surprise index and its relation to subsequent asset returns.

181. Macro-to-micro transmission (which sectors react to which indicators)
     - Covers: mapping macro to sectors.
     - Details: banks and rates, homebuilders and mortgage rates, exporters and currency.
     - Pitfall: using static sensitivities that change by regime.
     - Build: rolling sector betas to rate and commodity changes.

182. Geopolitical and commodity shock mapping
     - Covers: shock propagation.
     - Details: identify exposed supply chains, regions, and commodities and scenario outcomes.
     - Pitfall: guessing outcomes with no scenario framework.
     - Build: a shock-impact table per sector.

## 4.8 Event and corporate action fundamentals

183. Earnings calendar, guidance, and surprise-reaction modeling
     - Covers: scheduled earnings events.
     - Details: model expected move from options-implied move and past reactions. Guidance often moves price more than the quarter itself.
     - Pitfall: unreliable earnings dates.
     - Build: an event calendar with confirmed dates and an implied-move estimate.

184. M&A, spin-offs, restructurings, and merger-arbitrage spreads
     - Covers: corporate transactions.
     - Details: merger-arb spread = deal price - current price, compensating for completion and time risk.
     - Pitfall: deal-break losses are much larger than the typical gains.
     - Build: spread-implied deal probability.

185. Dividend declarations, ex-dates, special dividends, and stock-split effects
     - Covers: payout events.
     - Details: price drops by about the dividend on the ex-date. Splits change prices but not value.
     - Pitfall: treating the ex-date drop as a loss.
     - Build: a corporate-action event table feeding position and P&L.

186. Rights issues, QIPs, secondary offerings, and dilution events
     - Covers: equity raises.
     - Details: dilution, discount to market, and signal about management's view.
     - Pitfall: ignoring the adjustment factors for rights issues.
     - Build: event handling for adjusting price history and positions.

187. Credit rating changes and outlook revisions
     - Covers: debt-quality changes.
     - Details: downgrades below investment grade force selling by some funds.
     - Pitfall: ratings lag market-implied credit risk.
     - Build: rating-change event study.

188. Regulatory approvals, litigation outcomes, and sector-specific catalysts (e.g., drug trials)
     - Covers: binary events.
     - Details: payoffs are jump-like. Options-implied moves price the event.
     - Pitfall: sizing as if outcomes were continuous.
     - Build: binary-event position-sizing rule with a loss cap.

189. Management changes and activist involvement
     - Covers: governance events.
     - Details: CEO changes and activist stakes can change strategy and capital allocation.
     - Pitfall: assuming activists always create value.
     - Build: event-study of returns after activist disclosures.

## 4.9 Positioning, flows, and special situations

190. Commitment of Traders (COT) and 13F positioning data
     - Covers: positioning disclosures.
     - Details: COT is weekly for futures, 13F quarterly with 45-day lag.
     - Pitfall: using stale holdings as current positions.
     - Build: a positioning index with publication-date alignment.

191. Options flow, dark-pool prints, and ETF flow data
     - Covers: flow-based signals.
     - Details: unusual options volume and dark-print size are noisy, and require classification of trade direction.
     - Pitfall: misreading hedges as directional bets.
     - Build: a flow-signal test with trade-direction classification.

192. Index rebalancing, inclusion/exclusion, and ETF creation/redemption effects
     - Covers: mechanical flows.
     - Details: index funds must buy additions and sell deletions around effective dates, creating predictable demand.
     - Pitfall: crowded anticipation reduces the edge.
     - Build: an event study around index-announcement and effective dates.

193. IPOs, buybacks, secondary offerings, and lock-up expiries
     - Covers: supply and demand events.
     - Details: lock-up expiry increases potential supply. Buybacks add demand.
     - Pitfall: IPO data survivorship and allocation constraints.
     - Build: lock-up expiry calendar with return analysis.

194. Cross-listings, ADRs, and dual-listed arbitrage
     - Covers: same-company prices across venues.
     - Details: arbitrage needs FX, conversion ratios, and trading-hour alignment.
     - Pitfall: ignoring transfer costs and settlement differences.
     - Build: spread monitor adjusted for FX and ratio.

## 4.10 Devil's advocate on fundamental analysis

195. Why most fundamental signals are slow and often priced in
     - Covers: edge decay.
     - Details: public ratios are widely used, so the edge is small and horizon is long.
     - Pitfall: expecting quick alpha from public data.
     - Build: test the signal after a transaction-cost and capacity haircut.

196. Value-factor long drawdowns and the "value is dead" debate
     - Covers: drawdown tolerance.
     - Details: value underperformed for roughly a decade before recovering at points.
     - Pitfall: abandoning a factor at its low or leveraging into it.
     - Build: drawdown-duration analysis of the factor.

197. Accounting-based signal degradation from intangibles-heavy economies
     - Covers: measurement problem.
     - Details: R&D and brand spending are expensed, so book equity understates assets.
     - Pitfall: classic ratios mislabel intangible-heavy firms as expensive.
     - Build: intangible-adjusted book value.

198. Reported-data timing risk (stale information, late filers)
     - Covers: availability delay.
     - Details: some firms file late or restate, and data vendors lag.
     - Pitfall: trading on information everyone already has.
     - Build: filing-delay statistics per universe.

199. Model sensitivity: small input changes produce huge valuation changes
     - Covers: fragility.
     - Details: sensitivity to discount rate and growth is large.
     - Pitfall: false precision.
     - Build: report value ranges, not points.

200. Narrative bias vs. numbers and anchoring on analyst consensus
     - Covers: behavioral traps.
     - Details: compelling stories lead to ignoring base rates, and consensus anchors your estimates.
     - Pitfall: confirming your thesis with selective evidence.
     - Build: a pre-mortem and disconfirming-evidence checklist.
