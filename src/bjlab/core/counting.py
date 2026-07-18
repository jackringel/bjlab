"""Card counting: Hi-Lo tags, running/true counts, count-conditioned decks.

Convention: the true count is the running count divided by *exact* decks
remaining (52-card decks, no flooring). Flooring/truncation for bet ramps
and deviation indexes is applied by the consumer (``bjlab.session.BetSpread``
floors; deviation indexes compare against the exact value).
"""

from __future__ import annotations

from typing import Iterable

from .deck import Composition
from .rules import Rules
from .types import Rank

# Hi-Lo: 2-6 -> +1, 7-9 -> 0, ten-valued and aces -> -1. Balanced: the tags
# of a full deck sum to zero (5 ranks x 4 cards x +1 vs. 20 high cards x -1).
HILO_TAGS: dict[Rank, int] = {
    Rank.ACE: -1,
    Rank.TWO: +1,
    Rank.THREE: +1,
    Rank.FOUR: +1,
    Rank.FIVE: +1,
    Rank.SIX: +1,
    Rank.SEVEN: 0,
    Rank.EIGHT: 0,
    Rank.NINE: 0,
    Rank.TEN: -1,
}


def hilo_tag(rank: Rank) -> int:
    """Hi-Lo tag of one card."""
    return HILO_TAGS[rank]


def running_count(cards: Iterable[Rank]) -> int:
    """Hi-Lo running count of a sequence of seen cards."""
    return sum(HILO_TAGS[c] for c in cards)


def true_count(running: float, composition: Composition) -> float:
    """Running count per exact deck remaining."""
    decks = composition.decks_remaining
    if decks <= 0:
        raise ValueError("no cards remaining; true count is undefined")
    return running / decks


def composition_for_true_count(rules: Rules, tc: float) -> Composition:
    """Expected remaining composition given only a Hi-Lo true count. (Planned.)

    Sketch: start from the fresh-shoe composition and shift expected mass so
    that low cards (2-6) are depleted relative to tens/aces by ``tc`` net
    Hi-Lo tags per remaining deck, distributing the shift proportionally
    within each tag group (the 0-tag ranks 7-9 keep their fresh-shoe share).
    This is the prior Layer 2 uses to re-derive strategy at each count and
    extract deviations. Note the result is an *expected* (fractional)
    composition; the exact-count invariant of ``Composition`` may need a
    float-valued sibling type when this is implemented.
    """
    raise NotImplementedError
