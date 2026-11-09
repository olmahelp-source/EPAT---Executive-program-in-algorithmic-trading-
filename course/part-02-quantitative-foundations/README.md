# Part 2 Course Material: Quantitative Foundations

Worked examples, formulas, and runnable code for topics 36 to 78 of the master list.

| Lesson | Topics | Code |
|---|---|---|
| [2.1 Statistics and probability](2.1-statistics-and-probability.md) | 36 to 56 | `code/ex_2_1_statistics.py` |
| [2.2 Advanced statistics and validation](2.2-advanced-statistics-and-validation.md) | 57 to 65 | `code/ex_2_2_advanced.py` |
| [2.3 Mathematics](2.3-mathematics.md) | 66 to 78 | `code/ex_2_3_mathematics.py` |

## Running the code

Requires Python 3.10+ and numpy only.

```bash
cd course/part-02-quantitative-foundations/code
python3 run_all.py                 # runs everything and checks the key numbers (about 5 seconds)
python3 ex_2_1_statistics.py       # prints every example of section 2.1
```

Each topic is one function named `tNN_...` that returns a dictionary of results. Random seeds are fixed, so the numbers in the lessons reproduce exactly. `run_all.py` asserts the main figures, so a change to the code that breaks a lesson is caught.

## How each lesson is laid out
1. **Formula:** the definition or algorithm in plain text.
2. **Worked example:** concrete inputs and the numbers the code produces.
3. **Code:** the function that reproduces it.
4. **Watch out:** the typical mistake.

## One-page formula sheet

| Idea | Formula |
|---|---|
| t-statistic of a mean | `t = mean / (s / sqrt(n))` |
| Annualized Sharpe | `SR_ann = mean/std * sqrt(252)`; years needed for t = 2: `(2 / SR_ann)^2` |
| Sharpe standard error | `sqrt((1 + 0.5 SR^2) / n)`, adjusted: `sqrt((1 - skew SR + (kurt-1)/4 SR^2) / n)` |
| Bonferroni | reject if `p < alpha / m` |
| Deflated Sharpe | `PSR` evaluated at `SR* = E[max SR over N trials]` |
| EWMA variance | `s2_t = lambda s2_{t-1} + (1 - lambda) r_{t-1}^2` |
| GARCH(1,1) long-run variance | `omega / (1 - alpha - beta)` |
| OU half-life | `ln 2 / theta`, with `theta = -ln(1 + b)` from `dX = a + b X_{t-1}` |
| Variance ratio | `VR(q) = Var(q-period) / (q Var(1-period))` |
| Effective sample size | `n / (1 + 2 sum (1 - k/L) rho_k)` |
| Ito log drift | `mu - sigma^2 / 2` |
| Min-variance weights | `S^-1 1 / (1' S^-1 1)` |
| Risk contribution | `RC_i = w_i (S w)_i / sigma_p` |
| Correlation distance | `sqrt(0.5 (1 - rho))` |
| Fractional-difference weights | `w_k = -w_{k-1} (d - k + 1) / k` |

## Suggested order
Read 2.1 topics 36 to 44 first (the language of evidence), then 57 to 59 (why backtests mislead), then 66 to 70 (the math behind portfolios and options). The rest can follow the needs of the strategy you are building.
