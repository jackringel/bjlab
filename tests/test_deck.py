import pytest

from bjlab import Composition, Rank


def test_from_decks_counts():
    c = Composition.from_decks(6)
    assert c.total == 312
    assert c.count(Rank.TEN) == 96
    assert c.count(Rank.ACE) == 24
    assert c.count(Rank.FIVE) == 24
    assert c.decks_remaining == 6.0


def test_from_decks_invalid():
    with pytest.raises(ValueError):
        Composition.from_decks(0)


def test_probabilities():
    c = Composition.from_decks(1)
    probs = c.probabilities()
    assert abs(sum(probs.values()) - 1.0) < 1e-12
    assert probs[Rank.TEN] == 16 / 52
    assert probs[Rank.ACE] == 4 / 52


def test_remove_is_pure():
    c = Composition.from_decks(1)
    c2 = c.remove(Rank.TEN)
    assert c.count(Rank.TEN) == 16
    assert c2.count(Rank.TEN) == 15
    assert c2.total == 51
    assert c2.count(Rank.ACE) == 4


def test_remove_exhausted():
    c = Composition.from_decks(1)
    for _ in range(4):
        c = c.remove(Rank.ACE)
    with pytest.raises(ValueError):
        c.remove(Rank.ACE)


def test_empty_composition_cannot_draw():
    empty = Composition(tuple(0 for _ in Rank))
    with pytest.raises(ValueError):
        empty.p(Rank.TEN)


def test_invalid_counts():
    with pytest.raises(ValueError):
        Composition((1, 2, 3))  # wrong length
    with pytest.raises(ValueError):
        Composition(tuple([-1] + [0] * 9))
