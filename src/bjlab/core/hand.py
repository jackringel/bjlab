"""Immutable hand representation and total math."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

from .types import Rank


@dataclass(frozen=True, slots=True)
class Hand:
    """Immutable player (or dealer) hand. ``add`` returns a new Hand."""

    cards: Tuple[Rank, ...] = ()

    @staticmethod
    def from_cards(cards: Iterable[Rank]) -> "Hand":
        return Hand(tuple(cards))

    def add(self, card: Rank) -> "Hand":
        return Hand(self.cards + (card,))

    @property
    def n_cards(self) -> int:
        return len(self.cards)

    @property
    def is_empty(self) -> bool:
        return len(self.cards) == 0

    @property
    def is_blackjack(self) -> bool:
        """True for a two-card ace-plus-ten. (Whether a post-split 21 counts
        as blackjack is a rules question, decided by the engine, not here.)"""
        if self.n_cards != 2:
            return False
        ranks = set(self.cards)
        return (Rank.ACE in ranks) and (Rank.TEN in ranks)

    @property
    def is_pair(self) -> bool:
        """True if exactly two cards of the same rank."""
        return self.n_cards == 2 and self.cards[0] == self.cards[1]

    @property
    def pair_rank(self) -> Rank | None:
        return self.cards[0] if self.is_pair else None

    @property
    def hard_total(self) -> int:
        """Total counting every ace as 1."""
        return sum(c.hard_value for c in self.cards)

    @property
    def soft_total(self) -> int | None:
        """Total counting one ace as 11, or None if that busts or there is no
        ace. At most one ace can ever count as 11 (two would total 22)."""
        if Rank.ACE not in self.cards:
            return None
        t = self.hard_total + 10
        return t if t <= 21 else None

    @property
    def best_total(self) -> int:
        """Best total <= 21 if possible, else the (busted) hard total."""
        st = self.soft_total
        return st if st is not None else self.hard_total

    @property
    def is_soft(self) -> bool:
        return self.soft_total is not None

    @property
    def is_bust(self) -> bool:
        return self.hard_total > 21
