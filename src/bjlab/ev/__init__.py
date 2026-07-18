"""Layer 1: exact EV of each action for one hand vs. one upcard.

The unit convention for the whole package is set here: **all EVs are in
units of the initial bet**. DOUBLE and SPLIT EVs already include the extra
stake (a coin-flip double has EV 0.0, not "0.0 per unit wagered"), so the
optimal action is always simply the max EV, and Layer 3/4 can multiply by
the wager without bookkeeping.

Player states form a DAG (each hit adds a card; totals only grow), so the
planned implementation is memoized recursion: price STAND against the dealer
outcome distribution, price HIT as the composition-weighted EV of the
optimal continuation from each successor state, and so on. Results are
cached via ``bjlab.store``.
"""

from .actions import ActionEVs, action_evs
from .dealer import DealerDistribution, dealer_distribution

__all__ = ["ActionEVs", "action_evs", "DealerDistribution", "dealer_distribution"]
