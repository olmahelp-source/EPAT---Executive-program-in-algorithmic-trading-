# Part 13. Execution: Micro Details (topics 520 to 630)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 13.1 Execution architecture and components

520. Execution pipeline overview (signal, target position, order generation, routing, fills, position update)
     - Covers: the end-to-end path of a trade.
     - Details: signal produces a target position, the order generator computes the difference from current and pending positions, risk approves, the router sends, fills update positions.
     - Pitfall: computing the difference from confirmed positions only and ignoring working orders.
     - Build: a sequence diagram and an integration test that follows one trade through every stage.

521. Order Management System (OMS): order store, validation, state, and audit
     - Covers: the system of record for orders.
     - Details: stores every order and state change with timestamps and reason codes, validates inputs, and exposes queries by strategy, instrument, and status.
     - Pitfall: state held only in memory and lost on restart.
     - Build: a persistent order store with an append-only event log.

522. Execution Management System (EMS): algo selection, routing, and trader controls
     - Covers: how orders are worked.
     - Details: picks the algorithm and venue, applies parameters, and lets a trader pause, resume, or override.
     - Pitfall: controls with no audit trail.
     - Build: an EMS interface that logs every control action with the user and time.

523. Separation of concerns (strategy, risk, OMS, EMS, gateway) and the interfaces between them
     - Covers: component boundaries.
     - Details: strategies emit intents only, risk can veto, OMS owns state, EMS owns working logic, gateway owns protocol details.
     - Pitfall: strategies talking directly to the broker.
     - Build: interface definitions with contract tests between each pair.

524. Parent/child order model (parent order slicing into child orders, aggregation of fills)
     - Covers: working large orders.
     - Details: parent holds total quantity and constraints, children are the actual market orders. Fills on children roll up to the parent.
     - Pitfall: parent and child quantities drifting out of sync after cancels.
     - Build: invariants test that child fills always sum to the parent's executed quantity.

525. Order aggregation, netting, and internal crossing across strategies
     - Covers: combining flow.
     - Details: net opposite orders from different strategies internally to save spread and fees, then allocate fills back with a fair rule.
     - Pitfall: unfair allocation between strategies or accounts.
     - Build: a netting engine with documented allocation rules.

526. Execution service high availability and recovery after restart
     - Covers: surviving failure.
     - Details: persist state, reload open orders, query the broker for actual order and position status, and reconcile before resuming.
     - Pitfall: restarting and resending orders that are already working.
     - Build: a restart test that kills the service mid-trade and verifies correct recovery.

527. Paper trading and simulated exchange
     - Covers: running without real money.
     - Details: paper accounts may fill optimistically and ignore impact. A simulated exchange can model queues and latency.
     - Pitfall: treating paper results as proof of live profitability.
     - Build: a simulated exchange with configurable latency and fill rules, used in integration tests.

## 13.2 Order state machine and lifecycle correctness

528. Order state machine (new, pending, acknowledged, partially filled, filled, cancelled, rejected, expired)
     - Covers: allowed transitions.
     - Details: define valid transitions and reject impossible ones. Include pending-cancel and pending-replace states.
     - Pitfall: a state machine that allows impossible transitions, hiding bugs.
     - Build: a transition table with property-based tests.

529. Handling unknown or out-of-order states (pending-cancel races, late fills after cancel)
     - Covers: message-order problems.
     - Details: a fill can arrive after you sent a cancel. Treat the fill as authoritative and update positions.
     - Pitfall: ignoring a fill because the order is "cancelled".
     - Build: tests injecting late fills and reordered messages.

530. Idempotent order submission and client order ID design
     - Covers: preventing duplicates.
     - Details: unique client order IDs, generated before sending and persisted, so a retry reuses the same ID and the venue can reject duplicates.
     - Pitfall: generating a new ID on each retry.
     - Build: an ID generator and a duplicate-submission test.

531. Retry policy, timeouts, and duplicate-order prevention
     - Covers: handling no response.
     - Details: after a timeout, query order status before retrying. Use bounded retries with backoff.
     - Pitfall: blind retries that double the position.
     - Build: status-query-then-retry logic with a simulated lost acknowledgment.

