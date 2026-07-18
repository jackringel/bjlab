"""Basic enums shared by every layer: card ranks and player actions."""

from __future__ import annotations

from enum import Enum, IntEnum


class Action(str, Enum):
    """Player actions.

    Legality in a given spot is decided by the engine from ``Rules`` and
    ``DecisionContext`` (see ``DecisionContext.available_actions``), not by
    the enum itself.
    """

    HIT = "HIT"
    STAND = "STAND"
    DOUBLE = "DOUBLE"
    SPLIT = "SPLIT"
    SURRENDER = "SURRENDER"


class Rank(IntEnum):
    """Card ranks by blackjack value.

    Suits do not matter in blackjack, and neither does the difference between
    10, J, Q, and K; all four are ``TEN``. A single 52-card deck therefore
    holds four cards of each rank ACE..NINE and sixteen TENs.
    """

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10

    @property
    def hard_value(self) -> int:
        """Value counting the ace as 1."""
        return int(self)

    @property
    def is_ten_value(self) -> bool:
        return self is Rank.TEN

    @staticmethod
    def from_int(value: int) -> "Rank":
        """Convert a blackjack value (1-10) to a Rank.

        Face cards must already be mapped to 10 before calling.
        """
        if 1 <= value <= 10:
            return Rank(value)
        raise ValueError(f"Invalid rank int: {value}")

    @staticmethod
    def from_str(label: str) -> "Rank":
        """Parse a card label: 'A', '2'..'9', '10', 'T', 'J', 'Q', or 'K'
        (case-insensitive)."""
        u = label.strip().upper()
        if u in ("A", "ACE"):
            return Rank.ACE
        if u in ("10", "T", "J", "Q", "K"):
            return Rank.TEN
        if u.isdigit() and 2 <= int(u) <= 9:
            return Rank(int(u))
        raise ValueError(f"Unrecognized card label: {label!r}")
