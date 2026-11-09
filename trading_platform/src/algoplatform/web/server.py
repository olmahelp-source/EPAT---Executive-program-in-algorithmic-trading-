"""JSON API + static file server for the UI.

Security posture (read before exposing beyond localhost):
* Bearer tokens from ``UserManager`` (HMAC-signed, expiring); every route except login/register
  needs one, and every action goes through ``TradingPlatform`` which enforces RBAC.
* Request bodies are capped, static paths are confined to ``static/``, and responses carry
  CSP / nosniff / no-referrer headers. There is NO TLS here: bind to 127.0.0.1 or put a TLS
  reverse proxy in front. This is a paper-trading research UI, not a hardened live gateway.
"""
from __future__ import annotations

import json
import math
import mimetypes
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import numpy as np
import pandas as pd

from ..analytics.metrics import drawdown_series
from ..app.platform import TradingPlatform
from ..core.config import PlatformConfig
from ..core.enums import OrderType, Permission, Role, Side
from ..core.exceptions import (AuthenticationError, AuthorizationError, BacktestError, ConfigError, DataError,
                               OptimizationError, OrderError, PlatformError, RiskError, StrategyError, UserError,
                               ValidationError)
from ..core.logging import get_logger
from ..core.models import Bar
from ..data import MarketData, synthetic
from ..optimize import ParameterSpace
from ..strategy.base import STRATEGIES
from ..users.manager import User, UserManager

log = get_logger(__name__)
STATIC = os.path.join(os.path.dirname(__file__), "static")
MAX_BODY = 1_000_000
_STATUS = ((AuthenticationError, 401), (AuthorizationError, 403), (UserError, 409), (RiskError, 409), (OrderError, 409),
           (ValidationError, 400), (ConfigError, 400), (StrategyError, 400), (BacktestError, 400),
           (OptimizationError, 400), (DataError, 400))


def clean(o: Any) -> Any:
    """Make anything JSON-safe: numpy -> python, NaN/inf -> null, timestamps -> ISO strings."""
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return f if math.isfinite(f) else None
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp,)) or hasattr(o, "isoformat"):
        return o.isoformat()
    if hasattr(o, "value") and not isinstance(o, (str, int)):          # Enum
        return o.value
    return o


def series_points(s: pd.Series, max_points: int = 400) -> List[list]:
    if len(s) > max_points:
        s = s.iloc[np.linspace(0, len(s) - 1, max_points).astype(int)]
    return [[pd.Timestamp(i).strftime("%Y-%m-%d"), float(v)] for i, v in s.items()]


class LiveSession:
    """A paper-trading engine fed by a synthetic random-walk price stream."""

    def __init__(self, engine, symbols: List[str], seed: int) -> None:
        self.engine, self.symbols = engine, symbols
        self.rng = np.random.default_rng(seed)
        self.last = {s: float(self.rng.uniform(50, 300)) for s in symbols}
        self.next_ts = pd.Timestamp("2024-01-01")
        self.lock = threading.RLock()
        self.history: Dict[str, List[float]] = {s: [] for s in symbols}

    def step(self, n: int) -> None:
        with self.lock:
            for _ in range(n):
                bars = {}
                for s in self.symbols:
                    o = self.last[s]
                    c = o * float(np.exp(self.rng.normal(0.0003, 0.012)))
                    bars[s] = Bar(self.next_ts, s, o, max(o, c) * 1.003, min(o, c) * 0.997, c, 1e6)
                    self.last[s] = c
                    self.history[s].append(round(c, 4))
                    self.history[s] = self.history[s][-200:]
                self.engine.on_bars(bars)
                self.next_ts = self.next_ts + pd.offsets.BDay(1)


