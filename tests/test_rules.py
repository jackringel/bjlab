import pytest

from bjlab import Rules


def test_defaults_are_valid():
    Rules()  # validates in __post_init__


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n_decks": 0},
        {"penetration": 1.0},
        {"penetration": 0.0},
        {"early_surrender": True, "late_surrender": True},
        {"max_hands_after_splits": 0},
        {"blackjack_payout": "2_TO_1"},
        {"double_rule": "WHENEVER"},
    ],
)
def test_invalid_rules_raise_on_construction(kwargs):
    with pytest.raises(ValueError):
        Rules(**kwargs)


def test_payout_multiplier():
    assert Rules().bj_payout_multiplier == 1.5
    assert Rules(blackjack_payout="6_TO_5").bj_payout_multiplier == 1.2


def test_to_dict_roundtrip():
    r = Rules(n_decks=2, dealer_hits_soft_17=False)
    assert Rules(**r.to_dict()) == r


def test_stable_id():
    a, b = Rules(), Rules()
    assert a.stable_id() == b.stable_id()
    assert len(a.stable_id()) == 16
    int(a.stable_id(), 16)  # hex
    assert Rules(n_decks=8).stable_id() != a.stable_id()