532. Order amendment, cancel/replace semantics, and priority loss
     - Covers: changing live orders.
     - Details: some amendments keep queue priority (size down), others lose it (price change or size up). Replace creates a new order ID on many venues.
     - Pitfall: assuming an amendment is atomic and keeps priority.
     - Build: per-venue amendment rules table.

533. Fill processing (partial fills, busted fills, corrections, average-price computation)
     - Covers: handling executions.
     - Details: average price = sum(price x quantity) / sum(quantity). Handle trade busts and corrections that reverse earlier fills.
     - Pitfall: rounding errors and unprocessed busts.
     - Build: fill handler with bust and correction tests.

534. Position update on fills vs. on acknowledgments, and pending-exposure accounting
     - Covers: which events change positions.
     - Details: positions update on fills. Risk should include pending (working) order exposure.
     - Pitfall: risk blind to orders still working.
     - Build: exposure = position + working buys or sells, used in limit checks.

535. Order-state reconciliation with broker and exchange
     - Covers: comparing your view with theirs.
     - Details: periodic query of open orders and executions and diff against your OMS, with automated repair for safe cases and alerts for others.
     - Pitfall: trusting local state indefinitely.
     - Build: a reconciliation job with break classification.

536. Orphaned and ghost orders: detection and cleanup at startup and shutdown
     - Covers: stray orders.
     - Details: orders present at the broker but unknown locally, or known locally but gone at the broker.
     - Pitfall: orphan orders executing after the strategy is off.
     - Build: startup scan that cancels or adopts orphans by policy.

537. End-of-day and start-of-day order and position carry-over
     - Covers: session boundaries.
     - Details: decide which orders persist (GTC), what is cancelled, and how positions are reloaded and verified each morning.
     - Pitfall: stale day orders or missing overnight positions.
     - Build: daily open and close checklists automated with reports.

## 13.3 Pre-trade controls in the execution path

538. Price collars, fat-finger checks, and sanity bands against the last/mid price
     - Covers: bad prices.
     - Details: reject orders priced more than a set percentage or number of ticks from a reference price.
     - Pitfall: using a stale reference price.
     - Build: collar check with reference-price freshness test.

539. Quantity, notional, and order-rate limits per strategy, account, and instrument
     - Covers: size and speed caps.
     - Details: hard limits at multiple levels, with a lower soft limit for warnings.
     - Pitfall: limits configured but never tested.
     - Build: limit configuration with tests that exceed each limit.

540. Duplicate and runaway-order detection
     - Covers: loops and repeated orders.
     - Details: detect many identical orders in a short window or rapidly growing exposure.
     - Pitfall: loops that send orders faster than a human can stop.
     - Build: rate and similarity detectors with automatic strategy pause.

541. Buying-power, margin, and borrow checks before submission
     - Covers: capacity checks.
     - Details: estimate margin impact and confirm shares are available to borrow for shorts.
     - Pitfall: order rejected by broker after the strategy assumed fill.
     - Build: pre-submission capacity check using broker-reported values.

542. Restricted-list, compliance, and market-hours checks
     - Covers: rule checks.
     - Details: blocked instruments, trading windows, and compliance holds.
     - Pitfall: stale restricted lists.
     - Build: lists loaded from a controlled source with version stamps.

543. Self-trade and cross-strategy wash-trade prevention
     - Covers: avoiding trading against yourself.
     - Details: compare new orders with your resting orders on the opposite side at crossing prices.
     - Pitfall: separate strategies that unknowingly cross.
     - Build: pre-trade cross-check against all internal working orders.

544. Kill-switch integration at the OMS, gateway, and broker levels
     - Covers: layered emergency stop.
     - Details: OMS blocks new orders, gateway cancels working orders, and broker-side tools provide an independent backstop.
     - Pitfall: a single layer that fails with the rest of the system.
     - Build: drills that trigger each layer separately.

545. Throttling and circuit breakers on message rates
     - Covers: protecting the gateway and venue.
     - Details: token-bucket throttles and automatic pause when rejects or errors exceed thresholds.
     - Pitfall: retry storms after a venue slowdown.
     - Build: throttle and breaker with metrics and alerts.

