# Part 9. Derivatives and Other Products: Micro Details (topics 399 to 434)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 9.1 Options

399. Black-Scholes-Merton and its assumptions
     - Covers: the baseline option pricing model.
     - Details: call = S N(d1) - K e^{-rT} N(d2), with d1 = [ln(S/K) + (r + sigma^2/2)T] / (sigma sqrt(T)), d2 = d1 - sigma sqrt(T). Assumes constant volatility, continuous trading, and lognormal prices.
     - Pitfall: using it for American options or with a single flat volatility.
     - Build: an implementation checked against put-call parity.

400. Greeks (delta, gamma, vega, theta, rho, vanna, volga, charm)
     - Covers: sensitivities.
     - Details: delta to price, gamma to delta change, vega to volatility, theta to time, rho to rates. Higher-order Greeks (vanna, volga, charm) matter for large or long-dated books.
     - Pitfall: mixing Greek units (per 1% vol, per day).
     - Build: analytic Greeks checked against finite-difference bumps.

401. Implied volatility surfaces, smile, skew
     - Covers: market-implied volatility structure.
     - Details: implied volatility varies by strike and expiry. Equity indexes show downward skew. The surface must be arbitrage-free.
     - Pitfall: interpolating across strikes and expiries in ways that create arbitrage.
     - Build: a surface builder with calendar and butterfly arbitrage checks.

402. Volatility models (local vol, SABR, Heston, SVI)
     - Covers: models fitted to the surface.
     - Details: local volatility matches today's surface, stochastic models (Heston, SABR) capture dynamics, and SVI parameterizes the smile slice.
     - Pitfall: parameters unstable across days.
     - Build: calibrate one model daily and track parameter stability.

403. Binomial/trinomial trees, PDE and Monte Carlo pricing
     - Covers: numerical pricing.
     - Details: trees handle early exercise, PDEs give accurate Greeks, Monte Carlo suits path-dependent payoffs.
     - Pitfall: coarse grids or few paths without error checks.
     - Build: convergence study for each method.

404. American options and early exercise
     - Covers: exercise before expiry.
     - Details: early exercise matters for puts, and for calls around dividends. Use trees or least-squares Monte Carlo.
     - Pitfall: pricing American options as European.
     - Build: American put pricer compared with the European price.

405. Delta and gamma hedging, dynamic hedging costs
     - Covers: hedging a book.
     - Details: delta hedging removes first-order price risk. Gamma creates hedging P&L that depends on realized versus implied volatility. Hedging frequency trades slippage against residual risk.
     - Pitfall: ignoring transaction costs and discrete hedging error.
     - Build: simulate delta hedging at different frequencies and costs.

406. Volatility trading (straddles, strangles, variance swaps, dispersion)
     - Covers: trading volatility with options.
     - Details: long straddle profits from large moves, variance swaps pay realized minus strike variance, dispersion trades index versus single-stock volatility.
     - Pitfall: ignoring gamma-theta bleed and correlation risk.
     - Build: P&L attribution of a straddle into gamma, theta, and vega.

407. Spread strategies (verticals, calendars, butterflies, condors, ratios)
     - Covers: multi-leg structures.
     - Details: define max profit, max loss, breakeven, and Greeks for each structure.
     - Pitfall: illiquid legs with high combined costs.
     - Build: a payoff and Greek calculator for common spreads.

408. Income strategies (covered calls, cash-secured puts, wheel)
     - Covers: premium selling.
     - Details: collect premium and accept capped upside or assignment risk.
     - Pitfall: confusing premium income with risk-free yield, since losses occur in sharp declines.
     - Build: backtest with assignment handling and realistic fills.

409. Volatility risk premium and term structure
     - Covers: implied versus realized volatility.
     - Details: implied volatility has tended to exceed realized on average for indexes, with negative skew in returns to selling it. Term structure is usually in contango, inverting under stress.
     - Pitfall: ignoring crash risk in short-volatility positions.
     - Build: implied-minus-realized series and conditional returns.

