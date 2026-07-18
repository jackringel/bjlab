"""bjlab: an open, legible blackjack advantage-play laboratory.

The package is a stack of layers, each independently usable (see DESIGN.md):

    core      Shared vocabulary: rules, cards, hands, compositions, counting, state.
    ev        Layer 1 - exact EV of each action for one hand vs. one upcard.
    strategy  Layer 2 - basic strategy and count-indexed deviation charts.
    sim       Layer 3 - Monte Carlo shoe simulation: EV and time by true count.
    session   Layer 4 - bankroll math: EV/hr, variance, risk of ruin, N0, bet spreads.
    store     Fetch-or-compute caching shared by every layer.

Core types are re-exported here so ``from bjlab import Rules, Hand, ...`` works.
"""

from .core import (
    Action,
    Composition,
    DecisionContext,
    GameState,
    Hand,
    Rank,
    Rules,
    Shoe,
    hilo_tag,
    running_count,
    true_count,
)

__version__ = "0.1.0"

__all__ = [
    "Action",
    "Composition",
    "DecisionContext",
    "GameState",
    "Hand",
    "Rank",
    "Rules",
    "Shoe",
    "hilo_tag",
    "running_count",
    "true_count",
    "__version__",
]
