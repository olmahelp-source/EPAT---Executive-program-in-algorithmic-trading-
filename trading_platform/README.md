# algoplatform: a modular algorithmic trading platform in Python

One codebase for **research -> backtest -> paper -> live**. The same `TradingEngine` runs a backtest and a live session, so what you test is what you trade. Built from `../TRADING_PLATFORM_MASTER_TOPICS.md`.

Pure Python 3.10+ with `numpy` and `pandas`. No scipy: the statistical functions are implemented in `stats/special.py`.

```
pip install -e .                    # from this folder (optional: pip install -e ".[security]" for encrypted credentials)
python examples/run_demo.py         # full tour, ~15 s
python -m algoplatform backtest --strategy zscore_reversion --html report.html
python -m algoplatform optimize --strategy sma_crossover --method genetic
cd tests && python -m unittest discover -p "test_*.py"     # 200+ tests
```

## Web UI

```
PYTHONPATH=src python -m algoplatform.web --port 8080      # then open http://127.0.0.1:8080
```
Standard-library server plus a no-build single-page UI (`src/algoplatform/web/`). Tabs: **Backtest** (any built-in strategy, equity/drawdown charts, metrics, trades), **Strategy builder** (indicators and rules as a form, validated server-side), **Optimise** (random/genetic with plateau score), **Paper trading** (simulated broker on a synthetic feed: order ticket, positions, orders, risk meters, kill switch) and **Admin & audit** (audit log, role management).

- The first account created becomes the administrator; later sign-ups are traders. Raise roles in the Admin tab (a Risk Manager or Admin is needed to reset a tripped kill switch).
- Every call goes through `TradingPlatform`, so permissions are enforced server-side, not just hidden in the UI. Server text is rendered with `textContent` only, and responses carry CSP and no-sniff headers.
- **Localhost only.** There is no TLS and state is in memory. Do not expose it to a network without a TLS reverse proxy and your own auth in front.
- API: `POST /api/login|register`, `GET /api/me|strategies|session|audit|users`, `POST /api/backtest|optimize|session/open|step|order|cancel_all|killswitch|close|users/role` (see `web/server.py`).

## Architecture

```
            ┌──────────────┐   Signal(target weight)    ┌─────────────────────────────┐
 data ────► │  Strategy    │ ─────────────────────────► │ TradingEngine (app/engine)  │
 (store,    │ (SDK / rules)│                            │  sizing -> net targets      │
 feeds)     └──────────────┘                            └──────────────┬──────────────┘
                                                                       │ orders
                  ┌────────────────────────────────────────────────────▼───────────────┐
                  │ ExecutionService (orders/execution)                                │
                  │   OMS (state machine, idempotency) -> RiskManager gate -> Broker   │
                  └───────┬───────────────────────────────┬────────────────────┬───────┘
                          │ fills/events                  │ halt               │
                    ┌─────▼─────┐                  ┌──────▼──────┐      ┌──────▼──────┐
                    │ Portfolio │                  │ KillSwitch  │      │ BrokerGateway│ paper | your adapter
                    │ (ledger)  │                  │ + Monitor   │      │ (+ failover) │
                    └───────────┘                  └─────────────┘      └─────────────┘
```

`src/tradelib` and `src/tradeplatform` are an earlier untested draft, superseded by `algoplatform`.

Layers only depend downward; strategies never see orders or brokers, risk never knows about strategies, brokers only emit events.

## Module map

| Package | What it does | Key classes / functions |
|---|---|---|
| `core` | Shared contracts | typed exception tree (`retryable` flag), enums, `Order/Fill/Position/Signal/Bar`, `PlatformConfig` (validated), `EventBus`, `AuditLog`, `Registry` |
| `utils` | Reusable helpers | `retry`, `CircuitBreaker`, `RateLimiter`, `SimClock/SystemClock`, `TradingCalendar`, `IdGenerator`, validators |
| `users` | Users and broker accounts | scrypt passwords, lockout, signed tokens, RBAC (`Role`/`Permission`), `CredentialVault`, `BrokerAccountManager` |
| `brokers` | Venue connectivity | `BrokerGateway` ABC + registry, `PaperBroker` (bar-driven matching), `CostModel`, `ResilientGateway` (retry/breaker/failover), `RestBrokerBase` |
| `orders` | Order management | `OrderManager` (state machine, idempotent ids, duplicate/late fills, reconcile), `ExecutionService` |
| `risk` | Separate risk layer | pre-trade checks, `KillSwitch` (two-person reset), `RiskMonitor`, `RiskManager`, VaR/ES/Kupiec/stress |
| `portfolio` | Positions, sizing, allocation | `Portfolio` ledger, sizers (fixed-fractional, vol-target, risk-per-trade, Kelly, optimal-f), `FundAllocator`, optimisers (min-var, risk-parity, max-Sharpe, Black-Litterman) |
| `strategy` | Strategy SDK + creator | `Strategy` ABC, 6 built-ins, `StrategyBuilder` (JSON rules, no `eval`) |
| `data` | Market data | `MarketData` store/CSV, `clean_ohlcv`, split adjustment, synthetic generators |
| `backtest` | Event-driven backtester | `BacktestEngine`, `BacktestResult` |
| `optimize` | Parameter search | grid / random / genetic, `walk_forward`, plateau score |
| `analytics` | Measurement | metrics, drawdown periods, trade stats, tear sheet (text/JSON/HTML) |
| `stats` | Statistical methods | ADF, KPSS, Engle-Granger, Hurst, variance ratio, bootstrap, PSR/DSR, FDR, OLS+Newey-West |
| `quant` | Quantitative methods | indicators, Black-Scholes + Greeks + IV, GARCH/EWMA, Ledoit-Wolf, Kalman |
| `app` | Wiring | `TradingEngine`, `TradingPlatform` facade (permission-checked), CLI |

