import pytest

from bjlab import Action, Rank


def test_from_int_covers_all_values():
    assert Rank.from_int(1) is Rank.ACE
    assert Rank.from_int(10) is Rank.TEN
    for v in range(2, 10):
        assert Rank.from_int(v) == v


@pytest.mark.parametrize("bad", [0, 11, -1])
def test_from_int_invalid(bad):
    with pytest.raises(ValueError):
        Rank.from_int(bad)


@pytest.mark.parametrize(
    "label,expected",
    [("A", Rank.ACE), ("a", Rank.ACE), ("10", Rank.TEN), ("T", Rank.TEN),
     ("J", Rank.TEN), ("q", Rank.TEN), ("K", Rank.TEN), ("7", Rank.SEVEN)],
)
def test_from_str(label, expected):
    assert Rank.from_str(label) is expected


@pytest.mark.parametrize("bad", ["x", "11", "1", ""])
def test_from_str_invalid(bad):
    with pytest.raises(ValueError):
        Rank.from_str(bad)


def test_hard_value():
    assert Rank.ACE.hard_value == 1
    assert Rank.TEN.hard_value == 10
    assert Rank.FIVE.hard_value == 5


def test_is_ten_value():
    assert Rank.TEN.is_ten_value
    assert not Rank.NINE.is_ten_value
    assert not Rank.ACE.is_ten_value


def test_actions_are_strings():
    assert Action.HIT == "HIT"
    assert len(Action) == 5
