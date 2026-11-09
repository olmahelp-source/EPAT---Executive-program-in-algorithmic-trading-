# Part 14. Costs, Taxes, and Accounting: Micro Details (topics 631 to 640)

Each topic lists what it covers, the key details, the common pitfall, and something concrete to build or test.

## 14.1 Costs, taxes, and accounting

631. Funding, financing, and margin costs
     - Covers: cost of holding positions.
     - Details: interest on borrowed cash, financing in swaps and futures (embedded in the basis), and opportunity cost of margin posted.
     - Pitfall: ignoring financing on leveraged or overnight positions.
     - Build: a daily financing-cost calculation by position.

632. Commission structures, brokerage tiers, and exchange fees
     - Covers: explicit trading costs.
     - Details: per-share, per-contract, or percentage commissions, with volume tiers and minimums. Add exchange, clearing, and regulatory fees.
     - Pitfall: using a flat commission that misses minimums and tiers.
     - Build: a fee schedule table and a cost calculator tested against actual statements.

633. Maker-taker rebates and fee-tier optimization
     - Covers: venue incentives.
     - Details: some venues pay rebates for adding liquidity and charge for removing it. Tiers depend on monthly volume.
     - Pitfall: chasing rebates through passive orders that suffer adverse selection.
     - Build: net-of-rebate cost analysis by venue and order type.

634. Taxes (transaction taxes such as STT, capital gains, GST, stamp duty)
     - Covers: tax costs.
     - Details: transaction taxes apply per trade, capital gains depend on holding period and instrument type, and indirect taxes apply to fees.
     - Pitfall: pre-tax backtests for high-turnover strategies.
     - Build: tax-aware P&L with rates configurable per jurisdiction and instrument.

635. Borrow fees and short-rebate economics
     - Covers: cost of shorting.
     - Details: borrow fee varies by availability, you may receive a rebate on cash collateral, and recalls can force covering.
     - Pitfall: assuming shorts are free to hold.
     - Build: borrow-fee accrual and recall handling.

636. Total cost of ownership (data, infrastructure, staff, and compliance)
     - Covers: full running cost.
     - Details: data feeds, cloud or colocation, software licenses, staff time, audit, legal, and insurance.
     - Pitfall: judging profitability before overhead.
     - Build: monthly cost sheet and break-even capital.

637. Multi-currency accounting, FX conversion, and base-currency reporting
     - Covers: handling several currencies.
     - Details: P&L in local currency converted to base at appropriate rates, with FX P&L separated from price P&L.
     - Pitfall: converting at one rate for the entire period.
     - Build: multi-currency ledger with FX P&L split.

638. Cash management, interest accrual, and margin interest
     - Covers: cash flows.
     - Details: interest on cash balances and debit balances, and sweeps between accounts.
     - Pitfall: idle cash with no yield or unmonitored debit balances.
     - Build: cash ledger with accrual reconciliation.

639. Settlement cycles (T+1/T+2), settlement fails, custody, and clearing
     - Covers: post-trade lifecycle.
     - Details: trade date versus settlement date, buy-in rules for fails, and the role of custodians and clearing houses.
     - Pitfall: using unsettled cash as available.
     - Build: settled and unsettled position and cash views.

640. Time-weighted vs. money-weighted returns, log vs. simple returns, annualization conventions
     - Covers: return conventions.
     - Details: TWR removes flow effects, MWR (IRR) reflects flow timing. Annualization with 252 or 365 depending on context.
     - Pitfall: mixing conventions when comparing strategies.
     - Build: a conventions reference and test cases.
