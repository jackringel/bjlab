import math

import pytest

from bjlab.session import BetSpread, kelly_fraction, n0, risk_of_ruin


def test_kelly_fraction():
    assert kelly_fraction(0.01, 1.3) == pytest.approx(0.01 / 1.3)
    assert kelly_fraction(-0.005, 1.3) == 0.0  # never bet a negative edge
    with pytest.raises(ValueError):
        kelly_fraction(0.01, 0)


def test_risk_of_ruin_closed_form():
    # exp(-2 * ev * B / var): ev=1, B=1000, var=2000 -> exp(-1)
    assert risk_of_ruin(1000, 1, 2000) == pytest.approx(math.exp(-1))


def test_risk_of_ruin_edges():
    assert risk_of_ruin(0, 1, 1) == 1.0
    assert risk_of_ruin(1000, 0, 1) == 1.0
    assert risk_of_ruin(1000, -1, 1) == 1.0
    with pytest.raises(ValueError):
        risk_of_ruin(1000, 1, 0)


def test_risk_of_ruin_monotone_in_bankroll():
    assert risk_of_ruin(10_000, 5, 13_000) < risk_of_ruin(5_000, 5, 13_000)


def test_n0():
    assert n0(1, 100) == 100
    assert n0(0.005, 1.3) == pytest.approx(1.3 / 0.005**2)
    with pytest.raises(ValueError):
        n0(0, 1)
    with pytest.raises(ValueError):
        n0(1, 0)


def test_bet_spread_step_function():
    spread = BetSpread({0: 0, 1: 25, 2: 50, 4: 100})
    assert spread.bet_for(-3) == 0      # clamped below
    assert spread.bet_for(0.9) == 0     # floors to 0
    assert spread.bet_for(1.0) == 25
    assert spread.bet_for(1.9) == 25
    assert spread.bet_for(2.0) == 50
    assert spread.bet_for(3.7) == 50    # no key at 3 -> largest key <= 3
    assert spread.bet_for(4.0) == 100
    assert spread.bet_for(10) == 100    # clamped above


def test_bet_spread_validation():
    with pytest.raises(ValueError):
        BetSpread({})
    with pytest.raises(ValueError):
        BetSpread({1: -5})
