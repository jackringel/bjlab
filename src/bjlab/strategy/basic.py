"""Basic-strategy charts: optimal action for every spot under fixed Rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping

from ..core import Action, Hand, Rank, Rules
from ..store import Store

Kind = Literal["hard", "soft", "pair"]

# ("hard", 16, Rank.TEN) -> hard 16 vs ten; ("soft", 18, Rank.NINE) -> A,7
# vs 9; ("pair", 8, Rank.SIX) -> 8,8 vs 6 (pairs keyed by the paired rank's
# int value, aces = 1).
ChartKey = tuple[Kind, int, Rank]


@dataclass(frozen=True)
class StrategyChart:
    """Optimal action per (spot, upcard) under ``rules`` at a fresh-shoe
    composition."""

    rules: Rules
    table: Mapping[ChartKey, Action]

    def lookup(self, hand: Hand, upcard: Rank) -> Action:
        """Chart action for ``hand`` vs ``upcard``.

        Pairs are looked up as pairs first; if the chart has no pair entry
        (a chart that says "never split this"), falls back to the hand's
        soft/hard total.
        """
        if hand.is_pair:
            pair_key: ChartKey = ("pair", int(hand.pair_rank), upcard)
            if pair_key in self.table:
                return self.table[pair_key]
        kind: Kind = "soft" if hand.is_soft else "hard"
        key: ChartKey = (kind, hand.best_total, upcard)
        try:
            return self.table[key]
        except KeyError:
            raise KeyError(f"no chart entry for {kind} {hand.best_total} vs {upcard.name}") from None


def generate_basic_strategy(rules: Rules, store: Store | None = None) -> StrategyChart:
    """Derive (or fetch, keyed by ``rules.stable_id()``) the basic-strategy
    chart. (Planned.)

    Enumerates every spot -- hard totals 5-21, soft totals 13-21, all pairs
    -- against every upcard, builds the DecisionContext at a fresh-shoe
    composition (minus the visible cards), calls Layer 1's ``action_evs``,
    and records the optimal action.
    """
    raise NotImplementedError
