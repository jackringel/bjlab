"""Layer 3: Monte Carlo shoe simulation.

Plays full shoes according to a strategy chart (plus deviations), keeping a
Hi-Lo running count and converting to true count, to measure what the exact
layers don't give directly: how often each true count occurs and the
realized per-round EV and variance there. Layer 4 turns that into money.
"""

from .engine import SimConfig, SimResult, TrueCountBucket, simulate

__all__ = ["SimConfig", "SimResult", "TrueCountBucket", "simulate"]
