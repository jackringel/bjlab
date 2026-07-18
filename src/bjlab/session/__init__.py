"""Layer 4: turning sim output into money.

Given a Layer 3 ``SimResult``, a bet spread, table speed, and a bankroll,
this layer produces the numbers advantage players actually plan around:
EV/hand, EV/hour, variance, risk of ruin, N0 -- and, in reverse, an optimal
(Kelly) bet spread for a bankroll. "Layer 5" (overall vs. session bankroll)
is folded in here: one bankroll, sized session by session.

The closed-form pieces (Kelly fraction, risk of ruin, N0) are implemented
now and usable standalone -- you can plug in numbers from any source.
"""

from .betting import BetSpread, kelly_fraction, optimal_spread
from .risk import n0, risk_of_ruin
from .stats import SessionStats, derive_session_stats

__all__ = [
    "BetSpread",
    "kelly_fraction",
    "optimal_spread",
    "n0",
    "risk_of_ruin",
    "SessionStats",
    "derive_session_stats",
]
