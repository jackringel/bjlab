"""Count-indexed deviations from basic strategy.

A deviation exists wherever the optimal action under a count-shifted
composition differs from basic strategy. The *index* is the true count at
which the flip happens -- e.g. "16 vs T: STAND at TC >= 0".
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

from ..core import Action, Rules
from ..store import Store
from .basic import ChartKey


@dataclass(frozen=True)
class Deviation:
    """One index play."""

    key: ChartKey
    index: float
    direction: Literal["at_or_above", "at_or_below"]
    action: Action        # what to do when the index triggers
    basic_action: Action  # what basic strategy says otherwise


@dataclass(frozen=True)
class DeviationChart:
    rules: Rules
    deviations: tuple[Deviation, ...]


def generate_deviations(
    rules: Rules,
    true_counts: Sequence[int] = tuple(range(-5, 11)),
    store: Store | None = None,
) -> DeviationChart:
    """Derive (or fetch) the deviation chart for ``rules``. (Planned.)

    For each true count in ``true_counts``, re-derive the optimal action for
    every spot under ``composition_for_true_count(rules, tc)`` and compare
    against basic strategy; the boundary count where the action flips is the
    deviation's index. Validated in tests against the Illustrious 18 once
    implemented.
    """
    raise NotImplementedError
