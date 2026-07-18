"""Bankroll risk math: risk of ruin and N0.

All inputs are *per-round* mean ``ev`` and variance ``var`` in the same
monetary units as ``bankroll``, assuming i.i.d. rounds (a fixed spread over
a stationary count distribution). These are the standard diffusion
(Brownian-motion) approximations; the canonical treatment is Schlesinger,
*Blackjack Attack*.
"""

from __future__ import annotations

import math


def risk_of_ruin(bankroll: float, ev: float, var: float) -> float:
    """Probability of ever losing the entire bankroll, betting this fixed
    strategy forever (no stop-win, no resizing):

        RoR = exp(-2 * ev * bankroll / var)

    Diffusion approximation, accurate when the per-round edge is small
    relative to the per-round standard deviation (always true in blackjack).
    Edge cases: non-positive EV or non-positive bankroll means certain ruin
    (returns 1.0).
    """
    if var <= 0:
        raise ValueError("variance must be positive")
    if ev <= 0 or bankroll <= 0:
        return 1.0
    return min(1.0, math.exp(-2.0 * ev * bankroll / var))


def n0(ev: float, var: float) -> float:
    """N0: the number of rounds at which cumulative expectation equals one
    cumulative standard deviation:

        N0 = var / ev^2      (i.e. (sigma/mu)^2 per round)

    After N0 rounds, EV has "overcome" one sigma of luck; it is the standard
    yardstick for how long the long run is for a given game and spread.
    Defined only for positive-EV games.
    """
    if var <= 0:
        raise ValueError("variance must be positive")
    if ev <= 0:
        raise ValueError("N0 is defined only for positive-EV games")
    return var / (ev * ev)
