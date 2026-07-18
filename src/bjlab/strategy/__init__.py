"""Layer 2: strategy charts.

Runs Layer 1 across every spot to produce a ``StrategyChart`` (basic
strategy, fresh-shoe composition) and a ``DeviationChart`` (where the
optimal action flips as the composition shifts with the true count).
Charts are cached by ``rules.stable_id()`` and, once generation is
implemented, validated in tests against published basic strategy and
Illustrious-18 tables.
"""

from .basic import ChartKey, Kind, StrategyChart, generate_basic_strategy
from .deviations import Deviation, DeviationChart, generate_deviations

__all__ = [
    "ChartKey",
    "Kind",
    "StrategyChart",
    "generate_basic_strategy",
    "Deviation",
    "DeviationChart",
    "generate_deviations",
]
