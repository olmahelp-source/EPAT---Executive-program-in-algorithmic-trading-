# Part 2. Quantitative Foundations: Micro Details (topics 36 to 78)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 2.1 Statistics and probability

36. Descriptive statistics of returns (skewness, kurtosis, fat tails)
    - Covers: mean, variance, skew, excess kurtosis, quantiles.
    - Details: financial returns have excess kurtosis (fat tails) and often negative skew. Use robust measures (median, MAD) next to moments.
    - Pitfall: using mean and standard deviation as if returns were normal.
    - Build: a report comparing your series with a fitted normal (QQ plot, Jarque-Bera).

37. Probability distributions (normal, Student-t, log-normal, stable, mixtures)
    - Covers: candidate return models.
    - Details: Student-t captures fat tails with a degrees-of-freedom parameter. Mixtures model regimes. Prices are log-normal under the basic model.
    - Pitfall: picking a distribution by convenience and not by fit to tails.
    - Build: fit several distributions and compare AIC/BIC and tail fit.

38. Hypothesis testing and p-values in strategy validation
    - Covers: testing whether a result is distinguishable from chance.
    - Details: null hypothesis is often "mean return = 0". The t-stat = mean / (std / sqrt(n)). A p-value is not the probability the strategy works.
    - Pitfall: ignoring autocorrelation, which inflates the t-stat.
    - Build: a t-test with Newey-West standard errors on your strategy returns.

39. Multiple-testing correction (Bonferroni, Benjamini-Hochberg)
    - Covers: adjusting for many trials.
    - Details: Bonferroni divides the threshold by the number of tests. Benjamini-Hochberg controls false-discovery rate and is less conservative.
    - Pitfall: testing hundreds of variants and reporting only the best.
    - Build: log every trial, then apply a correction to the final result.

40. Deflated Sharpe ratio and probability of backtest overfitting (also as a reporting metric)
    - Covers: Sharpe adjusted for selection and non-normality.
    - Details: deflation uses the number of trials, track-record length, skew, and kurtosis. PBO uses combinatorially symmetric cross-validation.
    - Pitfall: reporting an unadjusted Sharpe after a large search.
    - Build: compute the deflated Sharpe for your best backtest with the real trial count.

41. Bootstrap, jackknife, and resampling
    - Covers: empirical sampling distributions.
    - Details: block bootstrap preserves serial dependence. Stationary bootstrap uses random block lengths.
    - Pitfall: an i.i.d. bootstrap on autocorrelated returns understates risk.
    - Build: a block-bootstrap confidence interval for Sharpe and max drawdown.

42. Bayesian inference and belief updating
    - Covers: priors, likelihoods, posteriors.
    - Details: shrinkage toward a prior reduces noise in small samples. Conjugate priors give closed-form updates.
    - Pitfall: strong priors that hide what the data say.
    - Build: a Bayesian estimate of a strategy's mean return with credible intervals.

43. Maximum likelihood and method-of-moments estimation
    - Covers: parameter estimation.
    - Details: MLE maximizes the likelihood and has good asymptotics. Moments matching is simple but less efficient.
    - Pitfall: non-converging or local-optimum fits for GARCH-type models.
    - Build: fit a Student-t by MLE and check the fit diagnostics.

44. Confidence intervals for performance metrics
    - Covers: uncertainty around Sharpe, drawdown, hit rate.
    - Details: asymptotic Sharpe standard error is roughly sqrt((1 + 0.5 SR^2) / n) under i.i.d.; adjust for skew and kurtosis.
    - Pitfall: presenting a point estimate with no interval.
    - Build: add intervals to every metric in your tear sheet.

45. Autocorrelation, partial autocorrelation, Ljung-Box test
    - Covers: serial dependence in returns and residuals.
    - Details: ACF shows total lag correlation, PACF the direct effect. Ljung-Box tests joint significance of lags.
    - Pitfall: finding "predictability" caused by bid-ask bounce or stale prices.
    - Build: ACF/PACF plots on returns and on squared returns.

