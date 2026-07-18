"""Action EVs for a single decision point -- the heart of Layer 1."""

from __future__ import annotations

from dataclasses import dataclass

from ..core import Action, DecisionContext
from ..store import Store


@dataclass(frozen=True, slots=True)
class ActionEVs:
    """EV of each action in units of the initial bet.

    ``None`` marks an action that is illegal in the spot being priced.
    DOUBLE and SPLIT include the extra stake in their EV.
    """

    stand: float | None = None
    hit: float | None = None
    double: float | None = None
    split: float | None = None
    surrender: float | None = None

    def as_dict(self) -> dict[Action, float]:
        """Legal actions only. Iteration order is declaration order, which
        also serves as the tie-break order for ``optimal``."""
        pairs = {
            Action.STAND: self.stand,
            Action.HIT: self.hit,
            Action.DOUBLE: self.double,
            Action.SPLIT: self.split,
            Action.SURRENDER: self.surrender,
        }
        return {a: ev for a, ev in pairs.items() if ev is not None}

    @property
    def optimal(self) -> Action:
        """The max-EV legal action."""
        d = self.as_dict()
        if not d:
            raise ValueError("no legal actions were priced")
        return max(d, key=d.__getitem__)

    @property
    def optimal_ev(self) -> float:
        return self.as_dict()[self.optimal]


def action_evs(ctx: DecisionContext, store: Store | None = None) -> ActionEVs:
    """Price every legal action in ``ctx``. (Planned.)

    Memoized recursion over the player-state DAG:

    - STAND: settle ``ctx.hand.best_total`` against
      ``dealer_distribution(ctx.upcard, ctx.composition, ctx.rules)``.
    - HIT: sum over next ranks r of ``p(r) * EV(optimal play of hand+r)``,
      with the composition updated by that removal.
    - DOUBLE: one card, forced stand, payoff doubled.
    - SPLIT: two child hands, each dealt one card from the (updated)
      composition; respects das / rsa / hit_split_aces /
      max_hands_after_splits via child DecisionContexts.
    - SURRENDER: -0.5.

    Results are cached in ``store`` keyed by
    ``(rules.stable_id(), composition, hand, upcard, spot flags)``.
    """
    raise NotImplementedError
