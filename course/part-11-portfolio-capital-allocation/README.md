# Part 11 Course Material: Portfolio Construction and Capital Allocation

Worked examples, formulas, and runnable code for topics 462 to 496 of the master list.

| Lesson | Topics | Code |
|---|---|---|
| [11.1 Portfolio construction and optimization](11.1-portfolio-construction-and-optimization.md) | 462 to 475 | `code/ex_11_1_construction.py` |
| [11.2 and 11.3 Position keeping and risk-model concepts](11.2-11.3-position-keeping-and-risk-model-concepts.md) | 476 to 484 | `code/ex_11_2_book_and_risk_models.py` |
| [11.4 Position sizing and fund allocation](11.4-position-sizing-and-fund-allocation.md) | 485 to 496 | `code/ex_11_3_sizing.py` |

## Running the code

Requires Python 3.10+ and numpy only.

```bash
cd course/part-11-portfolio-capital-allocation/code
python3 run_all.py                       # runs everything and checks the key numbers (about 1 minute)
python3 ex_11_3_sizing.py                # prints every example of section 11.4 (about 5 seconds)
```

Each topic is one function named `tNNN_...` that returns a dictionary of results. Random seeds are fixed, so the numbers in the lessons reproduce exactly. `run_all.py` asserts the main figures.

## One-page formula sheet

| Idea | Formula |
|---|---|
| Mean-variance weights | `w = (1/lambda) S^-1 (mu - gamma 1)` |
| Black-Litterman posterior | `[(tau S)^-1 + P' Omega^-1 P]^-1 [(tau S)^-1 pi + P' Omega^-1 q]` |
| Risk contribution | `RC_i = w_i (S w)_i / sigma_p` |
| Diversification ratio | `(w' sigma) / sqrt(w' S w)` |
| No-trade band (one asset) | `c / (lambda sigma^2)` |
| Minimum-variance hedge ratio | `Cov(spot, hedge) / Var(hedge)` |
| Active share, tracking error | `0.5 sum|w - w_b|`, `sqrt(a' S a)` |
| Fixed fractional size | `equity x risk / (entry - stop)` |
| Kelly (binary, continuous) | `(p b - q) / b`, `mu / sigma^2` |
| Growth rate at leverage f | `mu f - 0.5 sigma^2 f^2` |
| Volatility-target leverage | `target_vol / forecast_vol` |
| Margin-call drop | `(1/L - m) / (1 - m)` |
| Performance fee with high-water mark | `fee_rate x max(0, gross - HWM)` |

## Suggested order
Start with 485 to 488 (how big to trade), then 462 to 466 (how to combine positions), then 476 to 477 (keeping the books right), then the rest by need.