46. Stationarity tests (ADF, KPSS, Phillips-Perron)
    - Covers: whether a series has a stable mean and variance.
    - Details: ADF null is a unit root, KPSS null is stationarity, so use both. Prices are generally non-stationary, returns usually stationary.
    - Pitfall: modeling non-stationary prices with regression and getting spurious results.
    - Build: run ADF and KPSS on prices, returns, and spreads.

47. Cointegration (Engle-Granger, Johansen)
    - Covers: long-run relationships between non-stationary series.
    - Details: Engle-Granger is a two-step residual test for pairs. Johansen handles multiple series and gives several relationships.
    - Pitfall: a relationship that breaks out of sample, or is a sample artifact.
    - Build: test pairs in rolling windows to see how stable cointegration is.

48. Regression (OLS, ridge, lasso, elastic net, robust)
    - Covers: linear modeling and regularization.
    - Details: OLS assumes homoscedastic, uncorrelated errors. Ridge shrinks coefficients, lasso zeroes some, robust methods reduce outlier influence.
    - Pitfall: multicollinearity makes coefficients unstable.
    - Build: compare OLS, ridge, and lasso on the same factor-regression problem.

49. Heteroscedasticity and Newey-West correction
    - Covers: non-constant variance and correlated errors.
    - Details: Newey-West (HAC) standard errors correct inference without changing coefficients.
    - Pitfall: trusting default OLS standard errors on financial data.
    - Build: report both default and HAC t-stats.

50. Time-series models (AR, MA, ARIMA, SARIMA, VAR, VECM)
    - Covers: forecasting from past values.
    - Details: choose order via AIC/BIC and residual tests. VAR models several series jointly. VECM combines VAR with cointegration.
    - Pitfall: overfitting orders and forecasting noise.
    - Build: rolling out-of-sample forecast comparison against a naive baseline.

51. Volatility models (EWMA, GARCH, EGARCH, GJR, realized vol, stochastic vol)
    - Covers: forecasting variance.
    - Details: EWMA: sigma_t^2 = lambda sigma_{t-1}^2 + (1-lambda) r_{t-1}^2. GARCH adds mean reversion. EGARCH and GJR capture the leverage effect. Realized vol uses intraday data.
    - Pitfall: using in-sample fit to judge a volatility forecast.
    - Build: compare EWMA, GARCH, and realized-vol forecasts with a QLIKE loss.

52. Regime detection (HMM, Markov switching, change-point detection)
    - Covers: identifying distinct market states.
    - Details: HMMs infer hidden states from returns. Filtered probabilities use only past data, smoothed ones use all data.
    - Pitfall: look-ahead from using smoothed states in a backtest.
    - Build: a two-state HMM with filtered (not smoothed) probabilities only.

53. Kalman filter and state-space models
    - Covers: recursive estimation of hidden states.
    - Details: used for dynamic hedge ratios, time-varying betas, and trend estimation. Needs noise-variance settings.
    - Pitfall: poorly set noise variances produce lag or noise.
    - Build: a Kalman-filter hedge ratio for a pair versus a rolling regression.

54. Extreme value theory
    - Covers: modeling tails directly.
    - Details: peaks-over-threshold with a generalized Pareto distribution. Block maxima with GEV.
    - Pitfall: choosing a threshold arbitrarily.
    - Build: tail-risk estimates (VaR, ES) from a fitted GPD.

55. Copulas and tail dependence
    - Covers: dependence structure separate from marginals.
    - Details: Gaussian copulas have no tail dependence, t and Clayton copulas do. Assets move together more in crashes.
    - Pitfall: assuming correlation stays constant in stress.
    - Build: fit copulas to two assets and compare joint-tail probabilities.

56. Survival analysis and hazard models
    - Covers: time-to-event modeling.
    - Details: applies to default, trade duration, strategy lifetime, and time to stop-out. Censoring handles open events.
    - Pitfall: ignoring censored observations.
    - Build: a Kaplan-Meier curve of how long trades remain open.