## 13.4 Execution algorithms

546. Schedule-based algos (TWAP, VWAP, and volume-curve estimation)
     - Covers: time- and volume-scheduled execution.
     - Details: TWAP slices evenly by time. VWAP follows a historical intraday volume curve. Curve estimation uses averages over similar days.
     - Pitfall: predictable slicing that others exploit, and curves that ignore event days.
     - Build: VWAP scheduler and a comparison of realized versus benchmark VWAP.

547. Participation algos (POV, percentage of volume) and volume forecasting
     - Covers: trading as a share of market volume.
     - Details: order size per interval = participation rate x observed volume. Cap rates to limit impact.
     - Pitfall: chasing volume spikes that coincide with adverse moves.
     - Build: POV engine with minimum and maximum rate limits.

548. Implementation shortfall and arrival-price algos (Almgren-Chriss style trade-off of cost and risk)
     - Covers: front-loaded execution to reduce risk.
     - Details: trade faster when risk aversion is high or alpha decays quickly, slower when impact dominates.
     - Pitfall: calibrating impact and volatility from the wrong period.
     - Build: trajectory generator for several risk-aversion values.

549. Close, open, and auction-targeting algos
     - Covers: auction execution.
     - Details: aim at closing or opening prices, balancing continuous trading before the auction and order entry for the auction.
     - Pitfall: missing auction order cutoffs.
     - Build: cutoff-aware auction order scheduler.

550. Passive and liquidity-seeking algos (post, peg, and capture rebates)
     - Covers: providing liquidity.
     - Details: post at or inside the touch, reprice as the market moves, and cross the spread only when urgency rises.
     - Pitfall: unfilled orders while price moves away.
     - Build: logic for when to switch from passive to aggressive.

551. Iceberg and reserve-order logic and anti-gaming randomization
     - Covers: hiding size.
     - Details: display a small slice and randomize slice size and timing to avoid detection.
     - Pitfall: regular patterns that reveal the algorithm.
     - Build: randomization with bounded parameters.

552. Sniper, opportunistic, and dark-liquidity-seeking algos
     - Covers: waiting for good prices.
     - Details: strike when displayed size or price is favorable, and ping dark venues for hidden liquidity.
     - Pitfall: information leakage from pinging.
     - Build: opportunistic algo with spread and size triggers.

553. Pairs and spread execution (legging risk, simultaneous execution, and hedge ratios)
     - Covers: multi-leg trades.
     - Details: send both legs together, or leg the less liquid first, and manage the unhedged exposure if one leg fills alone.
     - Pitfall: leg fills without the hedge in fast markets.
     - Build: legging-risk limits and timeout actions.

554. Basket and portfolio execution (program trading, risk-balanced scheduling, and target-weight rebalancing)
     - Covers: trading many names together.
     - Details: schedule trades to keep exposures balanced during execution and manage residual risk.
     - Pitfall: large unhedged exposure mid-basket.
     - Build: risk-balanced basket scheduler.

555. Options execution (multi-leg orders, spread books, implied pricing, and delta-hedge timing)
     - Covers: trading option structures.
     - Details: use native spread orders where available, price legs from implied volatility, and hedge delta with the underlying.
     - Pitfall: legs executed separately at poor prices.
     - Build: multi-leg order using spread-book quotes.

556. Futures roll execution (calendar spread vs. leg-by-leg)
     - Covers: rolling contracts.
     - Details: calendar-spread order locks the roll price difference, leg-by-leg exposes you to leg risk.
     - Pitfall: rolling at illiquid times.
     - Build: roll scheduler with liquidity-aware timing.

557. FX execution (RFQ, streaming prices, last-look, and aggregator liquidity)
     - Covers: currency trading.
     - Details: liquidity comes from dealer streams with last-look, so rejection and hold time matter.
     - Pitfall: ignoring reject rates when comparing venues.
     - Build: last-look reject and hold-time statistics per liquidity provider.

558. Algorithm parameter selection and adaptive tuning (urgency, aggression, limit price, and end time)
     - Covers: algo settings.
     - Details: urgency, limit price protection, start and end times, and participation caps.
     - Pitfall: default parameters used for all orders.
     - Build: a parameter table by order size and liquidity.

