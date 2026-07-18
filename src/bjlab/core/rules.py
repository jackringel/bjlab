"""Table-rules configuration.

``Rules`` is the immutable set of rules for how a game is dealt and
paid. Each stack section - action EVs (Layer 1), strategy
and deviation charts (Layer 2), simulation results (Layer 3) - is a
function of a ``Rules`` instance + a deck composition, which is why
``stable_id()`` exists: it gives a deterministic cache key for all of them.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Literal, get_args

DoubleRule = Literal["ANY_TWO", "NINE_TEN_ELEVEN", "TEN_ELEVEN", "ELEVEN_ONLY"]
BlackjackPayout = Literal["3_TO_2", "6_TO_5"]


@dataclass(frozen=True, slots=True)
class Rules:
    """Immutable table rules. Validated on construction.

    Defaults describe a common "good" game: 6 decks, 75% penetration, H17,
    DAS, late surrender, 3:2 blackjacks.

    Attributes:
        n_decks: Shoe size in 52-card decks.
        penetration: Fraction of the shoe dealt before reshuffling, in (0, 1).
        dealer_hits_soft_17: True = H17, False = S17.
        das: Doubling allowed after a split.
        rsa: Resplitting aces allowed.
        late_surrender: Surrender offered after the dealer checks for blackjack.
        early_surrender: Surrender offered before the dealer checks.
            Mutually exclusive with ``late_surrender``.
        double_rule: Which two-card totals may be doubled.
        max_hands_after_splits: Total hands one seat may end up with
            (4 means up to 3 splits).
        hit_split_aces: Split aces may draw more than one card.
        surrender_after_split: Surrender allowed on post-split hands.
        blackjack_payout: "3_TO_2" (pays 1.5x) or "6_TO_5" (pays 1.2x).
        peek: Dealer checks for blackjack under a ten or ace before play.
        insurance_offered: Insurance offered when the upcard is an ace.
    """

    n_decks: int = 6
    penetration: float = 0.75
    dealer_hits_soft_17: bool = True
    das: bool = True
    rsa: bool = False
    late_surrender: bool = True
    early_surrender: bool = False
    double_rule: DoubleRule = "ANY_TWO"
    max_hands_after_splits: int = 4
    hit_split_aces: bool = False
    surrender_after_split: bool = False
    blackjack_payout: BlackjackPayout = "3_TO_2"
    peek: bool = True
    insurance_offered: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Raise ValueError on any incoherent combination."""
        if self.n_decks <= 0:
            raise ValueError("n_decks must be positive.")
        if not (0.0 < self.penetration < 1.0):
            raise ValueError("penetration must be in (0, 1).")
        if self.early_surrender and self.late_surrender:
            raise ValueError("early_surrender and late_surrender are mutually exclusive.")
        if self.max_hands_after_splits < 1:
            raise ValueError("max_hands_after_splits must be >= 1.")
        if self.double_rule not in get_args(DoubleRule):
            raise ValueError(f"Unknown double_rule: {self.double_rule!r}")
        if self.blackjack_payout not in get_args(BlackjackPayout):
            raise ValueError(f"Unknown blackjack_payout: {self.blackjack_payout!r}")

    @property
    def bj_payout_multiplier(self) -> float:
        """Blackjack profit multiplier relative to the initial bet."""
        return {"3_TO_2": 1.5, "6_TO_5": 1.2}[self.blackjack_payout]

    def to_dict(self) -> dict:
        """JSON-ready dict; round-trips via ``Rules(**rules.to_dict())``."""
        return asdict(self)

    def stable_id(self) -> str:
        """Deterministic 16-hex-char id of this ruleset, used as a cache key
        for every artifact derived from it (strategy charts, sims, ...)."""
        payload = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