class App:
    def __init__(self, config: Optional[PlatformConfig] = None, fast_hash: bool = False) -> None:
        self.platform = TradingPlatform(config or PlatformConfig(log_level="WARNING"))
        if fast_hash:                                    # tests only: cheap scrypt
            from ..users.security import PasswordHasher
            self.platform.users.hasher = PasswordHasher(n=2 ** 4)
        self.sessions: Dict[str, LiveSession] = {}
        self.lock = threading.Lock()
        self.routes: Dict[Tuple[str, str], Tuple[Callable, bool]] = {}
        self._register()

    # ---- routing --------------------------------------------------------------------------
    def route(self, method: str, path: str, public: bool = False):
        def deco(fn):
            self.routes[(method, path)] = (fn, public)
            return fn
        return deco

    def dispatch(self, method: str, path: str, body: Dict[str, Any], token: Optional[str]) -> Tuple[int, Any]:
        entry = self.routes.get((method, path))
        if entry is None:
            return 404, {"error": "NOT_FOUND", "message": f"no route {method} {path}"}
        fn, public = entry
        try:
            user = None
            if not public:
                if not token:
                    raise AuthenticationError("missing bearer token")
                user = self.platform.users.user_from_token(token)
            return 200, clean(fn(user, body))
        except PlatformError as exc:
            for cls, code in _STATUS:
                if isinstance(exc, cls):
                    return code, {"error": exc.code, "message": exc.message}
            return 500, {"error": "INTERNAL", "message": "internal error"}
        except (KeyError, TypeError, ValueError) as exc:     # malformed client input
            return 400, {"error": "BAD_REQUEST", "message": f"invalid request: {exc}"}
        except Exception:  # noqa: BLE001
            log.exception("unhandled error on %s %s", method, path)
            return 500, {"error": "INTERNAL", "message": "internal error"}

    # ---- helpers --------------------------------------------------------------------------
    @staticmethod
    def _data(body: Dict[str, Any]) -> Tuple[MarketData, List[str]]:
        symbols = [s.strip().upper() for s in body.get("symbols", ["AAA", "BBB", "CCC"]) if s.strip()]
        if not 1 <= len(symbols) <= 10 or not all(s.isalnum() and len(s) <= 8 for s in symbols):
            raise ValidationError("symbols: 1-10 alphanumeric tickers (max 8 chars)")
        bars = int(body.get("bars", 756))
        if not 150 <= bars <= 3000:
            raise ValidationError("bars must be between 150 and 3000")
        md = MarketData()
        for s, df in synthetic.universe(symbols, n=bars, seed=int(body.get("seed", 7))).items():
            md.add(s, df)
        return md, symbols

    def _session(self, user: User) -> LiveSession:
        s = self.sessions.get(user.user_id)
        if s is None:
            raise ValidationError("no open session; open one first")
        return s

    # ---- endpoints --------------------------------------------------------------------------
    def _register(self) -> None:
        r, P = self.route, self.platform

        @r("POST", "/api/register", public=True)
        def register(_u, b):
            # bootstrap: on a brand-new install the first account is the administrator. Everyone after
            # that self-registers as a plain trader; only an admin can raise roles.
            with self.lock:
                role = Role.ADMIN if P.users.user_count() == 0 else Role.TRADER
                user = P.users.register(b["username"], b["password"], role)
            return {"username": user.username, "role": user.role}

        @r("POST", "/api/login", public=True)
        def login(_u, b):
            token = P.users.login(b["username"], b["password"])
            user = P.users.user_from_token(token)
            return {"token": token, "username": user.username, "role": user.role}

        @r("GET", "/api/me")
        def me(u, _b):
            return {"username": u.username, "role": u.role, "permissions": sorted(p.value for p in Permission if u.has(p))}

        @r("GET", "/api/strategies")
        def strategies(_u, _b):
            return [{"name": n, "params": STRATEGIES.get(n).PARAMS, "bounds": STRATEGIES.get(n).PARAM_BOUNDS,
                     "doc": (STRATEGIES.get(n).__doc__ or "").strip().split("\n")[0]} for n in STRATEGIES.names()]

        @r("POST", "/api/backtest")
        def backtest(u, b):
            md, symbols = self._data(b)
            target = b["spec"] if b.get("spec") else b["strategy"]
            if not b.get("spec") and b["strategy"] == "pairs_trading":
                symbols = symbols[:2]
            res = P.backtest(u, target, md, symbols, b.get("params") or {})
            rep = res.report(n_trials=int(b.get("n_trials", 1)))
            eq = res.equity
            bench = (1 + res.benchmark).cumprod() * eq.iloc[0] if res.benchmark is not None else None
            trades = res.trades_frame().tail(200)
            return {"metrics": rep["performance"], "trade_stats": rep["trades"],
                    "significance": rep.get("significance"), "equity": series_points(eq),
                    "drawdown": series_points(drawdown_series(eq)),
                    "benchmark": series_points(bench) if bench is not None else None,
                    "trades": trades.assign(entry_ts=trades["entry_ts"].astype(str),
                                            exit_ts=trades["exit_ts"].astype(str)).round(4).to_dict("records"),
                    "orders": res.order_count, "rejected": res.rejected_orders,
                    "kill_switch": res.kill_switch_triggered, "symbols": symbols}

        @r("POST", "/api/optimize")
        def optimize(u, b):
            method = b.get("method", "random")
            if method not in ("random", "genetic"):
                raise ValidationError("method must be random or genetic")
            n = int(b.get("n_iter", 20))
            if not 5 <= n <= 60:
                raise ValidationError("n_iter must be between 5 and 60")
            if int(b.get("bars", 500)) > 1500:
                raise ValidationError("bars must be <= 1500 for optimisation")
            md, symbols = self._data({**b, "bars": b.get("bars", 500)})
            cls = STRATEGIES.get(b["strategy"])
            if not cls.PARAM_BOUNDS:
                raise ValidationError("strategy has no tunable parameters")
            space = ParameterSpace.from_bounds(cls.PARAM_BOUNDS)
            kw = {"n_iter": n} if method == "random" else {"population": max(6, n // 4), "generations": 4}
            res = P.optimize(u, b["strategy"], md, space, symbols, b.get("metric", "sharpe"), method, **kw)
            top = res.top(10)
            return {"summary": res.summary(), "top": top.to_dict("records"),
                    "scores": [float(x) for x in res.trials["score"].replace([-np.inf], np.nan).dropna()],
                    "plateau": res.plateau_score(space)}

        # ---- live (paper) session -----------------------------------------------------------
        @r("POST", "/api/session/open")
        def open_session(u, b):
            symbols = [s.strip().upper() for s in b.get("symbols", ["AAA", "BBB"]) if s.strip()]
            if not 1 <= len(symbols) <= 6 or not all(s.isalnum() and len(s) <= 8 for s in symbols):
                raise ValidationError("symbols: 1-6 alphanumeric tickers")
            with self.lock:
                if u.user_id in self.sessions:
                    raise ValidationError("a session is already open; close it first")
                strategies = []
                if b.get("strategy"):
                    strategies = [(P.create_strategy(u, b["strategy"], symbols, **(b.get("params") or {})), 1.0)]
                acc = P.accounts.link(u, "paper", {}, "ui-session")
                engine = P.open_session(u, acc.account_id, strategies)
                engine.start()
                sess = LiveSession(engine, symbols, int(b.get("seed", 1)))
                sess.step(1)
                self.sessions[u.user_id] = sess
            return self._snapshot(sess)

        @r("GET", "/api/session")
        def session(u, _b):
            UserManager.authorize(u, Permission.VIEW_PORTFOLIO)
            s = self.sessions.get(u.user_id)
            return {"open": False} if s is None else self._snapshot(s)

        @r("POST", "/api/session/step")
        def step(u, b):
            UserManager.authorize(u, Permission.PLACE_ORDER)
            s = self._session(u)
            n = int(b.get("n", 1))
            if not 1 <= n <= 100:
                raise ValidationError("n must be 1-100")
            s.step(n)
            return self._snapshot(s)

        @r("POST", "/api/session/order")
        def order(u, b):
            s = self._session(u)
            with s.lock:
                o = P.place_manual_order(u, s.engine, b["symbol"].upper(), Side(b["side"]), float(b["quantity"]),
                                         OrderType(b.get("type", "MARKET")),
                                         float(b["limit_price"]) if b.get("limit_price") else None)
            return {"order": self._order(o), **self._snapshot(s)}

        @r("POST", "/api/session/cancel_all")
        def cancel_all(u, _b):
            s = self._session(u)
            n = P.cancel_all(u, s.engine)
            return {"cancelled": n, **self._snapshot(s)}

        @r("POST", "/api/session/killswitch")
        def killswitch(u, b):
            s = self._session(u)
            with s.lock:
                if b.get("action") == "trip":
                    P.trip_kill_switch(u, s.engine, b.get("reason") or "manual halt from UI")
                elif b.get("action") == "reset":
                    P.reset_kill_switch(u, s.engine, b.get("reason", ""))
                else:
                    raise ValidationError("action must be trip or reset")
            return self._snapshot(s)

        @r("POST", "/api/session/close")
        def close(u, _b):
            with self.lock:
                s = self.sessions.pop(u.user_id, None)
            if s:
                s.engine.stop()
            return {"open": False}

        # ---- admin ---------------------------------------------------------------------------
        @r("GET", "/api/audit")
        def audit(u, _b):
            if not (u.has(Permission.MANAGE_USERS) or u.has(Permission.MANAGE_RISK)):
                raise AuthorizationError("audit log needs admin or risk-manager role")
            return list(reversed(P.audit.entries()[-150:]))

        @r("GET", "/api/users")
        def users(u, _b):
            return [{"id": x.user_id, "username": x.username, "role": x.role, "active": x.active}
                    for x in P.users.list_users(u)]

        @r("POST", "/api/users/role")
        def set_role(u, b):
            P.users.set_role(u, b["user_id"], Role(b["role"]))
            return {"ok": True}

    # ---- serialisation of live state ---------------------------------------------------------
    @staticmethod
    def _order(o) -> Dict[str, Any]:
        return {"id": o.client_order_id, "symbol": o.symbol, "side": o.side, "qty": o.quantity, "type": o.order_type,
                "limit": o.limit_price, "status": o.status, "filled": o.filled_qty, "avg": o.avg_fill_price,
                "reason": o.reject_reason, "strategy": o.strategy_id}

    def _snapshot(self, s: LiveSession) -> Dict[str, Any]:
        with s.lock:
            e = s.engine
            snap = e.portfolio.snapshot()
            ks = e.risk.kill_switch
            return {"open": True, "symbols": s.symbols, "prices": s.last, "history": s.history,
                    "portfolio": snap, "bars": e.bars_processed,
                    "equity_curve": series_points(e.portfolio.equity_curve().tail(300)) if e.bars_processed else [],
                    "orders": [self._order(o) for o in reversed(e.oms.all_orders()[-60:])],
                    "kill_switch": {"state": ks.state, "reason": ks.reason, "source": ks.source},
                    "risk": {"drawdown": e.risk.monitor.drawdown, "daily_pnl_pct": e.risk.monitor.daily_pnl_pct,
                             "max_daily_loss_pct": e.cfg.risk.max_daily_loss_pct,
                             "max_drawdown_pct": e.cfg.risk.max_drawdown_pct,
                             "rejections": e.risk.rejections, "exposure_scalar": e.risk.exposure_scalar()},
                    "strategy_errors": e.strategy_errors, "anomalies": len(e.oms.anomalies)}


def make_handler(app: App):
    class Handler(BaseHTTPRequestHandler):
        server_version = "algoplatform"

        def log_message(self, fmt, *args):          # quiet by default
            log.debug("%s " + fmt, self.address_string(), *args)

        def _headers(self, code: int, ctype: str, length: int) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(length))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

        def _json(self, code: int, obj: Any) -> None:
            raw = json.dumps(obj).encode()
            self._headers(code, "application/json; charset=utf-8", len(raw))
            self.wfile.write(raw)

        def _static(self, path: str) -> None:
            rel = "index.html" if path in ("/", "") else path.lstrip("/")
            full = os.path.realpath(os.path.join(STATIC, rel))
            if not full.startswith(os.path.realpath(STATIC) + os.sep) or not os.path.isfile(full):
                return self._json(404, {"error": "NOT_FOUND", "message": "not found"})
            ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
            with open(full, "rb") as fh:
                data = fh.read()
            self._headers(200, ctype + ("; charset=utf-8" if ctype.startswith("text") or "javascript" in ctype else ""), len(data))
            self.wfile.write(data)

        def _handle(self, method: str) -> None:
            path = urlparse(self.path).path
            if method == "GET" and not path.startswith("/api/"):
                return self._static(path)
            body: Dict[str, Any] = {}
            if method == "POST":
                try:
                    n = int(self.headers.get("Content-Length") or 0)
                except ValueError:
                    return self._json(400, {"error": "BAD_REQUEST", "message": "bad Content-Length"})
                if n > MAX_BODY:
                    return self._json(413, {"error": "TOO_LARGE", "message": "body too large"})
                try:
                    body = json.loads(self.rfile.read(n) or b"{}")
                    if not isinstance(body, dict):
                        raise ValueError
                except ValueError:
                    return self._json(400, {"error": "BAD_REQUEST", "message": "body must be a JSON object"})
            auth = self.headers.get("Authorization", "")
            token = auth[7:] if auth.startswith("Bearer ") else None
            code, obj = app.dispatch(method, path, body, token)
            self._json(code, obj)

        def do_GET(self):
            self._handle("GET")

        def do_POST(self):
            self._handle("POST")
    return Handler


def serve(host: str = "127.0.0.1", port: int = 8080, app: Optional[App] = None) -> None:
    app = app or App()
    httpd = ThreadingHTTPServer((host, port), make_handler(app))
    print(f"algoplatform UI on http://{host}:{port}  (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