559. Algo selection logic by order size, liquidity, volatility, and alpha-decay horizon
     - Covers: choosing the algorithm.
     - Details: small liquid orders may be sent directly, large orders get scheduled algos, fast-decaying alpha favors urgency.
     - Pitfall: using one algorithm for every case.
     - Build: rules-based selector with logged rationale.

560. Optimal execution theory (square-root impact, trade scheduling, and risk-aversion)
     - Covers: theoretical foundation.
     - Details: impact roughly proportional to sigma x sqrt(Q / V). Optimal schedules balance expected cost and variance of cost.
     - Pitfall: using theory without calibrating to your venues.
     - Build: calibrate an impact model on your fill data.

561. Anti-gaming and information-leakage control (randomized sizes, timing, and venue rotation)
     - Covers: reducing detectability.
     - Details: avoid fixed patterns in time, size, and price level. Rotate venues.
     - Pitfall: randomization that raises cost without reducing leakage.
     - Build: measure adverse price moves after your child orders.

## 13.5 Order types and instructions in execution

562. Smart limit-price logic (mid, touch, improving price, and price-chasing control)
     - Covers: choosing limit prices.
     - Details: price relative to mid or touch with a maximum chase distance.
     - Pitfall: chasing price without a cap.
     - Build: limit-price policy with a cap and a cancel-or-cross rule.

563. Marketable-limit and protection-price orders
     - Covers: aggressive orders with a price bound.
     - Details: a limit through the touch ensures a fill up to the bound, avoiding market-order extremes.
     - Pitfall: protection too tight, causing unfilled urgent orders.
     - Build: protection set from spread and volatility.

564. Conditional orders (stop-limit, trailing, and market-if-touched) and where they are held (client-side vs. exchange-side)
     - Covers: trigger-based orders.
     - Details: exchange-held orders survive disconnects, client-held ones do not.
     - Pitfall: client-side stops that disappear when your system is down.
     - Build: preference for exchange-side triggers where available.

565. Client-side simulated order types and their failure modes during disconnects
     - Covers: emulation risk.
     - Details: simulated stops, brackets, or trailing stops fail if the process stops.
     - Pitfall: false protection.
     - Build: documented list of simulated orders and a fallback plan.

566. Aggressive vs. passive decision logic (spread crossing, queue-position estimate, and fill probability)
     - Covers: trade-off between cost and fill certainty.
     - Details: estimate fill probability for a passive order in the time available versus the cost of crossing.
     - Pitfall: ignoring adverse selection on passive fills.
     - Build: simple fill-probability model compared with realized fills.

567. Order-sizing against displayed depth and expected impact
     - Covers: size selection.
     - Details: limit child order size to a fraction of displayed depth.
     - Pitfall: depth that disappears when you send.
     - Build: depth-based sizing rule and realized-impact check.

568. Order flags (post-only, reduce-only, hidden, minimum quantity, and all-or-none)
     - Covers: instructions that alter handling.
     - Details: post-only avoids taking, reduce-only prevents increasing a position, minimum quantity avoids small fills.
     - Pitfall: rejections for post-only orders that would cross.
     - Build: flag usage rules per venue.

569. Exchange-specific order types and matching-engine rules
     - Covers: venue differences.
     - Details: priority rules (price-time, pro-rata), supported types, and special features.
     - Pitfall: assuming all venues behave like your main one.
     - Build: a per-venue behavior sheet.

## 13.6 Smart order routing and venue selection

570. Venue characteristics (fees, fill rates, latency, toxicity, and hidden liquidity)
     - Covers: venue profile.
     - Details: record fee schedule, fill rate, markout after fills, and latency per venue.
     - Pitfall: choosing venues by fee alone.
     - Build: per-venue scorecard.

571. Routing logic (spray, sweep, waterfall, and cost-based routing)
     - Covers: how to allocate order across venues.
     - Details: spray sends to many at once, waterfall goes in sequence, cost-based picks by expected net price.
     - Pitfall: double fills from simultaneous routing.
     - Build: routing simulator with fill-overlap handling.

