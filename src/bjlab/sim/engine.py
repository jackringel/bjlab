"""The shoe-simulation engine."""

from __future__ import annotations

from dataclasses import dataclass

from ..core import Rules
from ..store import Store
from ..strategy import DeviationChart, StrategyChart


@dataclass(frozen=True)
class SimConfig:
    rules: Rules
    n_rounds: int = 1_000_000
    seed: int | None = None


@dataclass(frozen=True)
class TrueCountBucket:
    """Stats for rounds whose floored true count fell in this bucket.

    EV/variance are per round of one unit flat-bet -- bet sizing is Layer
    4's job, applied on top of these.
    """

    true_count: int
    frequency: float      # share of all rounds
    ev_per_round: float   # units of initial bet
    var_per_round: float  # units^2


@dataclass(frozen=True)
class SimResult:
    config: SimConfig
    buckets: tuple[TrueCountBucket, ...]

    @property
    def total_frequency(self) -> float:
        return sum(b.frequency for b in self.buckets)


def simulate(
    config: SimConfig,
    strategy: StrategyChart | None = None,
    deviations: DeviationChart | None = None,
    store: Store | None = None,
) -> SimResult:
    """Run the Monte Carlo shoe sim. (Planned.)

    Deals rounds from a ``Shoe`` (reshuffling at ``rules.penetration``),
    playing every hand per ``strategy`` overridden by ``deviations``
    (generating both from Layer 2 -- or fetching from ``store`` -- when not
    supplied). Each round is recorded under its floored true count *at the
    moment of betting* (before the deal). Results are cached keyed by
    ``(rules.stable_id(), n_rounds, seed, chart ids)``.
    """
    raise NotImplementedError
