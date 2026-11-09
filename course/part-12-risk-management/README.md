# Part 12 Course Material: Risk Management

Worked examples, formulas, and runnable code for topics 497 to 519 of the master list.

| Lesson | Topics | Code |
|---|---|---|
| [12.1 and 12.2 Controls, risk measures, stress testing, and exposures](12.1-12.2-controls-and-risk-measures.md) | 497 to 514 | `code/ex_12_1_controls_and_measures.py` |
| [12.3 Margin, leverage, and funding risk](12.3-margin-leverage-and-funding-risk.md) | 515 to 519 | `code/ex_12_2_margin_funding.py` |

## Running the code

Requires Python 3.10+ and numpy only.

```bash
cd course/part-12-risk-management/code
python3 run_all.py                        # runs everything and checks the key numbers (about 3 seconds)
python3 ex_12_1_controls_and_measures.py  # prints every example of sections 12.1 and 12.2
```

Each topic is one function named `tNNN_...` that returns a dictionary of results. Random seeds are fixed, so the numbers in the lessons reproduce exactly.

## One-page formula sheet

| Idea | Formula |
|---|---|
| Parametric VaR | `z x sigma` (z = 2.326 at 99%) |
| Expected shortfall (normal) | `sigma x phi(z) / (1 - a)` |
| Kupiec test | `-2 ln[(1-p)^(T-x) p^x] + 2 ln[(1-x/T)^(T-x) (x/T)^x]`, chi-square(1) |
| Reverse stress | `x* = -L S g / (g' S g)`, distance `L / sqrt(g' S g)` |
| Equal-correlation portfolio | `sigma^2 [1/N + (1 - 1/N) rho]` |
| Days to liquidate | `position / (participation x ADV)` |
| Impact estimate | `c x sigma x sqrt(position / ADV)` |
| Risk contribution | `w_i (S w)_i / sigma_p` |
| Effective number of bets | `exp(-sum p_i ln p_i)` over principal-portfolio risk shares |
| Delta-gamma-vega P&L | `delta dS + 0.5 gamma dS^2 + vega d sigma` |
| Gap position cap | `risk budget / quantile of overnight loss` |
| Margin call (long, leverage L, maintenance m) | `price drop >= (1/L - m) / (1 - m)` |
| Cross margin | `z x sqrt(sum of squared risks + 2 rho products)` |
| LVaR | `z sigma sqrt(sum of squared daily exposures) + spread + impact` |

## Suggested order
Start with 497 and 499 (stopping bad orders and stopping everything), then 500 to 503 (measuring risk and its limits), then 515 and 519 (capital and liquidity), and the rest by need.