572. Best execution policy and evidence capture
     - Covers: documenting decisions.
     - Details: define the factors (price, cost, speed, likelihood) and keep records showing compliance.
     - Pitfall: no evidence when asked.
     - Build: per-order record of venues considered and chosen.

573. Fragmentation and consolidated vs. direct feeds (NBBO, protected quotes, and trade-through rules)
     - Covers: multiple venues quoting the same instrument.
     - Details: consolidated feeds are slower, direct feeds are faster but need aggregation.
     - Pitfall: routing with stale consolidated data.
     - Build: aggregated book from direct feeds.

574. Dark pools, midpoint crossing, and block trading
     - Covers: non-displayed liquidity.
     - Details: midpoint crossing saves spread, minimum sizes apply, and fill rates are uncertain.
     - Pitfall: toxic dark venues with adverse markouts.
     - Build: markout analysis per dark venue.

575. Internalization, payment for order flow, and conflicts of interest
     - Covers: broker routing incentives.
     - Details: brokers may route retail flow to wholesalers that pay them.
     - Pitfall: assuming your broker routes for best price.
     - Build: compare execution quality across brokers.

576. Order-protection and locked/crossed market handling
     - Covers: unusual book states.
     - Details: locked or crossed quotes can occur across venues, and routing must handle them safely.
     - Pitfall: treating a crossed book as a trade signal.
     - Build: detection and handling policy.

577. Dynamic venue scoring using realized fill quality and markouts
     - Covers: adaptive routing.
     - Details: update venue scores using recent fill rates and post-fill price moves.
     - Pitfall: noisy scores from small samples.
     - Build: exponentially weighted venue scores with minimum samples.

578. Cross-listed and multi-currency routing
     - Covers: trading a name in multiple venues or currencies.
     - Details: compare prices after FX conversion and consider settlement and fees.
     - Pitfall: ignoring FX and transfer costs.
     - Build: FX-adjusted cross-listing price comparator.

## 13.7 Connectivity and protocols

579. Broker and exchange connectivity (FIX, REST, WebSocket, and native binary protocols)
     - Covers: protocol choices.
     - Details: FIX is standard for institutional, REST and WebSocket common for retail and crypto, binary protocols for speed.
     - Pitfall: building on a protocol without checking rate limits and reliability.
     - Build: protocol comparison table for your venues.

580. FIX in depth (message types, tags, session vs. application layer, sequence recovery, and custom tags)
     - Covers: FIX details.
     - Details: NewOrderSingle, ExecutionReport, OrderCancelRequest, OrderCancelReplaceRequest. Session layer handles logon, heartbeats, and sequence numbers.
     - Pitfall: misunderstanding ExecutionReport types (ExecType vs. OrdStatus).
     - Build: FIX message parser with tests from real logs.

581. Exchange native protocols (ITCH/OUCH, SBE, and binary gateways)
     - Covers: low-level exchange interfaces.
     - Details: ITCH for market data, OUCH for order entry, SBE for compact messages.
     - Pitfall: parsing errors from fixed-length fields.
     - Build: a decoder verified against sample exchange files.

582. Broker API behavior (rate limits, order-ID semantics, reject codes, and quirks per broker)
     - Covers: practical differences.
     - Details: rate limits per second and per day, order ID reuse, and partial-fill reporting.
     - Pitfall: undocumented behaviors discovered in production.
     - Build: a quirks log per broker with automated tests.

583. Session management (logon, heartbeat, reconnect, sequence reset, and failover gateways)
     - Covers: keeping connections alive.
     - Details: reconnect with backoff, resume from the correct sequence, and failover to a backup gateway.
     - Pitfall: reconnect loops that hammer the venue.
     - Build: reconnect logic with jitter and sequence recovery tests.

584. Market data and order-entry path separation
     - Covers: independent paths.
     - Details: separate connections so a data surge does not block orders.
     - Pitfall: shared queues causing order delays.
     - Build: separate threads and queues with latency monitoring.

585. Drop copy, trade confirmations, and independent fill feeds
     - Covers: independent verification.
     - Details: a second feed of fills allows detecting missed executions.
     - Pitfall: relying on a single execution-report stream.
     - Build: compare drop copy to OMS fills in real time.

