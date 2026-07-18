"""Fetch-or-compute persistence.

Every artifact in bjlab is a pure function of its inputs, so each layer
exposes a stable string key for what it makes (e.g.
``f"strategy/basic:{rules.stable_id()}"``) and a JSON-serializable payload.
Stores only move payloads; layers own the dict <-> object conversion.
"""

from .cache import InMemoryStore, JsonStore, Store

__all__ = ["Store", "InMemoryStore", "JsonStore"]
