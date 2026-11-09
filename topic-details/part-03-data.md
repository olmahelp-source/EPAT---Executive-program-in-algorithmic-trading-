# Part 3. Data: Micro Details (topics 79 to 96)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 3.1 Market data engineering

79. Real-time feeds (WebSocket, FIX/FAST, exchange APIs)
    - Covers: live data delivery methods.
    - Details: WebSocket suits retail and crypto, FIX/FAST and binary multicast suit exchange feeds. Know snapshot versus incremental updates.
    - Pitfall: missing a sequence gap and building a wrong book.
    - Build: a feed handler that detects gaps and resubscribes for a snapshot.

80. Historical data sourcing and cleaning
    - Covers: acquiring and validating history.
    - Details: check for gaps, duplicates, outliers, zero or negative prices, and time-zone errors. Compare against a second source.
    - Pitfall: trusting a single vendor without validation.
    - Build: an automated cleaning pipeline with a rejected-rows report.

81. Corporate actions (splits, dividends, mergers, spin-offs) and adjustments
    - Covers: price and volume adjustments.
    - Details: split-adjust prices and volumes. Dividend-adjust for total return. Keep raw and adjusted series separately.
    - Pitfall: using adjusted prices for order sizing or price-level rules.
    - Build: an adjustment factor table with effective dates.

82. Tick, bar, and order-book storage (TimescaleDB, kdb+, QuestDB, ClickHouse)
    - Covers: time-series storage choices.
    - Details: columnar storage with time partitioning and compression. Consider query patterns, write rate, and retention.
    - Pitfall: choosing a database before measuring data volume.
    - Build: a benchmark loading one month of ticks into two candidates.

83. Data normalization and symbology mapping
    - Covers: consistent identifiers.
    - Details: map tickers, ISIN, CUSIP, FIGI, exchange codes, and contract codes with effective dates.
    - Pitfall: ticker reuse by different companies.
    - Build: a security-master table with validity ranges.

84. Handling gaps, bad ticks, and outliers
    - Covers: data quality filters.
    - Details: filters on price jump, spread, volume spikes, and crossed quotes. Distinguish real moves from errors.
    - Pitfall: filtering out real crashes.
    - Build: a bad-tick filter with tunable thresholds and an audit log.

85. Point-in-time and bitemporal data
    - Covers: knowing what was known when.
    - Details: store both effective time and knowledge time. Needed for restated fundamentals and revised macro data.
    - Pitfall: using revised data in a backtest that would not have been available.
    - Build: a table with as-of queries returning data as it was on a given date.

86. Clock synchronization (PTP/NTP) and timestamping
    - Covers: accurate event times.
    - Details: NTP gives milliseconds, PTP gives microseconds or better. Use exchange timestamps and your receive timestamps both.
    - Pitfall: clock drift misordering events across systems.
    - Build: log clock offset continuously and alert on drift.

87. Data vendor selection, licensing, and cost
    - Covers: choosing and contracting data sources.
    - Details: evaluate coverage, history depth, latency, adjustments, redistribution rights, and cost per user or per use.
    - Pitfall: license terms that forbid your intended use.
    - Build: a scoring sheet comparing vendors on your requirements.

88. Data quality dashboards and lineage
    - Covers: monitoring and tracing data.
    - Details: track completeness, latency, freshness, anomaly counts, and the source of every derived number.
    - Pitfall: silent data failure until a bad trade.
    - Build: daily data-health checks with alerts.

## 3.2 Fundamental data engineering

89. Sources (exchange filings, XBRL, vendors, company websites, regulators)
    - Covers: where fundamentals come from.
    - Details: filings are primary but vary in format. Vendors standardize but may restate and lag.
    - Pitfall: mixing vendor definitions of the same field.
    - Build: a source inventory with field definitions and lag per source.

90. Parsing and normalizing filings (XBRL tagging, PDF extraction, NLP on text)
    - Covers: turning documents into data.
    - Details: XBRL tags give structured values, but custom tags and PDFs need extraction. Validate that totals reconcile.
    - Pitfall: silent parsing errors on unusual layouts.
    - Build: a parser with accounting-identity checks (assets = liabilities + equity).

91. Ticker, identifier, and corporate-structure mapping (mergers, renames, delistings)
    - Covers: tracking entities across time.
    - Details: map by permanent identifier and keep history of ticker changes and parent-subsidiary links.
    - Pitfall: breaking history at a rename or merger.
    - Build: an entity-history table with a ticker alias list.

92. Handling currency, unit, and fiscal-year-end differences
    - Covers: comparability.
    - Details: figures may be in thousands or millions, in local currency, with different fiscal-year ends.
    - Pitfall: comparing a March year-end with a December year-end as if aligned.
    - Build: calendarize financials to a common period and convert currency at period-appropriate rates.

93. Estimates data (consensus, revisions, point-in-time snapshots)
    - Covers: analyst forecasts.
    - Details: store each estimate with its timestamp. Consensus changes as analysts update.
    - Pitfall: using final consensus as if known earlier.
    - Build: a daily snapshot table of consensus per company.

94. Survivorship-free and delisting-return-inclusive datasets
    - Covers: including failed companies.
    - Details: delisted names must stay in the universe up to delisting, with the delisting return applied.
    - Pitfall: backtests that quietly exclude bankruptcies.
    - Build: verify the universe at past dates includes later-delisted names.

95. Data-vendor discrepancies and reconciliation
    - Covers: handling disagreement between sources.
    - Details: define a source hierarchy, flag differences above tolerance, and log decisions.
    - Pitfall: swapping vendors mid-project without a reconciliation.
    - Build: a reconciliation report comparing key fields across vendors.

96. Fundamental-to-price alignment (lags, announcement vs. effective dates)
    - Covers: joining fundamentals with prices.
    - Details: use the filing or announcement date plus a safety lag, not the period-end date.
    - Pitfall: look-ahead by aligning on period end.
    - Build: an alignment function with a configurable lag and a test showing no future leakage.
