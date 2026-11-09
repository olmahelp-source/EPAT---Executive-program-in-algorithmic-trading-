# Part 8. Artificial Intelligence and Machine Learning: Micro Details (topics 355 to 398)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 8.1 Machine learning

355. Supervised learning (linear models, SVM, k-NN)
     - Covers: baseline predictive models.
     - Details: start with linear and regularized models as baselines. Use time-aware splits and a naive benchmark such as zero or historical mean.
     - Pitfall: random train-test splits that leak future information.
     - Build: a baseline model with a walk-forward evaluation.

356. Tree ensembles (Random Forest, XGBoost, LightGBM, CatBoost)
     - Covers: non-linear tabular models.
     - Details: handle interactions and mixed features without scaling. Control depth, learning rate, and minimum leaf size to limit overfitting.
     - Pitfall: high in-sample fit on noisy financial targets.
     - Build: gradient-boosted model with early stopping on a purged validation set.

357. Unsupervised learning (k-means, hierarchical, DBSCAN, GMM)
     - Covers: structure discovery.
     - Details: clustering groups assets or regimes. Choose number of clusters with stability checks, not only silhouette scores.
     - Pitfall: clusters that change from sample to sample.
     - Build: asset clusters validated across time windows.

358. Dimensionality reduction (PCA, ICA, autoencoders, t-SNE, UMAP)
     - Covers: compressing features.
     - Details: PCA gives orthogonal components. t-SNE and UMAP are for visualization, not for predictive features.
     - Pitfall: fitting PCA on the full sample before splitting.
     - Build: PCA fit inside each training fold only.

359. Financial labeling (triple barrier, meta-labeling)
     - Covers: defining targets.
     - Details: triple barrier labels outcomes by profit target, stop, or time limit. Meta-labeling predicts whether to act on a primary signal and sizes the bet.
     - Pitfall: fixed-horizon labels that ignore path and risk.
     - Build: triple-barrier labels with volatility-scaled barriers.

360. Sample weighting, uniqueness, sequential bootstrap
     - Covers: handling overlapping labels.
     - Details: overlapping outcomes mean samples are not independent. Weight by uniqueness or return attribution.
     - Pitfall: treating overlapped samples as independent, which inflates confidence.
     - Build: compute average uniqueness and use it as sample weights.

361. Purged/embargoed and combinatorial purged cross-validation
     - Covers: leak-free validation.
     - Details: purging removes training samples overlapping test periods. Embargo skips samples right after the test window. Combinatorial purged CV produces many backtest paths.
     - Pitfall: standard k-fold on time series.
     - Build: purged k-fold and comparison of scores versus naive k-fold.

362. Feature engineering, selection, and importance (MDI, MDA, SHAP)
     - Covers: inputs and their value.
     - Details: stationary features, rolling statistics, and lags. MDI is biased toward high-cardinality features. MDA (permutation) and SHAP are more reliable.
     - Pitfall: selecting features using the test set.
     - Build: importance computed out of sample and checked for stability across folds.

363. Hyperparameter optimization and its overfitting danger
     - Covers: tuning.
     - Details: nested validation, limited search budget, and reporting the number of trials. More tuning raises selection bias.
     - Pitfall: extensive search on one validation set.
     - Build: a tuning log and deflated performance estimate.

364. Class imbalance and probability calibration
     - Covers: skewed targets and probabilities.
     - Details: rare events need weighting or resampling, and predicted probabilities should be calibrated (Platt, isotonic) before sizing bets.
     - Pitfall: using uncalibrated scores as probabilities.
     - Build: reliability diagram before and after calibration.

365. Concept drift, model decay, retraining policy
     - Covers: model aging.
     - Details: monitor input distribution and performance, and retrain on schedule or on triggers.
     - Pitfall: retraining so often that you chase noise, or so rarely that the model decays.
     - Build: drift monitors and a retraining experiment comparing schedules.

366. Online and incremental learning
     - Covers: continuous updates.
     - Details: update parameters as new data arrive, using forgetting factors or windowed learners.
     - Pitfall: instability and catastrophic forgetting.
     - Build: online learner compared with periodic retraining.

367. Explainability and model governance
     - Covers: understanding and controlling models.
     - Details: document data, assumptions, validation, limitations, and approvals. Use SHAP or partial dependence for explanations.
     - Pitfall: explanations that are plausible but not faithful.
     - Build: a model card for each production model.

