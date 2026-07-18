"""Deck compositions: what is left to be dealt.

Layer 1 conditions its exact math on a ``Composition``; Layer 2 derives
deviations by re-running Layer 2 under count-shifted compositions (see
``bjlab.core.counting.composition_for_true_count``); Layer 3 deals from a
``Shoe`` that owns a mutable composition plus penetration bookkeeping.
"""

from __future__ import annotations

from dataclasses import dataclass

from .types import Rank

CARDS_PER_DECK = 52

# Per 52-card deck: four of each rank ACE..NINE, sixteen ten-valued cards.
_PER_DECK = {rank: (16 if rank is Rank.TEN else 4) for rank in Rank}


@dataclass(frozen=True, slots=True)
class Composition:
    """Immutable multiset of undealt cards, counted per ``Rank``.

    ``counts[i]`` is the number of remaining cards of ``Rank(i + 1)``
    (index 0 = aces, index 9 = ten-valued cards).
    """

    counts: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.counts) != len(Rank):
            raise ValueError(f"counts must have {len(Rank)} entries, got {len(self.counts)}")
        if any(c < 0 for c in self.counts):
            raise ValueError("counts must be non-negative")

    @staticmethod
    def from_decks(n_decks: int) -> "Composition":
        """Fresh shoe of ``n_decks`` 52-card decks."""
        if n_decks < 1:
            raise ValueError("n_decks must be >= 1")
        return Composition(tuple(_PER_DECK[r] * n_decks for r in Rank))

    @property
    def total(self) -> int:
        """Number of undealt cards."""
        return sum(self.counts)

    @property
    def decks_remaining(self) -> float:
        """Exact decks remaining (total / 52), no rounding."""
        return self.total / CARDS_PER_DECK

    def count(self, rank: Rank) -> int:
        return self.counts[rank - 1]

    def p(self, rank: Rank) -> float:
        """Probability that the next card dealt is ``rank``."""
        total = self.total
        if total == 0:
            raise ValueError("cannot draw from an empty composition")
        return self.count(rank) / total

    def probabilities(self) -> dict[Rank, float]:
        """Draw probability of every rank; values sum to 1."""
        return {r: self.p(r) for r in Rank}

    def remove(self, rank: Rank) -> "Composition":
        """New composition with one card of ``rank`` dealt out."""
        if self.count(rank) == 0:
            raise ValueError(f"no {rank.name} left to remove")
        idx = rank - 1
        return Composition(
            tuple(c - 1 if i == idx else c for i, c in enumerate(self.counts))
        )


class Shoe:
    """Mutable dealing shoe for Layer 3 simulation. (Planned.)

    Will own an RNG, deal cards by mutating an internal ``Composition``,
    track the running count and penetration, and reshuffle per ``Rules``.
    The Layer 3 engine (``bjlab.sim``) drives it; nothing below Layer 3
    should ever need one.
    """

    def __init__(self, rules, seed: int | None = None) -> None:
        raise NotImplementedError("Shoe is built alongside bjlab.sim (Layer 3)")
