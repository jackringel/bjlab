"""Decision and game state.

``DecisionContext`` is the complete input to Layer 1: everything that
determines the EV of each action for one hand at one moment. ``GameState``
will be the Layer 3 engine's mutable table state.
"""

from __future__ import annotations

from dataclasses import dataclass

from .deck import Composition
from .hand import Hand
from .rules import Rules
from .types import Action, Rank


@dataclass(frozen=True, slots=True)
class DecisionContext:
    """One decision point, fully specified.

    Attributes:
        hand: The player's current hand.
        upcard: The dealer's exposed card.
        composition: Cards still undealt *from this decision's viewpoint*
            (i.e. with the hand's cards and the upcard already removed).
        rules: Table rules.
        splits_so_far: Splits already made by this seat this round.
        is_split_hand: This hand came from a split (gates DAS, resplits,
            surrender_after_split).
        is_split_aces: This hand is a split ace (gates hit_split_aces, RSA).
    """

    hand: Hand
    upcard: Rank
    composition: Composition
    rules: Rules
    splits_so_far: int = 0
    is_split_hand: bool = False
    is_split_aces: bool = False

    def available_actions(self) -> frozenset[Action]:
        """Legal actions in this spot. (Planned.)

        Will encode: HIT/STAND almost always; DOUBLE only on two cards
        satisfying ``rules.double_rule`` (and ``rules.das`` if a split hand);
        SPLIT only on pairs under ``rules.max_hands_after_splits`` (and
        ``rules.rsa`` for aces); SURRENDER only on the original two cards per
        the surrender rules; one-card-only on split aces unless
        ``rules.hit_split_aces``.
        """
        raise NotImplementedError


class GameState:
    """Mutable round state for the Layer 3 engine. (Planned.)

    Will hold the shoe, each seat's hands and bets, the dealer's hand, and
    the running count. Deliberately unspecified until the engine exists --
    ``bjlab.sim`` owns its lifecycle and will define what it needs.
    """
