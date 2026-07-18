"""Smoke tests: every module imports, top-level exports exist."""

import importlib
import pkgutil

import bjlab


def test_every_module_imports():
    for mod in pkgutil.walk_packages(bjlab.__path__, "bjlab."):
        importlib.import_module(mod.name)


def test_core_is_globally_accessible():
    from bjlab import (  # noqa: F401
        Action, Composition, DecisionContext, GameState, Hand, Rank, Rules, Shoe,
    )


def test_version():
    assert isinstance(bjlab.__version__, str)