410. Skew, term-structure, and calendar arbitrage
     - Covers: relative-value in volatility.
     - Details: trade rich or cheap points on the surface with hedged structures.
     - Pitfall: apparent mispricing that reflects bid-ask spreads and liquidity.
     - Build: a scanner that uses mid prices and tradeable-price versions.

411. Put-call parity and arbitrage checks
     - Covers: consistency relations.
     - Details: C - P = S - K e^{-rT} for European options without dividends. Violations indicate data errors or arbitrage.
     - Pitfall: ignoring dividends, borrow costs, and early exercise.
     - Build: a parity monitor that flags violations beyond costs.

412. Options on futures and index options (settlement, European vs. American)
     - Covers: contract differences.
     - Details: futures options use the futures price (Black-76). Index options are cash-settled and often European.
     - Pitfall: using spot pricing for futures options.
     - Build: Black-76 pricer and settlement-rule table.

413. Expiry mechanics, pin risk, assignment risk
     - Covers: expiration-time risk.
     - Details: near the strike at expiry, assignment is uncertain and positions can change overnight.
     - Pitfall: holding short options through expiry without a plan.
     - Build: an expiry checklist and automatic pre-expiry position reduction rule.

414. Margin and portfolio margin for options
     - Covers: capital requirements.
     - Details: strategy-based margin differs from risk-based portfolio margin, and requirements can change quickly.
     - Pitfall: leverage that a margin-rule change can break.
     - Build: margin calculator and a stress test of margin increases.

415. Exotics and structured products (barriers, Asians, digitals)
     - Covers: non-standard payoffs.
     - Details: barrier options have discontinuous Greeks near the barrier, digitals have gap risk.
     - Pitfall: hedging by naive delta near barriers.
     - Build: Monte Carlo pricing and a Greek profile near barriers.

## 9.2 Futures, fixed income, and FX

416. Futures, forwards, swaps (basis, carry, contango, backwardation)
     - Covers: linear derivatives.
     - Details: futures price ~ spot x e^{(r + storage - convenience yield)T}. Basis converges to zero at expiry. Marking to market creates daily cash flows.
     - Pitfall: ignoring margin calls and funding needs.
     - Build: a basis and roll-yield calculator.

417. Fixed income and rates (duration, convexity, yield curves)
     - Covers: bond and rate fundamentals.
     - Details: price change approx = -D x dy + 0.5 x C x dy^2. Curve construction uses bootstrapping and interpolation.
     - Pitfall: ignoring convexity and curve shape changes.
     - Build: bond price/yield engine and DV01 calculator.

418. FX specifics (carry, triangular arbitrage, forwards, rollover)
     - Covers: currency trading mechanics.
     - Details: forward points reflect interest differentials, positions roll with swap costs, and spot value dates are typically T+2.
     - Pitfall: ignoring rollover costs and weekend gaps.
     - Build: a carry and swap-cost model per pair.

## 9.3 Additional asset classes and products

419. Commodities (storage, seasonality, delivery, and physical-settlement risk)
     - Covers: commodity markets.
     - Details: term structure reflects storage and convenience yield. Seasonality affects agricultural and energy prices. Avoid physical delivery by rolling before notice dates.
     - Pitfall: accidental delivery obligations.
     - Build: a notice-date calendar and roll rules per contract.

420. ETFs and ETNs (tracking error, premium/discount, leveraged ETF decay)
     - Covers: exchange-traded products.
     - Details: ETFs trade near NAV through creation and redemption. Leveraged ETFs reset daily and decay in volatile, trendless markets. ETNs carry issuer credit risk.
     - Pitfall: holding leveraged products for long horizons.
     - Build: simulate leveraged ETF returns versus a multiple of the index.

421. Volatility products (VIX futures, VIX ETPs, roll-yield decay)
     - Covers: instruments tracking volatility.
     - Details: VIX itself is not directly tradable. Futures-based products suffer roll costs in contango.
     - Pitfall: treating VIX products as hedges without considering decay.
     - Build: roll-yield decomposition of a VIX-futures product.

