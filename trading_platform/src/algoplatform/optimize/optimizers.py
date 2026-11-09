"""Parameter optimisers: grid, random, genetic. Objectives are plain callables params -> score."""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from ..backtest.engine import BacktestEngine, BacktestResult
from ..core.exceptions import OptimizationError, PlatformError
from ..core.logging import get_logger
from .space import ParameterSpace

log = get_logger(__name__)
Objective = Callable[[Dict[str, Any]], float]


@dataclass
class OptimizationResult:
    trials: pd.DataFrame                       # one row per evaluation: params..., score, error
    best_params: Dict[str, Any]
    best_score: float
    n_trials: int
    method: str
    elapsed: float = 0.0

    def top(self, n: int = 10) -> pd.DataFrame:
        return self.trials.sort_values("score", ascending=False).head(n)

    def summary(self) -> Dict[str, Any]:
        s = self.trials["score"].replace([-np.inf, np.inf], np.nan).dropna()
        return {"method": self.method, "trials": self.n_trials, "failed": int(self.trials["error"].notna().sum()),
                "best_score": self.best_score, "best_params": self.best_params,
                "score_mean": float(s.mean()) if len(s) else float("nan"),
                "score_std": float(s.std()) if len(s) > 1 else float("nan"),
                "score_variance_for_dsr": float(s.var()) if len(s) > 1 else float("nan"), "seconds": round(self.elapsed, 2)}

    def plateau_score(self, space: ParameterSpace, params: Optional[Dict[str, Any]] = None, points: int = 5,
                      radius: float = 0.2) -> float:
        """Mean score of nearby points divided by the point's own score. Near 1 => a plateau
        (robust); near 0 => a lone spike (likely overfit). NaN when there is nothing to compare.

        Uses adjacent grid points when they were evaluated (grid search); otherwise falls back to
        evaluated trials within ``radius`` of each axis range (random / genetic search)."""
        params = params or self.best_params
        own = self._lookup(params)
        if own is None or own <= 0:
            return float("nan")
        neigh = [self._lookup(n) for n in space.neighbors(params, points)]
        neigh = [v for v in neigh if v is not None and math.isfinite(v)]
        if not neigh:
            neigh = self._nearby(space, params, radius)
        return float(np.mean(neigh) / own) if neigh else float("nan")

    def _nearby(self, space: ParameterSpace, params: Dict[str, Any], radius: float) -> List[float]:
        df = self.trials[np.isfinite(self.trials["score"])]
        mask = np.ones(len(df), dtype=bool)
        same = np.ones(len(df), dtype=bool)
        for p in space.params:
            col = df[p.name]
            if p.kind == "choice":
                mask &= (col == params[p.name]).to_numpy()
            else:
                mask &= ((col - params[p.name]).abs() <= radius * (p.high - p.low)).to_numpy()
            same &= (col == params[p.name]).to_numpy()
        return [float(v) for v in df.loc[mask & ~same, "score"]]

    def _lookup(self, params: Dict[str, Any]) -> Optional[float]:
        df = self.trials
        mask = np.ones(len(df), dtype=bool)
        for k, v in params.items():
            if k in df.columns:
                mask &= (df[k] == v).to_numpy()
        return float(df.loc[mask, "score"].iloc[0]) if mask.any() else None


class _Runner:
    """Evaluates points with caching and failure isolation (a crashing trial scores -inf)."""

    def __init__(self, objective: Objective, space: ParameterSpace) -> None:
        self.objective, self.space = objective, space
        self.cache: Dict[tuple, float] = {}
        self.rows: List[Dict[str, Any]] = []

    def evaluate(self, params: Dict[str, Any]) -> float:
        key = tuple(params[n] for n in self.space.names)
        if key in self.cache:
            return self.cache[key]
        err = None
        try:
            score = float(self.objective(params))
            if not math.isfinite(score):
                score, err = -math.inf, "non-finite score"
        except PlatformError as exc:
            score, err = -math.inf, exc.message or exc.code
        except Exception as exc:  # noqa: BLE001 - one bad parameter set must not kill the search
            log.warning("trial %s failed: %r", params, exc)
            score, err = -math.inf, repr(exc)
        self.cache[key] = score
        self.rows.append({**params, "score": score, "error": err})
        return score

    def result(self, method: str, t0: float) -> OptimizationResult:
        df = pd.DataFrame(self.rows)
        if df.empty:
            raise OptimizationError("no trials were evaluated")
        ok = df[np.isfinite(df["score"])]
        if ok.empty:
            raise OptimizationError("every trial failed", details={"first_error": str(df["error"].iloc[0])})
        best = ok.loc[ok["score"].idxmax()]
        bp = {n: _py(best[n]) for n in self.space.names}
        return OptimizationResult(df, bp, float(best["score"]), len(df), method, time.time() - t0)


