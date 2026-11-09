# Part 1. Market Foundations: Micro Details (topics 1 to 35)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 1.1 Market structure and asset classes

1. Market structure (exchanges, brokers, ECNs, dark pools, market makers)
   - Covers: exchanges, broker-dealers, ECNs/ATS, dark pools, market makers, clearing houses, depositories.
   - Details: order path is client, broker, venue, central counterparty (CCP). The CCP takes over both sides through novation. Fee models include maker-taker and taker-maker.
   - Pitfall: treating one venue as "the market" when liquidity is fragmented across venues.
   - Build: a one-page map of venues and intermediaries for your target market.

2. Asset classes (equities, futures, options, FX, fixed income, crypto)
   - Covers: instrument types and how each trades.
   - Details: they differ in hours, settlement, leverage, tick size, cost structure, and data availability. FX and bonds are largely OTC with no single tape.
   - Pitfall: reusing equity assumptions (continuous price series, central tape) on futures, FX, or bonds.
   - Build: a comparison table of every instrument you plan to trade.

3. Order book mechanics, bid/ask spread, liquidity
   - Covers: bids, asks, depth, price-time priority, L1/L2/L3 data.
   - Details: spread = best ask - best bid. Mid = (bid + ask) / 2. Relative spread in bps = spread / mid x 10,000. Some futures use pro-rata matching, not price-time.
   - Pitfall: treating displayed depth as real liquidity (spoofing, icebergs, quote flicker).
   - Build: an order-book class with add, cancel, match, and spread/depth metrics.

4. Auction mechanisms (opening, closing, volatility halts)
   - Covers: call auctions, opening and closing auctions, intraday volatility auctions.
   - Details: the uncross price maximizes executed volume. Exchanges publish indicative prices and imbalances. Closing auctions often carry a large share of daily volume and set official prices.
   - Pitfall: ignoring auction phases when computing returns, fills, or volume profiles.
   - Build: an auction uncross simulator using a sample order list.

## 1.2 Order types and order handling

5. Order types and order lifecycle (market, limit, stop, IOC/FOK, fills)
   - Covers: market, limit, stop, stop-limit, IOC, FOK, day, and GTC orders.
   - Details: lifecycle is new, acknowledged, partially filled, filled / cancelled / rejected / expired. Market orders take liquidity and limit orders may provide it.
   - Pitfall: stop orders turn into market orders and can fill far past the stop price in a gap.
   - Build: a state diagram plus unit tests for each order type.

6. Bracket, OCO, OTO, and trailing-stop orders
   - Covers: linked and conditional order groups.
   - Details: bracket = entry plus stop plus target. OCO cancels the other leg on a fill. Check whether the logic runs at the exchange or inside the broker's system.
   - Pitfall: broker-simulated brackets can fail silently on disconnect or restart.
   - Build: a test showing what happens to each leg when the session drops.

7. Time-in-force variants (GTC, GTD, day, auction-only)
   - Covers: how long an order lives and in which session.
   - Details: day orders expire at session end, GTC orders can persist across corporate actions and may be repriced or cancelled by the exchange.
   - Pitfall: stale GTC orders left working after a strategy is switched off.
   - Build: a start-of-day report of all open orders with their TIF.

8. Partial fills, rejections, amendments, and cancel/replace races
   - Covers: non-ideal order outcomes.
   - Details: a cancel can arrive after the fill. Amending price usually loses queue priority. Rejects carry codes that distinguish retryable from fatal.
   - Pitfall: assuming "cancel sent" means "cancelled".
   - Build: handlers for late fills after cancel, with tests.

9. Pegged, hidden, and reserve orders
   - Covers: orders tied to a reference or showing only part of size.
   - Details: pegs follow the best bid/offer or midpoint. Hidden orders lose time priority at many venues. Reserve (iceberg) shows a small display quantity.
   - Pitfall: iceberg refresh patterns are detectable and exploited.
   - Build: randomize the display size and refresh timing in a simulator.

10. Self-trade prevention and wash-trade guards
    - Covers: stopping your own orders from matching each other.
    - Details: exchanges offer STP modes (cancel newest, cancel oldest, cancel both). Multiple strategies on one account can cross unintentionally.
    - Pitfall: self-crossing can breach market-abuse rules and distorts volume.
    - Build: a pre-trade check comparing a new order against your own resting orders.

