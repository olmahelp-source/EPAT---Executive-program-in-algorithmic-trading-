# Part 18. Human Factors, Case Studies, Emerging Topics, and Prerequisites: Micro Details (topics 829 to 850)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 18.1 Behavioral considerations

829. Trader psychology and discipline (discretionary or hybrid systems)
     - Covers: human behavior in trading.
     - Details: fear, greed, overconfidence, and revenge trading affect rule-following. Pre-commit to rules and limits, keep a journal.
     - Pitfall: overriding the system after a few losses.
     - Build: a trading journal and an override log reviewed weekly.

830. Behavioral biases and market anomalies
     - Covers: systematic errors by participants.
     - Details: anchoring, herding, disposition effect, and overreaction relate to momentum and reversal anomalies.
     - Pitfall: believing anomalies persist unchanged after discovery.
     - Build: map each bias to a testable hypothesis and test it.

## 18.2 Case studies in failure

831. Knight Capital (deployment and kill-switch failure)
     - Covers: a 2012 trading-software failure.
     - Details: a faulty deployment left old code active on one server, generating large unintended orders and huge losses in under an hour.
     - Pitfall: inconsistent deployments and no effective stop.
     - Build: checklist covering deployment consistency and kill-switch tests.

832. LTCM (leverage and correlation risk)
     - Covers: a 1998 hedge-fund collapse.
     - Details: high leverage on convergence trades, with correlations rising and liquidity vanishing in the crisis.
     - Pitfall: trusting historical correlations and liquidity under stress.
     - Build: leverage and liquidity stress scenarios for your book.

833. 2007 Quant Quake and crowded quant positions
     - Covers: August 2007 equity market-neutral losses.
     - Details: forced deleveraging by some funds hit similar positions held by others, causing sharp losses.
     - Pitfall: crowded factor exposures.
     - Build: crowding indicators and a deleveraging scenario test.

834. 2010 Flash Crash
     - Covers: May 2010 rapid market drop and rebound.
     - Details: a large automated sell order interacted with liquidity withdrawal, creating extreme prices.
     - Pitfall: market orders in thin conditions.
     - Build: replay a flash-crash scenario through your execution logic.

835. Volmageddon (2018 short-volatility collapse)
     - Covers: February 2018 volatility spike.
     - Details: short-volatility products lost most value in a day after a volatility surge and rebalancing flows.
     - Pitfall: selling convexity without loss limits.
     - Build: volatility-spike scenario for short-vol positions.

836. Archegos (hidden leverage and concentrated swaps)
     - Covers: 2021 forced liquidation.
     - Details: concentrated positions through total-return swaps across multiple banks produced hidden leverage and large losses when prices fell.
     - Pitfall: opaque exposure and counterparty concentration.
     - Build: aggregate look-through exposure and counterparty limits.

837. GameStop and short-squeeze dynamics
     - Covers: January 2021 squeeze.
     - Details: heavily shorted stock, retail buying, and options gamma contributed to rapid price rises and margin pressure.
     - Pitfall: unlimited loss in shorts.
     - Build: short-squeeze stress test with borrow recall.

838. Terra/Luna and FTX collapses (crypto custody and design failures)
     - Covers: 2022 crypto failures.
     - Details: an algorithmic stablecoin lost its peg and an exchange misused customer funds.
     - Pitfall: counterparty and design risk.
     - Build: exchange and stablecoin exposure caps.

839. Common pattern analysis (leverage, crowding, no kill switch, untested assumptions)
     - Covers: lessons across failures.
     - Details: recurring themes include excess leverage, crowded trades, inadequate controls, and reliance on benign historical data.
     - Pitfall: believing your case is different.
     - Build: a pre-launch checklist derived from these patterns.

## 18.3 Emerging topics

840. T+0 settlement and tokenized securities
     - Covers: faster settlement and on-chain securities.
     - Details: shorter settlement reduces counterparty risk and changes funding needs.
     - Pitfall: operational readiness for compressed timelines.
     - Build: settlement-timeline impact analysis.

841. Quantum computing for optimization
     - Covers: potential computing advances.
     - Details: quantum methods target certain optimization problems, with practical advantages for portfolios still unproven.
     - Pitfall: hype without a measured benefit.
     - Build: benchmark a quantum-inspired solver against classical.

842. Synthetic data and privacy-preserving research
     - Covers: data generation and privacy.
     - Details: generate realistic data for testing and sharing without exposing sensitive information.
     - Pitfall: synthetic data that misses real dependence structure.
     - Build: fidelity tests comparing real and synthetic statistics.

843. Federated and decentralized data sharing
     - Covers: collaborative modeling.
     - Details: learn from distributed data without centralizing it.
     - Pitfall: leakage through model updates.
     - Build: small federated-learning experiment.

844. Hardware acceleration beyond FPGA (GPU-based simulation and inference)
     - Covers: accelerated computing.
     - Details: GPUs speed up large simulations and model inference, though not ultra-low-latency paths.
     - Pitfall: transfer overhead outweighing gains for small tasks.
     - Build: GPU versus CPU benchmark on a Monte Carlo workload.

## 18.4 Prerequisites and learning path

845. Python, NumPy, pandas, and SQL fundamentals
     - Covers: core programming skills.
     - Details: data structures, vectorized operations, time-series handling in pandas, and SQL joins and window functions.
     - Pitfall: loops over rows where vectorization is available.
     - Build: clean and aggregate a tick dataset using pandas and SQL.

846. Linux, Git, and cloud basics
     - Covers: tooling.
     - Details: shell usage, processes, permissions, branching and merging, and basic cloud services.
     - Pitfall: unmanaged servers and unreviewed changes.
     - Build: deploy a small service from a Git repository to a cloud VM.

847. Probability and linear algebra refresher
     - Covers: math foundations.
     - Details: random variables, expectation, variance, conditional probability, matrix operations, eigenvalues.
     - Pitfall: using formulas without understanding assumptions.
     - Build: exercises computing portfolio variance with matrices.

848. Financial accounting basics
     - Covers: reading statements.
     - Details: the three statements, accruals, and key ratios.
     - Pitfall: ignoring cash flows.
     - Build: analyze one company's filings end to end.

849. Capstone project design (end-to-end paper-trading system)
     - Covers: integrating skills.
     - Details: data ingestion, strategy, backtest, risk, execution to a paper account, monitoring, and a report.
     - Pitfall: scope too large to finish.
     - Build: staged milestones with a working minimum version first.

850. Reading list (core quant textbooks, papers, and post-mortems)
     - Covers: structured study.
     - Details: pick a few core books on quantitative trading, risk, and market microstructure, plus papers on backtest overfitting and incident post-mortems.
     - Pitfall: collecting reading material without implementing anything.
     - Build: a reading plan tied to the build milestones.