368. MLOps (feature stores, model registry, monitoring, reproducibility)
     - Covers: production ML processes.
     - Details: version data, code, features, and models. Ensure the same feature code runs in training and in production.
     - Pitfall: training-serving skew.
     - Build: a pipeline that reproduces any past model from tagged inputs.

## 8.2 Deep learning

369. Feed-forward networks and regularization
     - Covers: basic neural networks.
     - Details: use weight decay, dropout, early stopping, and normalization. Small networks are often enough.
     - Pitfall: large networks memorizing noise.
     - Build: compare a small network with a linear baseline.

370. RNN, LSTM, GRU for sequences
     - Covers: sequence models.
     - Details: gating helps with long dependencies. Window length, scaling, and stateful versus stateless training matter.
     - Pitfall: normalizing with statistics that include test data.
     - Build: an LSTM with expanding-window normalization.

371. Temporal CNNs and WaveNet-style models
     - Covers: convolutional sequence models.
     - Details: dilated causal convolutions capture long context efficiently.
     - Pitfall: non-causal padding that leaks the future.
     - Build: a causal-convolution model with leakage test.

372. Transformers and attention for time series
     - Covers: attention-based models.
     - Details: handle long contexts and multiple inputs. Positional encodings need care for irregular time.
     - Pitfall: overparameterization on short financial histories.
     - Build: a small transformer benchmark against simple baselines.

373. Temporal Fusion Transformer, N-BEATS, PatchTST
     - Covers: specialized forecasting architectures.
     - Details: TFT handles static and known-future inputs with interpretability. N-BEATS is a pure forecasting stack. PatchTST uses patches of time steps.
     - Pitfall: published benchmarks on low-noise data that do not transfer to returns.
     - Build: evaluate on your target with proper walk-forward splits.

374. Deep learning on limit order books (DeepLOB)
     - Covers: models on order-book snapshots.
     - Details: CNN plus LSTM on multi-level book features predicting short-term mid-price moves.
     - Pitfall: predictions too small to cover spread and fees.
     - Build: profitability test after realistic costs and latency.

375. Graph neural networks for asset relationships
     - Covers: models on relational structure.
     - Details: nodes are assets, edges from correlation, supply chain, or sector links.
     - Pitfall: unstable graph construction.
     - Build: graph built point-in-time and a comparison with non-graph features.

376. Generative models (GANs, VAEs, diffusion) for synthetic data
     - Covers: data generation.
     - Details: generate scenarios for stress or augmentation. Check that stylized facts (fat tails, volatility clustering) are preserved.
     - Pitfall: synthetic data that looks realistic but lacks true dependence structure.
     - Build: stylized-fact tests on generated series.

377. Autoencoders for anomaly detection and denoising
     - Covers: reconstruction-based methods.
     - Details: high reconstruction error flags unusual states or data errors.
     - Pitfall: threshold chosen after seeing events.
     - Build: anomaly detector for data-quality monitoring.

378. Foundation and pretrained time-series models
     - Covers: large pretrained forecasters.
     - Details: zero-shot and fine-tuned use. Check for overlap between pretraining data and your test period.
     - Pitfall: test-period leakage through pretraining data.
     - Build: evaluate zero-shot versus fine-tuned versus baseline on a held-out period.

379. Uncertainty estimation (MC dropout, ensembles, conformal prediction)
     - Covers: knowing when the model is unsure.
     - Details: ensembles and conformal intervals give calibrated uncertainty. Use it to scale position size.
     - Pitfall: overconfident uncertainty estimates.
     - Build: coverage test of predicted intervals.

380. Training under low signal-to-noise ratio
     - Covers: financial-data difficulty.
     - Details: small signals, heavy tails, and non-stationarity. Use robust losses, heavy regularization, and ensembling.
     - Pitfall: assuming accuracy benchmarks from other fields apply.
     - Build: a simulation with a known weak signal to test whether your pipeline can recover it.

## 8.3 Reinforcement learning

381. MDP formulation for trading (state, action, reward design)
     - Covers: problem definition.
     - Details: state includes features, position, and costs. Actions are target positions. Rewards link to risk-adjusted returns.
     - Pitfall: states that omit current position or costs.
     - Build: a written MDP specification before any training.

382. Q-learning and DQN
     - Covers: value-based methods.
     - Details: discrete actions, replay buffers, target networks.
     - Pitfall: instability and overestimation bias.
     - Build: DQN on a simulated mean-reverting series where the optimal policy is known.

383. Policy gradient, A2C, PPO, SAC, DDPG, TD3
     - Covers: policy-based methods.
     - Details: PPO is a common stable choice. SAC, DDPG, and TD3 handle continuous actions.
     - Pitfall: seed sensitivity and unreproducible results.
     - Build: multiple seeds and report the distribution of results.