11. Order-to-trade ratio limits and exchange throttling rules
    - Covers: message-rate and OTR constraints.
    - Details: exchanges and regulators cap messages per second and penalize high cancel-to-fill ratios.
    - Pitfall: quote-updating algos exceed limits and get disconnected or fined.
    - Build: a token-bucket throttle in front of the gateway.

12. FIX session management (sequence numbers, resend, heartbeats, drop copy)
    - Covers: FIX session layer.
    - Details: both sides track sequence numbers. Gaps trigger ResendRequest. Heartbeats detect dead links. Drop copy is an independent fill feed.
    - Pitfall: resetting sequence numbers carelessly and replaying or losing messages.
    - Build: a FIX session test harness covering gap fill and reconnect.

13. Cancel-on-disconnect and broker-side kill features
    - Covers: automatic protection when the link dies.
    - Details: the exchange cancels your open orders when the session drops. Know which products and brokers support it.
    - Pitfall: assuming it is on by default.
    - Build: a checklist per broker with a tested yes/no for each protective feature.

14. RFQ and OTC execution
    - Covers: request-for-quote trading in bonds, FX, and block options.
    - Details: you ask dealers for quotes, then hit one. Last-look can let the dealer reject.
    - Pitfall: information leakage when quoting too many dealers.
    - Build: an RFQ workflow with a quote-timeout timer.

15. Auction participation strategies (opening, closing, and imbalance trading)
    - Covers: trading in the auction phases.
    - Details: use published imbalances and indicative prices. Market-on-close orders guarantee the closing price but not the quantity-risk.
    - Pitfall: large MOC orders pay for liquidity during imbalances.
    - Build: a study of closing-price versus last-price-before-close moves.

16. Odd lots, fractional shares, and lot-size changes
    - Covers: size granularity.
    - Details: odd lots may not appear in the quoted best price. Fractional shares depend on the broker. Exchanges change lot sizes over time.
    - Pitfall: hard-coded lot sizes break after a change.
    - Build: a reference-data table of lot sizes with effective dates.

## 1.3 Calendars, contracts, and exchange rules

17. Trading calendars, sessions, holidays, time zones
    - Covers: when each market is open.
    - Details: half days, special sessions, daylight-saving shifts, and local holidays differ per venue.
    - Pitfall: using one calendar for all assets or ignoring time-zone offsets.
    - Build: a calendar service keyed by venue and product.

18. Contract specifications (tick size, lot size, multipliers)
    - Covers: static contract data.
    - Details: PnL = price change x multiplier x quantity. Tick value = tick size x multiplier. Expiry rules and settlement type matter.
    - Pitfall: wrong multiplier gives wrong PnL and wrong risk.
    - Build: a contract master table checked against exchange files.

19. Exchange-specific rules (circuit limits, price bands)
    - Covers: per-exchange guardrails.
    - Details: orders outside the price band are rejected. Limit-up/limit-down stop trading or restrict price moves.
    - Pitfall: algos keep resubmitting rejected orders.
    - Build: store band limits and block orders outside them before sending.

20. Short selling, borrow availability, locate costs
    - Covers: selling what you don't own.
    - Details: need a borrow, pay a borrow fee, and may face recalls. Some markets restrict shorting or ban it in stress.
    - Pitfall: backtests that short hard-to-borrow names at zero cost.
    - Build: a borrow-availability and fee table feeding the backtester.

21. Contract rollover handling and expiry-day logic
    - Covers: moving from one futures contract to the next.
    - Details: roll by date, volume crossover, or open interest. Back-adjustment methods (difference vs. ratio) change historical levels.
    - Pitfall: treating the roll gap as a return.
    - Build: a roll calendar and a unit test comparing adjusted and unadjusted series.

22. Position limits and regulatory restrictions (short-sale rules, pattern day-trader rules)
    - Covers: legal limits on size and activity.
    - Details: exchanges and regulators cap position size in some contracts. Retail accounts may face day-trade rules.
    - Pitfall: discovering a limit only after a rejected order or a violation.
    - Build: a limits table checked in pre-trade controls.

