"""Core value types shared by the whole library (master list topics 3, 5, 18, 530)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Side(Enum):
    BUY = 1
    SELL = -1

    @property
    def sign(self) -> int:
        return self.value

    @classmethod
    def from_qty(cls, signed_qty: float) -> "Side":
        return cls.BUY if signed_qty > 0 else cls.SELL


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"


class TimeInForce(Enum):
    DAY = "day"      # expires at the end of the bar after submission
    GTC = "gtc"      # stays until filled or cancelled


@dataclass(frozen=True)
class Instrument:
    """Static contract data: P&L = price change x multiplier x quantity (topic 18)."""
    symbol: str
    multiplier: float = 1.0
    tick_size: float = 0.01
    lot_size: int = 1
    currency: str = "USD"


@dataclass(frozen=True)
class Bar:
    """One completed bar. ts is epoch seconds (UTC) of the bar start."""
    symbol: str
    ts: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class OrderRequest:
    """What a strategy or portfolio manager asks for. The OMS turns it into an Order."""
    symbol: str
    side: Side
    qty: int
    order_type: OrderType = OrderType.MARKET
    limit_price: float | None = None
    tif: TimeInForce = TimeInForce.DAY
    strategy_id: str = ""
    ts: int = 0
    reduce_only: bool = False

    @property
    def signed_qty(self) -> int:
        return self.side.sign * self.qty


@dataclass(frozen=True)
class Fill:
    order_id: str
    symbol: str
    side: Side
    qty: int
    price: float
    fee: float
    ts: int

    @property
    def signed_qty(self) -> int:
        return self.side.sign * self.qty