384. Reward shaping (risk-adjusted, drawdown-penalized, cost-aware)
     - Covers: reward design.
     - Details: include transaction costs and risk penalties. Poor reward design yields exploitative behavior.
     - Pitfall: rewards that encourage excessive leverage or hidden risk.
     - Build: ablation across reward functions.

385. Trading environment simulation (Gym-style, realistic fills)
     - Covers: training environment.
     - Details: model spread, fees, slippage, latency, and market impact.
     - Pitfall: simulators with optimistic fills that the agent exploits.
     - Build: environment with realistic frictions and unit tests.

386. RL for optimal execution
     - Covers: learning execution schedules.
     - Details: state includes remaining quantity and time. Benchmark against TWAP and Almgren-Chriss.
     - Pitfall: gains that vanish with realistic impact.
     - Build: comparison against standard execution benchmarks.

387. RL for market making
     - Covers: learning quoting policies.
     - Details: state includes inventory and book features, and rewards penalize inventory risk.
     - Pitfall: simulators that ignore adverse selection.
     - Build: market-making agent against an event-driven simulator.

388. RL for portfolio allocation and dynamic hedging
     - Covers: sequential allocation.
     - Details: actions are weights or hedge ratios. Needs constraints and turnover penalties.
     - Pitfall: unstable weights and unrealistic rebalancing.
     - Build: RL allocation versus a simple volatility-target benchmark.

389. Multi-agent RL and market simulation
     - Covers: interacting agents.
     - Details: agents learn in a shared market, which allows studying impact and equilibrium.
     - Pitfall: simulated markets that lack real participant diversity.
     - Build: a simple multi-agent market with heterogeneous agents.

390. Sim-to-real gap and non-stationarity
     - Covers: transfer to live.
     - Details: simulated dynamics differ from real ones, and real markets change over time.
     - Pitfall: deploying a policy tuned to simulator quirks.
     - Build: stress the policy with perturbed simulator parameters.

391. Offline RL and safe/constrained RL
     - Covers: learning from logged data and under constraints.
     - Details: offline RL avoids online exploration risk. Constraints encode risk limits.
     - Pitfall: distribution shift between logged data and the learned policy.
     - Build: constrained policy with explicit drawdown and position limits.

## 8.4 Generative AI and LLM agents

392. LLMs for financial text understanding
     - Covers: text analysis with language models.
     - Details: extraction, classification, summarization, and scoring of filings, news, and calls.
     - Pitfall: unstable outputs across model versions.
     - Build: a fixed prompt and model version with a labeled evaluation set.

393. Retrieval-augmented generation over filings and research
     - Covers: grounded question answering.
     - Details: retrieve relevant passages, then answer with citations. Index by company and date.
     - Pitfall: retrieving documents dated after the decision date.
     - Build: a date-filtered retrieval pipeline with citation checks.

394. LLM agents for research, strategy ideation, and code generation
     - Covers: automation of research tasks.
     - Details: agents can draft hypotheses and code, but outputs need review and tests.
     - Pitfall: confident but wrong code or invented statistics.
     - Build: agent output gated by unit tests and human review.

395. Agentic trading workflows with guardrails and human approval
     - Covers: autonomous or semi-autonomous operations.
     - Details: limit tool permissions, set spending and position caps, require approval for risky actions, and log everything.
     - Pitfall: an agent with direct unrestricted order access.
     - Build: agent actions routed through the risk layer with approvals.

396. Prompt design, evaluation, hallucination control
     - Covers: output quality.
     - Details: structured outputs, test sets, and checks against source documents.
     - Pitfall: evaluating on a few hand-picked examples.
     - Build: an evaluation suite measuring accuracy and refusal behavior.

397. Backtesting LLM signals without look-ahead (knowledge-cutoff leakage)
     - Covers: historical leakage in language models.
     - Details: models trained after your test period may know outcomes. Use models whose training cutoff precedes the test period, or test only post-cutoff data.
     - Pitfall: impressive backtests on events the model memorized.
     - Build: test on data after the model's cutoff and compare with earlier periods.

398. Cost, latency, and reproducibility of LLM pipelines
     - Covers: operational concerns.
     - Details: per-call cost, response time, rate limits, nondeterminism, and model deprecations.
     - Pitfall: a signal that is unusable at production speed or cost.
     - Build: cost and latency budget per signal and cached, versioned outputs.