586. Gateway abstraction layer for multi-broker support
     - Covers: one interface for many brokers.
     - Details: common order and event model with adapters per broker.
     - Pitfall: leaking broker-specific details into strategies.
     - Build: adapter interface with a mock broker for tests.

587. Reject-code handling and error classification (retryable vs. fatal)
     - Covers: interpreting errors.
     - Details: classify as retry, modify, or stop. For example, rate limit is retry later, invalid symbol is fatal.
     - Pitfall: retrying fatal errors.
     - Build: error-code mapping with default-safe behavior.

588. Cancel-on-disconnect and session-loss behavior
     - Covers: what happens when a session drops.
     - Details: know whether the venue cancels your orders and design accordingly.
     - Pitfall: assuming orders are cancelled when they are not.
     - Build: verified per-venue behavior documented and drilled.

589. Testing environments, certification, and exchange conformance testing
     - Covers: pre-production tests.
     - Details: exchanges offer test environments and require conformance testing before live access.
     - Pitfall: differences between test and production behavior.
     - Build: a conformance test suite and a record of results.

590. Broker outage handling and failover to a secondary broker or venue
     - Covers: redundancy.
     - Details: define how to hedge or flatten via a backup route.
     - Pitfall: backup routes that were never tested.
     - Build: failover drill with a secondary account.

## 13.8 Market impact and liquidity-aware execution

591. Market impact estimation (temporary vs. permanent, square-root model, and calibration from own fills)
     - Covers: measuring impact.
     - Details: regress slippage against size relative to volume and volatility. Separate temporary reversion from permanent move.
     - Pitfall: attributing alpha-related price moves to impact.
     - Build: impact calibration on your data with confidence intervals.

592. Participation-rate limits and liquidity-based position-size caps
     - Covers: size limits.
     - Details: cap per-order and total position as a fraction of average daily volume.
     - Pitfall: positions that cannot be exited quickly.
     - Build: caps enforced in pre-trade checks.

593. Intraday volume and spread patterns, and time-of-day execution scheduling
     - Covers: timing patterns.
     - Details: volume is high at open and close, spreads are wider at open.
     - Pitfall: trading in illiquid midday periods without adjusting.
     - Build: intraday volume and spread curves per instrument.

594. Liquidity estimation (depth, resilience, and hidden liquidity)
     - Covers: measuring liquidity.
     - Details: depth at levels, how fast the book refills after trades, and fill-based estimates of hidden size.
     - Pitfall: relying on displayed depth only.
     - Build: resilience and depth metrics from order-book data.

595. Order-book-based execution signals (imbalance, microprice, and short-term price prediction)
     - Covers: short-horizon signals for execution.
     - Details: microprice = (bid x ask size + ask x bid size) / (bid size + ask size). Imbalance predicts next price move direction.
     - Pitfall: signals that cannot cover costs.
     - Build: execution timing using imbalance with measured benefit.

596. Trading around events (auctions, announcements, expiries, and index rebalances)
     - Covers: special periods.
     - Details: liquidity and volatility patterns change around events.
     - Pitfall: running normal algos through events.
     - Build: event-aware algo settings.

597. Handling illiquid instruments, wide spreads, and thin books
     - Covers: difficult markets.
     - Details: use limit orders, smaller sizes, longer horizons, and avoid market orders.
     - Pitfall: marking positions at stale mid.
     - Build: illiquid-instrument rule set.

598. Capacity limits implied by execution costs
     - Covers: how much capital is deployable.
     - Details: increase size until marginal cost equals marginal edge.
     - Pitfall: ignoring impact growth with scale.
     - Build: capacity curve per strategy.

599. Pre-trade cost estimation and go/no-go decisions
     - Covers: cost-aware trading.
     - Details: estimate spread, fees, and impact before sending, and skip trades with edge below cost.
     - Pitfall: trading signals whose edge is below cost.
     - Build: pre-trade cost estimator and threshold.

## 13.9 Execution for specific products

600. Equities (lot sizes, auctions, short-sale rules, and fractional shares)
     - Covers: stock-specific execution.
     - Details: lot sizes, auction participation, short-sale restrictions, and corporate-action impact on open orders.
     - Pitfall: open orders at pre-split prices.
     - Build: corporate-action-aware order handling.

