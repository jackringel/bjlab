import pytest

from bjlab import Composition, Rank, Rules, hilo_tag, running_count, true_count
from bjlab.core.counting import HILO_TAGS, composition_for_true_count


def test_hilo_is_balanced():
    # A full deck's tags sum to zero.
    per_deck = {r: (16 if r is Rank.TEN else 4) for r in Rank}
    assert sum(HILO_TAGS[r] * n for r, n in per_deck.items()) == 0


def test_tags():
    assert hilo_tag(Rank.TWO) == 1
    assert hilo_tag(Rank.SIX) == 1
    assert hilo_tag(Rank.SEVEN) == 0
    assert hilo_tag(Rank.NINE) == 0
    assert hilo_tag(Rank.TEN) == -1
    assert hilo_tag(Rank.ACE) == -1


def test_running_count():
    assert running_count([Rank.TWO, Rank.TEN, Rank.ACE, Rank.FIVE]) == 0
    assert running_count([Rank.TWO, Rank.THREE, Rank.SEVEN]) == 2


def test_true_count_exact_decks():
    three_decks = Composition.from_decks(3)
    assert true_count(6, three_decks) == 2.0
    assert true_count(-3, Composition.from_decks(6)) == -0.5


def test_true_count_empty_shoe():
    empty = Composition(tuple(0 for _ in Rank))
    with pytest.raises(ValueError):
        true_count(1, empty)


def test_composition_for_true_count_is_planned():
    with pytest.raises(NotImplementedError):
        composition_for_true_count(Rules(), 2.0)
