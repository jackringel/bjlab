"""Core data structures for bjlab.

This package contains *only* definitions and helpers; no EV
math or simulation:

- ``types``    - Rank and Action enums.
- ``rules``    - immutable table-rules configuration (and its stable cache id).
- ``hand``     - immutable hand representation and total math.
- ``deck``     - Composition (undealt-card multiset) and the Shoe (planned).
- ``counting`` - Hi-Lo tags, running/true counts, count-conditioned decks.
- ``state``    - DecisionContext (Layer 1 input) and GameState (planned).

Everything higher in the stack is a pure function of these objects.
"""

from .counting import HILO_TAGS, hilo_tag, running_count, true_count
from .deck import CARDS_PER_DECK, Composition, Shoe
from .hand import Hand
from .rules import BlackjackPayout, DoubleRule, Rules
from .state import DecisionContext, GameState
from .types import Action, Rank

__all__ = [
    "Action",
    "BlackjackPayout",
    "CARDS_PER_DECK",
    "Composition",
    "DecisionContext",
    "DoubleRule",
    "GameState",
    "HILO_TAGS",
    "Hand",
    "Rank",
    "Rules",
    "Shoe",
    "hilo_tag",
    "running_count",
    "true_count",
]