## Safety properties (each has tests)

- **No look-ahead.** Strategies read a causal `HistoryView`; a signal on bar *t* fills no earlier than the open of bar *t+1*. Altering future data leaves past results unchanged.
- **Deterministic.** Same inputs give identical results, independent of Python's hash seed.
- **Idempotent orders.** Reusing an `idempotency_key` returns the original order; duplicate fills are ignored; late fills after a cancel are recorded, not lost.
- **Fail closed.** A broken risk check rejects the order. A crashing strategy is contained, and repeated failures trip the kill switch.
- **Kill switch.** Trips on daily loss, drawdown, consecutive errors or stale data (or by hand). It cancels resting orders, flattens positions with reduce-only orders, blocks everything else, and resets only with a permitted user, a written reason and (optionally) a second approver.
- **Netting.** Opposing views from different strategies cancel internally before any order is sent.
- **Overfitting guards.** Walk-forward analysis, parameter-plateau score, deflated Sharpe ratio that accounts for the number of trials, a `min_trades` filter in objectives.

## Quick start

```python
from algoplatform.data import MarketData, synthetic
from algoplatform.backtest import BacktestEngine
from algoplatform.strategy import SMACrossover
from algoplatform.core import PlatformConfig

md = MarketData()
for sym, df in synthetic.universe(["AAA", "BBB"], n=750).items():
    md.add(sym, df)                      # or md.add_csv("AAA", "aaa.csv")  (date,open,high,low,close,volume)

result = BacktestEngine(md, PlatformConfig()).run(SMACrossover(md.symbols, fast=10, slow=50))
print(result.metrics()["sharpe"], result.trade_stats()["win_rate"])
```

### Define a strategy without code
```python
from algoplatform.strategy import StrategyBuilder, create_from_spec
spec = (StrategyBuilder("rsi_trend").param("lvl", 35)
        .indicator("rsi", "rsi", period=14).indicator("trend", "sma", period=100).indicator("atr", "atr", period=14)
        .long_entry(("rsi", "<", "$lvl"), ("close", ">", "trend")).long_exit(("rsi", ">", 60))
        .stop_atr("atr", 2.5).build())          # validated; JSON-serialisable via spec_to_json
strategy = create_from_spec(spec, ["AAA"])
```

### Write a strategy in code
```python
from algoplatform.strategy import Strategy, STRATEGIES
from algoplatform.core import Signal
from algoplatform.quant import sma

@STRATEGIES.register("my_trend")
class MyTrend(Strategy):
    name = "my_trend"
    PARAMS = {"n": 50}
    PARAM_BOUNDS = {"n": (10, 200)}          # lets the optimiser and CLI tune it
    @property
    def warmup(self): return self.p("n") + 1
    def on_bar(self, ctx):
        out = []
        for s in self.symbols:
            if s in ctx.bars and self.ready(ctx, s):
                c = ctx.closes(s, self.p("n") + 1)
                out.append(Signal(s, 1.0 if c[-1] > sma(c, self.p("n"))[-1] else 0.0))
        return out
```

### Add a broker
Subclass `BrokerGateway` (or `RestBrokerBase` for HTTP APIs), implement `connect / submit_order / cancel_order / get_positions / get_cash`, emit `BrokerEvent`s for ack/fill/reject/cancel, and register with `@BROKERS.register("name")`. Nothing else changes.

### Run a permission-checked session
```python
from algoplatform.app import TradingPlatform
from algoplatform.core import Role
from algoplatform.strategy import SMACrossover
plat = TradingPlatform()
admin = plat.users.register("admin_user", "Str0ng-Passw0rd!", Role.ADMIN)
trader = plat.users.register("trader_one", "Str0ng-Passw0rd!")
acc = plat.accounts.link(trader, "paper", {})
engine = plat.open_session(trader, acc.account_id, [(SMACrossover(["AAA"]), 1.0)])
# engine.start(); feed bars with engine.on_bars({...}); plat.trip_kill_switch(trader, engine, "reason")
```

## Honest limits

- Fills are bar-based (open/limit/stop touch, optional volume participation). There is no order-book queue or latency simulation, so high-frequency strategies are out of scope.
- No real broker adapters ship here; `RestBrokerBase` is the template. Test any adapter against its sandbox first.
- Credentials are encrypted only if the optional `cryptography` package is installed; otherwise they live in memory only and are never logged.
- Optimisation is single-process. Measured here: about 0.1 s per 1,000 bars per symbol for the SMA strategy; indicator-heavy rule strategies are slower.
- Backtests use whatever data you supply. Synthetic data is for tests and demos and says nothing about real markets.
- Research code, not investment advice. Paper trade for an extended period before risking capital.

## Topic coverage (from the master list)

Strong: order lifecycle and idempotency (13.2), pre-trade controls (13.3), kill switch (12.1), position sizing (11.4), portfolio optimisation (11.1), VaR/ES/stress (12.2), backtesting and bias control (10.x), statistical validation incl. deflated Sharpe and multiple testing (2.1-2.2), performance analytics and tear sheets (15.x), strategy SDK (7.3), user/RBAC and audit (16.6, 17.x).
Partial: execution algorithms (market/limit/stop only; no TWAP/VWAP), derivatives (Black-Scholes and Greeks only), data engineering (in-memory store).
Not included: ML/DL/RL/LLM (Part 8), FIX/native protocol adapters, fundamental-data pipelines (Part 4), alternative data (Part 6), HFT latency engineering.
