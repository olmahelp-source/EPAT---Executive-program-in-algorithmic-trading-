# trading_platform (work in progress)

A reusable library (`tradelib`) and a trading platform system (`tradeplatform`) built from the master topic list in `../TRADING_PLATFORM_MASTER_TOPICS.md`.

## Status

This is an unfinished draft. Nothing here has been run or tested yet.

Written so far (all under `src/tradelib/`):
- `core/types.py`: side, order, bar, and fill types
- `marketdata/`: bar builder, data cleaning and split adjustment, synthetic data, CSV reading and writing
- `orderbook.py`: limit order book with price-time priority
- `oms/oms.py`: order state machine, client order IDs, working-exposure accounting
- `risk/`: pre-trade gate, kill switch, VaR and expected-shortfall measures
- `portfolio/`: average-cost ledger, position sizing

Still to do: optimizers, execution (costs, algos, paper broker), strategies, analytics, the `tradeplatform` engine, CLI, tests, and documentation.

## Planned design
One event-driven engine runs the same strategy code in backtest and paper trading. A strategy emits target weights. The portfolio manager turns them into orders. Each order passes the risk gate, goes through the OMS, and is filled by a broker adapter. Every event is written to an append-only log so state can be rebuilt after a restart.
