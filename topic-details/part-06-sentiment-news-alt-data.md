# Part 6. Sentiment, News, and Alternative Data: Micro Details (topics 302 to 313)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 6.1 Text, news, and alternative-data signals

302. News ingestion pipelines (wires, RSS, APIs, social media)
     - Covers: collecting news in real time.
     - Details: wire services are fastest and costly, RSS and web scraping are slower. Store the source timestamp and your receive timestamp separately. Deduplicate syndicated stories.
     - Pitfall: duplicate or re-published stories counted as separate events.
     - Build: an ingestion service with deduplication and latency metrics.

303. Entity recognition and ticker mapping
     - Covers: linking text to securities.
     - Details: named-entity recognition finds companies, then a mapping table resolves names, aliases, subsidiaries, and tickers. Ambiguous names (for example common words) need context.
     - Pitfall: wrong mapping of similar names or old tickers.
     - Build: a labeled test set and precision/recall for the mapper.

304. Event detection (earnings, M&A, guidance, central bank, macro releases)
     - Covers: classifying what happened.
     - Details: rule-based patterns for scheduled events, classifiers for unscheduled ones. Tag event type, direction, and novelty.
     - Pitfall: treating a rehash of old news as a new event.
     - Build: an event taxonomy and a novelty score versus recent stories.

305. Sentiment scoring (lexicon, FinBERT, LLM-based)
     - Covers: turning text into scores.
     - Details: lexicons (such as Loughran-McDonald) are transparent but crude. Fine-tuned transformers like FinBERT do better on finance text. LLMs give flexible scoring but cost more and need versioning.
     - Pitfall: general-purpose lexicons mislabel finance words ("liability", "tax").
     - Build: compare three scorers on the same labeled sample and on forward returns.

306. Social media signals (Twitter/X, Reddit, StockTwits, Telegram)
     - Covers: retail and crowd attention.
     - Details: measure volume of mentions, sentiment, and unusual spikes relative to baseline. Account-quality filtering reduces bot noise.
     - Pitfall: platform API changes and manipulation by coordinated accounts.
     - Build: a mention-spike detector normalized by each ticker's baseline.

307. Earnings call and SEC filing analysis (10-K, 10-Q, 8-K)
     - Covers: text analysis of company disclosures.
     - Details: measure tone shifts, uncertainty words, and changes from the prior filing. Q&A sections often carry more information than prepared remarks.
     - Pitfall: boilerplate language dominating the text signal.
     - Build: year-over-year text-change scores per filing.

308. Economic calendar ingestion and macro-surprise modeling
     - Covers: scheduled macro events.
     - Details: store release time, consensus, actual, and prior. Surprise = actual - consensus, scaled by historical surprise standard deviation.
     - Pitfall: revisions and unit differences in actual values.
     - Build: a surprise series and a short-window reaction study per event.

309. Alternative data (satellite, web traffic, app data, card spend, shipping, job postings)
     - Covers: non-traditional datasets.
     - Details: they proxy for revenue, activity, or demand before official reports. Each needs a mapping to company, coverage assessment, and history length.
     - Pitfall: short history, panel changes, and signals that decay once widely sold.
     - Build: a coverage and bias report before any modeling.

310. Search trends and attention measures
     - Covers: public interest proxies.
     - Details: normalized search volume, Wikipedia page views, and news-count measures capture attention shifts.
     - Pitfall: sampling noise and scaling changes in search-trend data.
     - Build: attention z-scores and their lead-lag relation with volume.

311. News latency, timestamp accuracy, point-in-time handling
     - Covers: knowing when information was available.
     - Details: only information time-stamped before your decision time may be used. Vendor timestamps may reflect processing time, not publication.
     - Pitfall: look-ahead from using backfilled or reordered timestamps.
     - Build: audit of timestamp versus an independent source for a sample of events.

312. Signal decay and crowding for sentiment strategies
     - Covers: how fast sentiment edge fades.
     - Details: news-based alpha decays within minutes to days. Faster capture is needed, and crowded data sources lose edge.
     - Pitfall: backtesting with execution assumptions too slow or too fast for reality.
     - Build: return by time-since-news curves to find the usable horizon.

313. Fake news, manipulation, and bot filtering
     - Covers: data integrity.
     - Details: pump-and-dump messages, spoofed accounts, and fabricated press releases can trigger automated systems.
     - Pitfall: automated trading on single unverified sources.
     - Build: source-credibility scores, multi-source confirmation, and a halt rule for suspicious spikes.
