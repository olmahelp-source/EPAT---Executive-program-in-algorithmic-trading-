"""Position sizing (topics 485 to 489)."""
from __future__ import annotations

import math


def round_to_lot(qty: float, lot: int = 1) -> int:
    """Round toward zero to a multiple of the lot size."""
    if lot <= 0:
        raise ValueError("lot must be positive")
    return int(math.trunc(qty / lot)) * lot


def target_shares(weight: float, equity: float, price: float, multiplier: float = 1.0, lot: int = 1) -> int:
    """Shares (or contracts) for a target weight = position value / equity."""
    if price <= 0 or multiplier <= 0:
        return 0
    return round_to_lot(weight * equity / (price * multiplier), lot)


def fixed_fractional_shares(equity: float, risk_fraction: float, entry: float, stop: float, multiplier: float = 1.0) -> float:
    """Shares such that a stop-out loses `risk_fraction` of equity (topic 485)."""
    dist = abs(entry - stop)
    if dist == 0:
        raise ValueError("stop must differ from entry")
    return equity * risk_fraction / (dist * multiplier)


def vol_target_scale(target_vol: float, forecast_vol: float, cap: float = 3.0) -> float:
    """Leverage that targets a volatility, capped (topic 487). Vols are annualized."""
    if forecast_vol <= 0:
        return cap
    return min(cap, target_vol / forecast_vol)


def kelly_fraction(mu: float, variance: float, fraction: float = 0.5) -> float:
    """Continuous Kelly leverage mu / variance, scaled by a safety fraction (topic 486)."""
    if variance <= 0:
        return 0.0
    return fraction * mu / variance


def gap_adjusted_position_pct(risk_budget: float, stop_distance: float, gap_quantile: float) -> float:
    """Position as a fraction of equity using the larger of stop distance and overnight gap quantile (topic 488)."""
    return risk_budget / max(stop_distance, gap_quantile)
