from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Literal, Optional

DoubleRule = Literal["ANY_TWO", "NINE_TEN_ELEVEN", "TEN_ELEVEN", "ELEVEN_ONLY"]
BlackJackPayout = Literal["3_TO_2", "6_TO_5"]

@dataclass(frozen=True, slots=True)
class Rules:
    """
    Table rules configuration.
    -Number of decks
    -H17 vs S17
    -Double after split or not
    -Late surrender or no
    -Doubling rules
    -Number of resplits
    -Resplit aces yes or no
    -Blackjack payout
    -Assume peek enabled
    Initialize with rules for common "good" game
    """
    n_decks: int=6
    penetration: float=0.75 # shuffle 75% of way through
    dealer_hits_soft_17: bool=True # true = H17, false S17
    das: bool=True
    rsa: bool=False
    late_surrender: bool=True
    early_surrender: bool=False
    double_rule: DoubleRule = "ANY_TWO"
    # splits
    max_hands_after_splits: int=4
    hit_split_aces: bool=False
    surrender_after_spplit: bool=False
    blackjack_payout: BlackjackPayout="3_TO_2"
    peek: bool=True
    insurance_offered: bool=True
    
    # ensure compatibility
    def validate(self) -> None:
        if self.n_decks <= 0:
            raise ValueError("n_decks must be positive.")
        if not (0.0 < self.penetration < 1.0):
            raise ValueError("penetration must be in (0, 1).")
        if self.early_surrender and self.late_surrender:
            raise ValueError("Cannot have both early_surrender and late_surrender True.")
        if self.max_hands_after_splits < 1:
            raise ValueError("max_hands_after_splits must be >= 1.")
    
    @property
    def bj_payout_multiplier(self) -> float:
        """Return blackjack payout (profit) multiplier relative to original bet."""
        if self.blackjack_payout == "3_TO_2":
            return 1.5
        if self.blackjack_payout == "6_TO_5":
            return 1.2
        raise ValueError(f"Unknown blackjack_payout: {self.blackjack_payout}")
    
     def to_dict(self) -> dict:
        """Stable dict representation for configs/logging."""
        d = asdict(self)
        # Ensure deterministic ordering if you serialize (json with sort_keys does this too)
        return d

    def stable_id(self) -> str:
        """
        Deterministic short hash of the rules (useful for caching strategy tables).
        """
        payload = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:16]