def _py(v: Any) -> Any:
    return v.item() if hasattr(v, "item") else v


def grid_search(objective: Objective, space: ParameterSpace, points: int = 5, max_trials: int = 2000) -> OptimizationResult:
    t0 = time.time()
    if space.grid_size(points) > max_trials * 10:
        raise OptimizationError("grid too large; use random_search or reduce points",
                                details={"size": space.grid_size(points)})
    run = _Runner(objective, space)
    for i, p in enumerate(space.grid(points)):
        if i >= max_trials:
            log.warning("grid truncated at %d trials", max_trials)
            break
        run.evaluate(p)
    return run.result("grid", t0)


def random_search(objective: Objective, space: ParameterSpace, n_iter: int = 50, seed: Optional[int] = 0) -> OptimizationResult:
    t0 = time.time()
    rng = np.random.default_rng(seed)
    run = _Runner(objective, space)
    for _ in range(n_iter):
        run.evaluate(space.sample(rng))
    return run.result("random", t0)


def genetic_search(objective: Objective, space: ParameterSpace, population: int = 16, generations: int = 8,
                   elite: int = 2, mutation_rate: float = 0.3, tournament: int = 3,
                   seed: Optional[int] = 0) -> OptimizationResult:
    """Simple GA: tournament selection, uniform crossover, Gaussian mutation, elitism."""
    t0 = time.time()
    rng = np.random.default_rng(seed)
    run = _Runner(objective, space)
    pop = [space.sample(rng) for _ in range(population)]
    for _ in range(generations):
        scores = [run.evaluate(p) for p in pop]
        order = np.argsort(scores)[::-1]
        nxt = [pop[i] for i in order[:elite]]
        while len(nxt) < population:
            def pick():
                idx = rng.integers(len(pop), size=tournament)
                return pop[int(idx[np.argmax([scores[i] for i in idx])])]
            a, b = pick(), pick()
            child = {n: (a[n] if rng.random() < 0.5 else b[n]) for n in space.names}
            for p in space.params:
                if rng.random() < mutation_rate:
                    child[p.name] = p.perturb(child[p.name], rng)
            if space.valid(child):
                nxt.append(child)
            else:
                nxt.append(space.sample(rng))
        pop = nxt
    for p in pop:
        run.evaluate(p)
    return run.result("genetic", t0)


def optimize(objective: Objective, space: ParameterSpace, method: str = "random", **kwargs: Any) -> OptimizationResult:
    methods = {"grid": grid_search, "random": random_search, "genetic": genetic_search}
    if method not in methods:
        raise OptimizationError(f"unknown method '{method}'", details={"valid": sorted(methods)})
    return methods[method](objective, space, **kwargs)


# ---- backtest objectives ---------------------------------------------------------------------
def backtest_objective(engine: BacktestEngine, factory: Callable[..., Any], metric: str = "sharpe",
                       start=None, end=None, min_trades: int = 5, max_drawdown: Optional[float] = None) -> Objective:
    """Score = chosen metric of a backtest; penalised to -inf when it trades too little or
    breaches a drawdown cap (guards against 'optimal' parameters that never trade)."""
    def objective(params: Dict[str, Any]) -> float:
        res = engine.run(factory(**params), start=start, end=end)
        if len(res.trades) < min_trades:
            return -math.inf
        m = res.metrics()
        if max_drawdown is not None and m["max_drawdown"] < -abs(max_drawdown):
            return -math.inf
        if metric not in m:
            raise OptimizationError(f"unknown metric '{metric}'", details={"valid": sorted(m)})
        return float(m[metric])
    return objective
