from __future__ import annotations

from enum import Enum, IntEnum


class Action(str, Enum):
    """Player actions, engine decides legality based on state/rules"""
    HIT = "HIT"
    STAND = "STAND"
    DOUBLE = "DOUBLE"
    SPLIT = "SPLIT"
    SURRENDER = "SURRENDER"


class Rank(IntEnum):
    """Card rankings."""
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
        """Hard val - ace=1"""
        return 1 if self is Rank.ACE else int(self)
    
    @property
    def is_ten_value(self) -> bool:
        return self is Rank.TEN
    
    @staticmethod
    def from_int(value:int) -> "Rank":
        """Convert number to Rank. Face cards must be mapped to TEN before calling"""
        if value==1:
            return Rank.ACE
        if 2<=value<=9:
            return Rank(value)
        if value==10:
            return Rank.TEN
        raise ValueError(f"Invalid rank int: {value}")