601. Futures (roll, tick size, calendar spreads, and settlement windows)
     - Covers: futures execution.
     - Details: tick values, margin, daily settlement, and last-trading-day rules.
     - Pitfall: accidental holding into delivery.
     - Build: expiry guardrails that block new positions near expiry.

602. Options (strike and expiry selection, spread-order books, early-exercise and assignment handling, and implied-vol quoting)
     - Covers: option execution specifics.
     - Details: quote in price or implied volatility, handle assignment events, and manage exercise decisions.
     - Pitfall: unmanaged assignment.
     - Build: assignment handler and exercise-decision policy.

603. FX (spot vs. forward, value dates, and swap points)
     - Covers: currency execution.
     - Details: value-date conventions, rollover charges, and forward points.
     - Pitfall: rollover costs on carry trades.
     - Build: value-date calculator and swap-cost tracker.

604. Fixed income (RFQ, dealer-to-client, and TRACE-style reporting)
     - Covers: bond execution.
     - Details: mostly dealer-based, with price discovery by quotes and post-trade reporting.
     - Pitfall: stale indicative prices.
     - Build: RFQ workflow with quote capture.

605. Crypto (CEX order books, perpetual-swap mechanics, and DEX routing with gas and slippage)
     - Covers: crypto execution.
     - Details: exchange API limits, funding payments, and on-chain transaction costs and slippage.
     - Pitfall: failed or front-run on-chain transactions.
     - Build: DEX route estimator including gas and slippage.

606. Cross-asset hedges executed together (delta hedge with underlying, and FX hedge for foreign positions)
     - Covers: coordinated hedging.
     - Details: send hedge and main orders together or immediately after fills.
     - Pitfall: unhedged time windows.
     - Build: hedge trigger on fills with timing metrics.

## 13.10 Execution under stress and abnormal conditions

607. Degraded-mode logic (stale data, partial connectivity, and feed disagreement)
     - Covers: operating with problems.
     - Details: define actions when feeds are stale, disagree, or partially fail.
     - Pitfall: continuing normal behavior with bad data.
     - Build: degraded-mode state machine.

608. Behavior during halts, auctions, limit-up/limit-down, and volatility interruptions
     - Covers: market stoppages.
     - Details: orders may be rejected, held, or queued.
     - Pitfall: resubmitting into halts.
     - Build: halt detection and pause logic.

609. Handling rejected, stuck, or unconfirmed orders and positions of unknown state
     - Covers: uncertainty.
     - Details: query status, treat unknown as possibly filled for risk, and reconcile.
     - Pitfall: assuming unconfirmed means unfilled.
     - Build: unknown-state exposure treatment.

610. Emergency flatten, reduce-only, and liquidation procedures
     - Covers: exit under duress.
     - Details: prioritized exit by risk and liquidity, using reduce-only to avoid reversal.
     - Pitfall: flatten commands that create opposite positions.
     - Build: tested flatten procedure with reduce-only.

611. Partial-fill exposure management for multi-leg and pairs trades
     - Covers: incomplete spreads.
     - Details: monitor hedge ratio after partial fills and rebalance or unwind.
     - Pitfall: unhedged residuals.
     - Build: residual-exposure monitor.

612. Latency spikes and queue backlogs in the order path
     - Covers: delay detection.
     - Details: monitor queue depth and end-to-end latency, then pause or shed load.
     - Pitfall: sending orders based on very old signals.
     - Build: signal-age check before sending.

613. Controlled shutdown, restart, and resume procedures
     - Covers: planned stops.
     - Details: stop new orders, handle working orders, save state, and resume with reconciliation.
     - Pitfall: resuming without checking broker state.
     - Build: documented and automated shutdown and resume.

614. Manual intervention workflows and four-eyes approval
     - Covers: human actions.
     - Details: clear roles, approvals for risky actions, and logs.
     - Pitfall: undocumented manual trades.
     - Build: approval workflow with audit.

## 13.11 Latency engineering and high-frequency execution

