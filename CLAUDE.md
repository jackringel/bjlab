# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`bjlab` is an open-source blackjack advantage-play simulator: derive optimal
play from first principles (per-action EVs, basic strategy, count deviations),
then simulate play to produce EV/hr, variance, risk of ruin, N0, and optimal
bet spreads. **DESIGN.md is the source of truth for the architecture and the
decisions log — read it before changing structure, and keep it updated when
design conclusions are reached.**

## Commands

```powershell
.venv\Scripts\Activate.ps1        # activate the local Python 3.14 venv
pip install -e ".[dev]"           # editable install + pytest (canonical setup)
pytest                            # run the whole suite
pytest tests/test_hand.py::test_hard_and_soft_totals   # run one test
bjlab --help                      # CLI entry point (subcommands are stubs)
```

Dependencies are declared in `pyproject.toml` (numpy/scipy/matplotlib; pytest
under the `[dev]` extra). `requirements.txt` is just a pinned snapshot of the
dev venv. No linter/formatter is configured yet.

## Architecture

src-layout package; layers depend strictly downward
(`session -> sim -> strategy -> ev -> core`); `store` is a leaf usable by all;
nothing in `core` imports from a layer. See DESIGN.md for the per-layer
algorithms and the conventions that must not be broken (EV units are the
initial bet; `Rank.TEN` aggregates T/J/Q/K; true count is exact, flooring
happens at consumers; core types are frozen dataclasses validated in
`__post_init__`; blackjack is tracked separately from 21; action legality is
the engine's job).

- `src/bjlab/core/` — shared vocabulary: `types` (Action, Rank), `rules`
  (frozen `Rules` + `stable_id()` cache key), `hand`, `deck` (`Composition`,
  `Shoe`), `counting` (Hi-Lo), `state` (`DecisionContext`)
- `src/bjlab/ev/` — Layer 1: dealer outcome distribution + per-action EVs
- `src/bjlab/strategy/` — Layer 2: basic strategy + deviation charts
- `src/bjlab/sim/` — Layer 3: Monte Carlo shoe simulation
- `src/bjlab/session/` — Layer 4: bet spreads, Kelly, risk of ruin, N0
- `src/bjlab/store/` — fetch-or-compute cache (`InMemoryStore`, `JsonStore`)
- `src/bjlab/cli.py` — argparse CLI (`bjlab` console script)

**Implemented and tested**: all of `core`, `store`, and the closed-form
bankroll math in `session` (`BetSpread`, `kelly_fraction`, `risk_of_ruin`,
`n0`). **Stubs** (raise `NotImplementedError`, with the planned algorithm
specified in their docstrings): `dealer_distribution`, `action_evs`,
`generate_basic_strategy`, `generate_deviations`,
`composition_for_true_count`, `Shoe`, `simulate`, `derive_session_stats`,
`optimal_spread`, all CLI subcommand handlers. When implementing a stub,
follow its docstring spec, keep the math documented in-source (see
`session/risk.py` for the template), and check off the DESIGN.md roadmap.

## Conventions for changes

- Tests mirror modules (`tests/test_<module>.py`); every implemented behavior
  gets a test, and stubs have tests asserting `NotImplementedError` — replace
  those when implementing. Layer 2 output must ultimately be validated
  against published basic-strategy tables and the Illustrious 18.
- Keep files ASCII/UTF-8. README.md is read by pip as the package
  description, so it must stay clean UTF-8 (this broke the build once —
  avoid writing files via PowerShell redirection, which emits UTF-16 by
  default).
- License is GPL-3.0-only; `requires-python >= 3.11` even though dev runs
  3.14.