## 1.4 Regional and market-specific topics

23. Local market structure and rules (for example NSE/BSE, SEBI, and retail algo regulations)
    - Covers: the rules of your target market.
    - Details: segments, trading hours, lot sizes, margin rules, and the regulator's stance on retail and algorithmic trading.
    - Pitfall: copying a US/EU design into a market with different rules.
    - Build: a compliance checklist specific to your market.

24. Broker API landscape (Interactive Brokers, Zerodha, Angel One, Alpaca, Binance)
    - Covers: practical broker connectivity options.
    - Details: compare API type, rate limits, order types supported, data included, fees, and reliability.
    - Pitfall: building deeply on one broker's quirks with no abstraction layer.
    - Build: a broker comparison matrix and a common gateway interface.

25. Regional circuit breakers, trading hours, and holiday calendars
    - Covers: market-wide halts and hours.
    - Details: index-level breakers halt trading after large moves, with thresholds and durations set per market.
    - Pitfall: not handling a market-wide halt in the execution logic.
    - Build: a halt-handling test that pauses algos and resumes safely.

26. Cross-border trading, capital controls, and foreign-investor limits
    - Covers: trading across jurisdictions.
    - Details: foreign ownership caps, repatriation rules, withholding taxes, and currency restrictions.
    - Pitfall: ignoring FX and tax friction in cross-border backtests.
    - Build: a per-market friction table.

27. Local tax and reporting obligations by jurisdiction
    - Covers: taxes and filings.
    - Details: transaction taxes, capital gains treatment (short vs. long term), reporting forms, and record-keeping periods.
    - Pitfall: strategies that are profitable pre-tax and unprofitable post-tax.
    - Build: tax-aware PnL columns in reports.

## 1.5 Abnormal market conditions

28. Trading halts, limit-up/limit-down, and stale quotes
    - Covers: states where normal pricing fails.
    - Details: halted instruments have no valid price. Stale quotes persist after a feed stops.
    - Pitfall: marking positions to a stale price.
    - Build: a staleness timer that flags and handles old quotes.

29. Flash-crash handling and liquidity vacuums
    - Covers: sudden extreme moves with thin books.
    - Details: spreads blow out, depth vanishes, and stops trigger in cascades.
    - Pitfall: market orders during a vacuum fill at extreme prices.
    - Build: replay a past crash through your algos and check outcomes.

30. Exchange, broker, or data-feed outages (degraded-mode behavior)
    - Covers: failures in external dependencies.
    - Details: decide in advance whether to flatten, hold, or stop trading when each dependency fails.
    - Pitfall: undefined behavior when only one of several feeds fails.
    - Build: a degraded-mode matrix with a tested response for each failure.

31. Fat-finger prints and erroneous trades (busted-trade policy)
    - Covers: bad prints and trade cancellations.
    - Details: exchanges may cancel trades outside clearly erroneous ranges, which changes positions afterward.
    - Pitfall: signals triggered by a bad print.
    - Build: a print filter and a handler for trade-bust messages.

32. Index and futures-expiry dislocations
    - Covers: pressure around expiries and index events.
    - Details: expiry-day volume spikes, settlement-price jumps, and basis convergence.
    - Pitfall: running normal strategy logic through expiry unchanged.
    - Build: an expiry-day behavior study per contract.

33. Short squeezes and meme-stock dynamics
    - Covers: crowded shorts and retail-driven spikes.
    - Details: high short interest plus borrow recalls plus social attention can produce multi-day rallies.
    - Pitfall: unbounded loss on short positions.
    - Build: a short-interest risk cap and a squeeze scenario test.

34. Negative-price events (such as oil in 2020)
    - Covers: prices below zero.
    - Details: log returns and percentage calculations fail. Some systems reject negative prices.
    - Pitfall: crashes or corrupted analytics from negative or zero prices.
    - Build: tests that feed negative prices through every calculation.

35. Circuit-breaker and market-wide halt behavior
    - Covers: system response to market-wide pauses.
    - Details: reopening usually uses an auction. Orders may be cancelled or retained depending on the exchange.
    - Pitfall: stale orders hitting the book at reopening.
    - Build: a reopening-procedure test with order cleanup.
