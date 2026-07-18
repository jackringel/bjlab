"""Headline session numbers from sim output + a spread + table speed."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .betting import BetSpread

if TYPE_CHECKING:
    from ..sim import SimResult


@dataclass(frozen=True)
class SessionStats:
    """Everything Layer 4 reports, in the bankroll's currency units."""

    ev_per_round: float
    var_per_round: float
    ev_per_hour: float
    std_per_hour: float
    n0_rounds: float
    risk_of_ruin: float


def derive_session_stats(
    sim: "SimResult",
    spread: BetSpread,
    *,
    bankroll: float,
    rounds_per_hour: float = 100.0,
) -> SessionStats:
    """Combine per-count sim stats with a bet spread and speed. (Planned.)

    With f(tc) the count frequencies, b(tc) the spread's wagers, and
    mu(tc)/var(tc) the per-unit round stats from the sim:

        ev_per_round  = sum_tc f(tc) * b(tc) * mu(tc)
        var_per_round = via the law of total variance across counts
                        (within-count b(tc)^2 * var(tc) plus the variance of
                        the per-count means around the overall mean)
        ev_per_hour   = ev_per_round * rounds_per_hour
        std_per_hour  = sqrt(var_per_round * rounds_per_hour)

    plus ``n0`` and ``risk_of_ruin`` from ``bjlab.session.risk``.
    ``rounds_per_hour`` is the knob for crew size / heads-up play: fewer
    players means more rounds per hour.
    """
    raise NotImplementedError
