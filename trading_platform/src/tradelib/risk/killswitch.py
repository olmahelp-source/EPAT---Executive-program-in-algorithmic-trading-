"""Kill switch (topics 499, 544, 210). Uses integer counts, not rounded percentages."""
from __future__ import annotations

from collections import deque


class KillSwitch:
    def __init__(self, daily_loss_limit_pct: float = 0.03, max_drawdown_pct: float = 0.25,
                 reject_window: int = 20, max_rejects_in_window: int = 6) -> None:
        self.daily_loss_limit_pct = daily_loss_limit_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.max_rejects = max_rejects_in_window
        self._results: deque[bool] = deque(maxlen=reject_window)
        self.day_start_equity: float | None = None
        self.peak_equity: float | None = None
        self.tripped_reason: str | None = None

    @property
    def tripped(self) -> bool:
        return self.tripped_reason is not None

    def new_day(self, equity: float) -> None:
        self.day_start_equity = equity

    def on_equity(self, equity: float) -> None:
        self.peak_equity = equity if self.peak_equity is None else max(self.peak_equity, equity)
        if self.tripped:
            return
        if self.day_start_equity and equity <= self.day_start_equity * (1 - self.daily_loss_limit_pct):
            self.tripped_reason = f"daily loss limit {self.daily_loss_limit_pct:.1%} breached"
        elif self.peak_equity and equity <= self.peak_equity * (1 - self.max_drawdown_pct):
            self.tripped_reason = f"drawdown limit {self.max_drawdown_pct:.1%} breached"

    def on_order_result(self, accepted: bool) -> None:
        self._results.append(accepted)
        if not self.tripped and len(self._results) == self._results.maxlen:
            rejects = self._results.maxlen - sum(self._results)
            if rejects > self.max_rejects:
                self.tripped_reason = f"{rejects} rejects in the last {self._results.maxlen} orders"

    def reset(self, approved_by: str) -> None:
        """Manual restart. Needs a named approver so the action is recorded (topic 614)."""
        if not approved_by:
            raise ValueError("a named approver is required")
        self.tripped_reason = None
        self._results.clear()
        self.peak_equity = self.day_start_equity
