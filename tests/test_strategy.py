import pytest

from bjlab import Action, Hand, Rank, Rules
from bjlab.strategy import StrategyChart


@pytest.fixture
def chart():
    return StrategyChart(
        rules=Rules(),
        table={
            ("pair", 8, Rank.TEN): Action.SPLIT,
            ("soft", 18, Rank.NINE): Action.HIT,
            ("hard", 17, Rank.TEN): Action.STAND,
            ("hard", 20, Rank.SIX): Action.STAND,
        },
    )


def test_pair_lookup(chart):
    hand = Hand.from_cards([Rank.EIGHT, Rank.EIGHT])
    assert chart.lookup(hand, Rank.TEN) is Action.SPLIT


def test_soft_lookup(chart):
    hand = Hand.from_cards([Rank.ACE, Rank.SEVEN])  # soft 18
    assert chart.lookup(hand, Rank.NINE) is Action.HIT


def test_hard_lookup(chart):
    hand = Hand.from_cards([Rank.TEN, Rank.SEVEN])
    assert chart.lookup(hand, Rank.TEN) is Action.STAND


def test_pair_falls_back_to_total(chart):
    # T,T has no pair entry -> falls back to hard 20.
    hand = Hand.from_cards([Rank.TEN, Rank.TEN])
    assert chart.lookup(hand, Rank.SIX) is Action.STAND


def test_missing_entry_raises(chart):
    hand = Hand.from_cards([Rank.TWO, Rank.THREE])
    with pytest.raises(KeyError):
        chart.lookup(hand, Rank.TEN)