## 2.2 Advanced statistics and validation

57. White's Reality Check, Hansen's SPA test, and data-snooping controls
    - Covers: testing the best of many rules.
    - Details: bootstraps the distribution of the best performance under the null of no skill. SPA improves power.
    - Pitfall: ignoring the full search space.
    - Build: apply the test to a family of parameter variants of one strategy.

58. Sharpe ratio under autocorrelation (Lo adjustment) and minimum track record length
    - Covers: annualizing and testing Sharpe correctly.
    - Details: with autocorrelation, annual Sharpe is not monthly Sharpe x sqrt(12). Minimum track record length shows how long a record must be for significance.
    - Pitfall: overstated Sharpe from smoothed or illiquid returns.
    - Build: compute Lo-adjusted Sharpe and the minimum track record length for your strategy.

59. Ergodicity and why ensemble averages mislead single-account outcomes
    - Covers: time average versus ensemble average.
    - Details: a bet with positive expected value can still lead to ruin along a single path if sized too large. Growth rate is the geometric mean.
    - Pitfall: optimizing arithmetic expectation instead of long-run growth.
    - Build: simulate repeated bets and compare ensemble and time averages.

60. Causal inference (Granger causality, instrumental variables, double ML) vs. correlation
    - Covers: separating cause from association.
    - Details: Granger tests predictive precedence, not true causation. Instruments and double ML address confounders.
    - Pitfall: confusing lead-lag correlation with a tradable cause.
    - Build: a Granger test with lag selection and a stability check across periods.

61. Quantile regression and non-parametric methods
    - Covers: modeling conditional quantiles and distribution-free methods.
    - Details: quantile regression gives tail behavior given a signal. Kernel and rank methods avoid distribution assumptions.
    - Pitfall: noisy extreme-quantile estimates from small samples.
    - Build: estimate how a signal shifts the 5th, 50th, and 95th return quantiles.

62. Variance ratio test and Hurst exponent
    - Covers: random-walk versus trending versus mean-reverting behavior.
    - Details: variance ratio VR(q) = 1 for a random walk. Hurst H = 0.5 random, above 0.5 trending, below 0.5 mean-reverting.
    - Pitfall: noisy Hurst estimates on short samples.
    - Build: variance-ratio tests across several horizons and instruments.

63. Ornstein-Uhlenbeck calibration and half-life of mean reversion
    - Covers: modeling spreads that revert.
    - Details: dX = theta(mu - X)dt + sigma dW. Half-life = ln(2) / theta. Estimate from an AR(1) regression of the spread.
    - Pitfall: trading a spread whose half-life exceeds your holding capacity.
    - Build: a half-life estimator with a stability check over rolling windows.

64. Filters and signal processing (low-pass, Hodrick-Prescott, Savitzky-Golay)
    - Covers: smoothing and trend extraction.
    - Details: two-sided filters use future data. Causal filters trade lag for smoothness.
    - Pitfall: using a two-sided filter in a backtest, which leaks the future.
    - Build: compare causal and two-sided filters and show the look-ahead gap.

65. Effective sample size and overlapping-observation problems
    - Covers: how many independent observations you really have.
    - Details: overlapping multi-day returns are strongly autocorrelated, so the effective sample is much smaller than the row count.
    - Pitfall: significance inflated by overlapping labels.
    - Build: compute effective sample size and use non-overlapping or weighted samples.

## 2.3 Mathematics

66. Linear algebra (eigen decomposition, SVD, PCA)
    - Covers: matrix tools behind risk and factor models.
    - Details: eigenvectors of the covariance matrix are principal components. SVD works on non-square data. Condition number shows numerical instability.
    - Pitfall: inverting a near-singular covariance matrix.
    - Build: PCA on a universe and a scree plot of explained variance.

