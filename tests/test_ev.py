import pytest

from bjlab import Action
from bjlab.ev import ActionEVs, DealerDistribution


def test_optimal_action_is_max_ev():
    evs = ActionEVs(stand=-0.54, hit=-0.41, surrender=-0.5)
    assert evs.optimal is Action.HIT
    assert evs.optimal_ev == -0.41
    assert set(evs.as_dict()) == {Action.STAND, Action.HIT, Action.SURRENDER}


def test_illegal_actions_are_excluded():
    evs = ActionEVs(stand=0.1)
    assert evs.as_dict() == {Action.STAND: 0.1}
    assert evs.optimal is Action.STAND


def test_no_priced_actions_raises():
    with pytest.raises(ValueError):
        ActionEVs().optimal


def test_dealer_distribution_validates():
    dd = DealerDistribution(
        p_17=0.14, p_18=0.14, p_19=0.14, p_20=0.18, p_21=0.12,
        p_blackjack=0.05, p_bust=0.23,
    )
    assert dd.p_total(20) == 0.18
    with pytest.raises(ValueError):
        dd.p_total(22)
    with pytest.raises(ValueError):
        DealerDistribution(p_17=1.0, p_18=0.5, p_19=0, p_20=0, p_21=0,
                           p_blackjack=0, p_bust=0)
