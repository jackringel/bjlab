"""Dealer-side probabilities.

Every player action ultimately resolves against one distribution: the
dealer's final outcome given the upcard, the remaining composition, and the
rules (H17 vs. S17; peek conditioning).
"""

from __future__ import annotations

from dataclasses import dataclass

from ..core import Composition, Rank, Rules


@dataclass(frozen=True, slots=True)
class DealerDistribution:
    """P(dealer final outcome). Validated to sum to 1.

    ``p_21`` is a multi-card 21; a two-card ace-plus-ten is ``p_blackjack``
    (they pay out differently, so they are tracked separately). In a peek
    game, distributions conditioned on "no blackjack" have ``p_blackjack=0``.
    """

    p_17: float
    p_18: float
    p_19: float
    p_20: float
    p_21: float
    p_blackjack: float
    p_bust: float

    def __post_init__(self) -> None:
        probs = (self.p_17, self.p_18, self.p_19, self.p_20, self.p_21,
                 self.p_blackjack, self.p_bust)
        if any(p < 0 for p in probs):
            raise ValueError("probabilities must be non-negative")
        s = sum(probs)
        if abs(s - 1.0) > 1e-6:
            raise ValueError(f"probabilities must sum to 1, got {s}")

    def p_total(self, total: int) -> float:
        """P(dealer stands on exactly ``total``), excluding blackjack."""
        table = {17: self.p_17, 18: self.p_18, 19: self.p_19,
                 20: self.p_20, 21: self.p_21}
        try:
            return table[total]
        except KeyError:
            raise ValueError(f"dealer standing totals are 17-21; got {total}") from None


def dealer_distribution(
    upcard: Rank, composition: Composition, rules: Rules
) -> DealerDistribution:
    """Exact dealer outcome distribution. (Planned.)

    Recursion over dealer draws from ``composition``: the dealer draws to 17
    (hitting soft 17 iff ``rules.dealer_hits_soft_17``), each draw updating
    the composition. When ``rules.peek`` and the upcard is ten/ace, the
    returned distribution is conditioned on the dealer *not* having
    blackjack (the hand is over before the player acts otherwise).
    """
    raise NotImplementedError
