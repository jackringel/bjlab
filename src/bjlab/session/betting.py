"""Bet spreads and Kelly sizing."""

from __future__ import annotations

import math
from bisect import bisect_right
from dataclasses import dataclass
from typing import TYPE_CHECKING, Mapping

if TYPE_CHECKING:
    from ..sim import SimResult


@dataclass(frozen=True)
class BetSpread:
    """Wager as a step function of the floored true count.

    ``bets`` maps true counts to wagers (currency or units -- just be
    consistent with the bankroll you pair it with). ``bet_for`` floors the
    exact true count, clamps it to the keyed range, and returns the entry at
    the largest key <= that count. A wager of 0 means sit out ("wong out").

    Example: ``BetSpread({0: 0, 1: 25, 2: 50, 4: 100})`` wongs out below
    TC 1, bets 25 at TC 1, 50 at TC 2-3, and 100 at TC 4+.
    """

    bets: Mapping[int, float]

    def __post_init__(self) -> None:
        if not self.bets:
            raise ValueError("bets must not be empty")
        if any(b < 0 for b in self.bets.values()):
            raise ValueError("wagers must be non-negative")

    def bet_for(self, true_count: float) -> float:
        keys = sorted(self.bets)
        tc = max(keys[0], min(math.floor(true_count), keys[-1]))
        return self.bets[keys[bisect_right(keys, tc) - 1]]


def kelly_fraction(ev_per_unit: float, var_per_unit: float) -> float:
    """Full-Kelly fraction of bankroll to wager on one round:

        f* = EV / Var    (mean over variance, both per unit wagered)

    This is the first-order optimum of expected log-bankroll growth, valid
    for the small edges blackjack offers (exact Kelly maximizes
    E[log(1 + f*X)]; for |X| outcomes concentrated near +/-1 and small EV,
    f* = mu/sigma^2 is the standard approximation). Negative-EV spots
    return 0.0 -- never bet a negative edge.
    """
    if var_per_unit <= 0:
        raise ValueError("variance must be positive")
    return max(0.0, ev_per_unit / var_per_unit)


def optimal_spread(
    sim: "SimResult",
    bankroll: float,
    *,
    unit: float,
    max_bet: float | None = None,
    fractional_kelly: float = 1.0,
) -> BetSpread:
    """Derive a bet spread from sim results and a bankroll. (Planned.)

    Per true count tc: wager = fractional_kelly * bankroll *
    kelly_fraction(ev(tc), var(tc)), rounded down to a multiple of ``unit``
    and capped at ``max_bet``; negative-EV counts get the table minimum or a
    wong-out (0), whichever the caller configures. Fractional Kelly < 1
    trades growth for drawdown protection.
    """
    raise NotImplementedError
