from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple
from .types import Rank

@dataclass(frozen=True, slots=True)
class Hand:
    """Iterable player hand representation"""
    cards: Tuple[Rank,...]=()
    
    @staticmethod
    def from_cards(cards: Iterable[Rank]) -> "Hand":
        return Hand(tuple(cards))
    
    def add(self, card: Rank) -> "Hand":
        return Hand(self.cards+(card,))
        
    @property
    def n_cards(self) -> int:
        return len(self.cards)
        
    @property
    def is_empty(self) -> bool:
        return len(self.cards)==0
    
    @property
    def is_blackjack(self) -> bool:
        """True if 2 cards and 21 val"""
        if self.n_cards!=2:
            return False
        ranks = set(self.cards)
        return (Rank.ACE in ranks) and (Rank.TEN in ranks)
    
    @property
    def is_pair(self) -> bool:
        """True if 2 cards same rank"""
        return self.n_cards == 2 and self.cards[0] == self.cards[1]
    
    @property
    def hard_total(self) ->int:
        """Counts aces as 1"""
        return sum(c.hard_value for c in self.cards)
    
    def soft_total(self) -> int | None:
        """if can be valued at soft (ace counts as 11) return that else none"""
        if Rank.ACE not in self.cards:
            return None
        t = self.hard_total + 10 # #upgrade one ace
        return t if t<=21 else None
    
    @property
    def best_total(self) -> int:
        """Best total <=21 if poss else hard_total"""
        st = self.soft_total
        return st if st is not None else self.hard_total
    
    @property
    def is_soft(self) -> bool:
        return self.soft_total is not None
     
    @property
    def is_bust(self) -> bool:
        return self.hard_total > 21
    
    def pair_rank(self) -> Rank| None:
        if not self.is_pair:
            return None
        return self.cards[0]