615. Latency budget and measurement (tick-to-trade, wire-to-wire, and percentile tracking)
     - Covers: measuring delay.
     - Details: record timestamps at each stage and track median, 99th, and 99.9th percentiles.
     - Pitfall: tracking averages only.
     - Build: timestamped pipeline and percentile dashboard.

616. Network design (co-location, cross-connects, microwave links, and kernel bypass)
     - Covers: network speed.
     - Details: co-location minimizes distance, and kernel bypass reduces software stack delay.
     - Pitfall: investing in network before fixing software latency.
     - Build: latency breakdown by component.

617. Hardware acceleration (FPGA, SmartNICs, and GPU where relevant)
     - Covers: specialized hardware.
     - Details: FPGAs give deterministic, low-latency processing for simple logic.
     - Pitfall: high development cost for small edge.
     - Build: cost-benefit analysis before adoption.

618. Software optimization (lock-free queues, CPU pinning, NUMA, and garbage-collection control)
     - Covers: code-level tuning.
     - Details: avoid locks and allocations on the hot path, pin threads, and control memory.
     - Pitfall: premature optimization.
     - Build: profile first, then optimize hot spots.

619. Time synchronization and hardware timestamping
     - Covers: accurate timing.
     - Details: PTP with hardware timestamps for precise measurements.
     - Pitfall: unsynchronized clocks distort latency measurement.
     - Build: clock-offset monitoring.

620. Latency arbitrage, speed races, and queue-position strategies
     - Covers: speed-based strategies.
     - Details: strategies that depend on being faster than others.
     - Pitfall: competing against better-resourced firms.
     - Build: honest assessment of where you rank.

621. Cost-benefit of speed (when low latency is not worth building)
     - Covers: decision to invest.
     - Details: compare the edge sensitivity to latency with the cost of reducing it.
     - Pitfall: chasing microseconds for strategies that decay over minutes.
     - Build: edge versus latency curve.

622. Determinism and jitter control
     - Covers: consistent timing.
     - Details: stable latency can matter more than the lowest average.
     - Pitfall: random pauses from garbage collection or scheduling.
     - Build: jitter measurement and mitigation.

## 13.12 Execution testing, simulation, and quality assurance

623. Execution simulator design (fill models, queue models, and latency models)
     - Covers: realistic simulation.
     - Details: combine queue position, partial fills, and latency into fill logic.
     - Pitfall: optimistic fill assumptions.
     - Build: simulator calibrated to live fills.

624. Replay-based testing with recorded market data and order flow
     - Covers: realistic scenario tests.
     - Details: replay past sessions including crises.
     - Pitfall: incomplete recordings.
     - Build: library of recorded sessions.

625. Paper-trading limitations vs. live fills (no market impact and optimistic fills)
     - Covers: gaps between paper and live.
     - Details: paper often fills at the touch with no impact.
     - Pitfall: scaling based on paper results.
     - Build: compare paper to small live trades.

626. Fault injection (disconnects, duplicate messages, delayed acknowledgments, and rejects)
     - Covers: failure testing.
     - Details: inject failures in test and verify correct handling.
     - Pitfall: only testing the happy path.
     - Build: fault-injection harness with scenarios.

627. Algorithm unit tests and regression suites with expected schedules
     - Covers: algo correctness.
     - Details: assert expected child-order schedules for fixed inputs.
     - Pitfall: untested parameter edge cases.
     - Build: regression tests with golden outputs.

628. Shadow-mode execution and canary rollout of new algos
     - Covers: safe deployment.
     - Details: run new algo in shadow, then route a small share of orders.
     - Pitfall: full rollout without staged testing.
     - Build: staged rollout plan and metrics gates.

629. Production monitoring of execution (fill rates, rejects, slippage, and latency)
     - Covers: live quality metrics.
     - Details: real-time dashboards with alerts on drift.
     - Pitfall: no alerts until after losses.
     - Build: execution dashboard with thresholds.

630. Post-trade review loop (feeding transaction-cost analytics back into algo parameters)
     - Covers: continuous improvement.
     - Details: review slippage by algo, venue, and size, then adjust parameters.
     - Pitfall: tuning to noise.
     - Build: monthly review with statistical checks.