67. Covariance estimation (Ledoit-Wolf shrinkage, random matrix denoising)
    - Covers: stable covariance matrices.
    - Details: with N assets and T observations, sample covariance is noisy when N/T is not small. Shrinkage blends sample and structured targets. RMT removes noise eigenvalues.
    - Pitfall: feeding a raw sample covariance into an optimizer.
    - Build: compare out-of-sample portfolio variance under sample, shrunk, and denoised covariance.

68. Calculus and numerical differentiation
    - Covers: derivatives for sensitivities and optimization.
    - Details: finite differences have a step-size trade-off. Automatic differentiation avoids it.
    - Pitfall: step sizes too small cause round-off error, too big cause truncation error.
    - Build: finite-difference Greeks checked against analytic Greeks.

69. Convex and non-convex optimization (quadratic, conic, gradient-based, evolutionary)
    - Covers: solving allocation and calibration problems.
    - Details: convex problems have global optima. Constraints like cardinality make the problem non-convex.
    - Pitfall: trusting a local optimum or over-tuned solver settings.
    - Build: a mean-variance optimizer in a convex solver with turnover constraints.

70. Stochastic calculus (Brownian motion, Ito's lemma)
    - Covers: continuous-time price models.
    - Details: dS = mu S dt + sigma S dW. Ito's lemma gives d ln S = (mu - sigma^2/2)dt + sigma dW.
    - Pitfall: forgetting the Ito correction term (volatility drag).
    - Build: simulate geometric Brownian motion and verify the drift correction.

71. Stochastic differential equations and simulation
    - Covers: discretizing and simulating SDEs.
    - Details: Euler-Maruyama is simple, Milstein has higher order. Choose step size for accuracy.
    - Pitfall: discretization bias in mean-reverting or rate models.
    - Build: simulate an OU process and check its moments against theory.

72. Numerical methods (finite differences, trees, Monte Carlo, quasi-Monte Carlo)
    - Covers: pricing and risk computation.
    - Details: Monte Carlo error falls as 1/sqrt(N). Variance reduction (antithetic, control variates) and quasi-random sequences speed convergence.
    - Pitfall: too few paths and no error estimate.
    - Build: price a European option by Monte Carlo and compare with Black-Scholes.

73. Information theory (entropy, mutual information)
    - Covers: measuring dependence and information content.
    - Details: mutual information captures non-linear dependence. Estimation needs binning or kernel choices.
    - Pitfall: unstable estimates on small samples.
    - Build: mutual information between a feature and future returns with a permutation test.

74. Fourier and wavelet analysis, spectral methods
    - Covers: frequency-domain analysis.
    - Details: Fourier assumes stationarity. Wavelets localize in time and frequency.
    - Pitfall: finding "cycles" in noise.
    - Build: a spectrum of returns versus a surrogate random series.

75. Game theory
    - Covers: strategic interaction among participants.
    - Details: Nash equilibria, auctions, and signaling explain market-maker and informed-trader behavior.
    - Pitfall: assuming other participants are passive.
    - Build: a simple market-maker versus informed-trader game.

76. Optimal control and dynamic programming
    - Covers: sequential decisions under uncertainty.
    - Details: Bellman equation gives optimal policies. Used in execution, inventory management, and portfolio problems.
    - Pitfall: the curse of dimensionality as the state grows.
    - Build: a dynamic-programming solution for a small inventory problem.

77. Graph theory and network analysis of correlations
    - Covers: representing asset relationships as graphs.
    - Details: minimum spanning trees and clustering from a correlation-distance metric d = sqrt(0.5 (1 - rho)).
    - Pitfall: unstable graphs from noisy correlations.
    - Build: an MST of your universe and its change across regimes.

78. Fractional differentiation and memory-preserving stationarity
    - Covers: making series stationary while keeping information.
    - Details: differencing order d between 0 and 1 retains long memory. Choose the smallest d that passes a stationarity test.
    - Pitfall: integer differencing discards useful level information.
    - Build: find the minimum d for your price series that passes ADF.