422. Credit (bonds, CDS, spreads, and default modeling)
     - Covers: credit instruments.
     - Details: spread compensates for default probability and recovery plus risk premia. CDS spreads approximate default hazard times loss given default.
     - Pitfall: liquidity and funding differences between bonds and CDS.
     - Build: a simple hazard-rate calculation from spread.

423. Convertibles and warrants
     - Covers: hybrid instruments.
     - Details: convertible value = bond floor + embedded call. Delta, gamma, credit, and borrow all matter.
     - Pitfall: ignoring call provisions and credit risk.
     - Build: a component decomposition of a convertible bond.

424. Prediction markets
     - Covers: event-outcome contracts.
     - Details: prices approximate probabilities but include fees and liquidity effects. Resolution rules matter.
     - Pitfall: ambiguous resolution criteria.
     - Build: compare market-implied probabilities with calibrated forecasts.

425. Weekly and zero-days-to-expiry options (0DTE) behavior
     - Covers: very short-dated options.
     - Details: gamma is very high near expiry, and moves in the underlying quickly change delta. Costs and liquidity dominate.
     - Pitfall: underestimating gamma risk and intraday path dependence.
     - Build: intraday P&L simulation under different volatility paths.

## 9.4 Crypto and DeFi

426. Crypto derivatives (perpetuals, funding rates, liquidations)
     - Covers: perpetual swaps and futures.
     - Details: funding payments anchor perpetual prices to spot. Liquidation engines can cascade in fast markets. Leverage and margin modes differ by exchange.
     - Pitfall: liquidation and auto-deleveraging risk.
     - Build: a funding-rate and liquidation-distance tracker.

427. Crypto specifics (DEX/CEX integration, custody, on-chain data)
     - Covers: practical crypto infrastructure.
     - Details: centralized exchanges offer order books, decentralized ones use pools or on-chain books. Custody needs key management and withdrawal limits. On-chain data gives flows and positions.
     - Pitfall: leaving large balances on exchanges.
     - Build: a custody policy and a balance-reconciliation job.

428. AMM mechanics, impermanent loss, and LP strategies
     - Covers: automated market makers.
     - Details: constant product x y = k. Liquidity providers face impermanent loss relative to holding, offset by fees.
     - Pitfall: ignoring loss when prices diverge.
     - Build: simulate LP returns including fees and impermanent loss.

429. MEV, front-running, and sandwich attacks
     - Covers: transaction-ordering extraction.
     - Details: searchers reorder transactions to profit from pending trades. Private relays and slippage limits reduce exposure.
     - Pitfall: large swaps with loose slippage settings.
     - Build: a pre-trade check estimating sandwich exposure.

430. Stablecoin depeg risk
     - Covers: peg failure.
     - Details: reserves, redemption mechanics, and market confidence determine peg stability.
     - Pitfall: treating all stablecoins as cash equivalents.
     - Build: monitoring of peg deviation and exposure limits per issuer.

431. Bridge and smart-contract risk
     - Covers: protocol-level risk.
     - Details: contract bugs, bridge exploits, and governance attacks have caused large losses.
     - Pitfall: ignoring audits and concentration in a single protocol.
     - Build: exposure caps per protocol and a review checklist.

432. Exchange proof-of-reserves and counterparty risk
     - Covers: exchange solvency.
     - Details: reserves attestations should cover liabilities, ideally with independent audit.
     - Pitfall: relying on reserves snapshots without liabilities.
     - Build: counterparty limits and withdrawal-test routines.

433. Tokenized assets and 24/7 market dynamics
     - Covers: continuous trading and tokenization.
     - Details: weekend liquidity is thinner, and gaps occur when traditional markets reopen.
     - Pitfall: running weekday logic on weekends.
     - Build: time-of-week liquidity and volatility profile.

434. On-chain order books and settlement finality
     - Covers: decentralized order matching.
     - Details: transactions are final after confirmation depth, and reorganizations can reverse recent blocks on some chains.
     - Pitfall: treating unconfirmed fills as final.
     - Build: confirmation-depth rules per chain.
