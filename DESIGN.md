# bjlab design

This document records the architecture and the decisions behind it. It is the
source of truth for *why* the code is shaped the way it is; keep it current
when the design changes.

## Motivation

Commercial advantage-play software (CVCX and friends) computes EV/hr,
variance, risk of ruin, N0, and optimal bet spreads; but it is expensive and
a black box. bjlab is the open, legible alternative: derive optimal play from
first principles, then simulate playing it under configurable conditions to
produce those same numbers, with every formula visible and documented.

Three principles drive everything:

1. **Legible math.** Every probability and formula is documented where it is
   computed (see `session/risk.py` for the template: formula, assumptions,
   reference). Reading the source should double as reading the derivation.
2. **Every layer is independently usable.** Price one hand, print a strategy
   chart, run a sim, or just plug external numbers into the bankroll
   formulas; no layer requires driving the whole stack.
3. **Fetch-or-compute everywhere.** Every artifact is a pure function of its
   inputs, so everything is cacheable by a stable key and recomputed only
   when missing. Users can always ask for a result and get it from cache or
   from a fresh computation transparently.

## The layer stack

| Layer | Package | Input | Output |
|---|---|---|---|
| core | `bjlab.core` | — | Shared vocabulary: `Rules`, `Rank`, `Hand`, `Composition`, Hi-Lo counting, `DecisionContext` |
| 1 | `bjlab.ev` | one `DecisionContext` (hand, upcard, composition, rules, spot flags) | EV of each legal action (`ActionEVs`), dealer outcome distribution |
| 2 | `bjlab.strategy` | `Rules` (+ count-shifted compositions) | `StrategyChart` (basic strategy), `DeviationChart` (index plays) |
| 3 | `bjlab.sim` | `Rules` + charts | `SimResult`: per-true-count frequency, EV, variance (Monte Carlo) |
| 4 | `bjlab.session` | `SimResult` + `BetSpread` + bankroll + speed | EV/hand, EV/hr, variance, risk of ruin, N0; reverse: optimal (Kelly) spreads |
| — | `bjlab.store` | string key | fetch-or-compute cache used by all layers |

Layers depend strictly downward (`session → sim → strategy → ev → core`);
`store` is a leaf utility importable by all. Nothing in `core` imports from a
layer.

### Layer 1: action EVs (`bjlab.ev`)

Player states form a DAG (hits only add cards; totals only grow), so action
EVs come from **memoized recursion**:

- STAND settles the hand's best total against the dealer outcome
  distribution (`ev/dealer.py`), which is itself an exact recursion over
  dealer draws from the composition (H17/S17 per rules, conditioned on "no
  dealer blackjack" in peek games).
- HIT is the composition-weighted average over next cards of the EV of
  *optimal play* from each successor state (which recursively reuses Layer 1).
- DOUBLE is one card + forced stand at doubled stakes.
- SPLIT spawns child hands, each dealt one card, gated by DAS / RSA /
  hit-split-aces / max-hands rules via child `DecisionContext`s.
- SURRENDER is −0.5.

Card removal matters: every draw updates the `Composition` the next
probability is computed from. This is what makes deck count and count-shifted
priors flow through the whole stack for free.

### Layer 2: strategy charts (`bjlab.strategy`)

Basic strategy = run Layer 1 over every spot (hard 5–21, soft 13–21, all
pairs × all upcards) at a fresh-shoe composition and record the argmax
action. Deviations = repeat under `composition_for_true_count(rules, tc)`
for a range of counts; wherever the optimal action flips, record the boundary
count as the deviation's **index** (e.g. "16 vs T: STAND at TC ≥ 0").

Validation strategy: once generation works, tests compare output against
published basic-strategy tables and the Illustrious 18.

### Layer 3: simulation (`bjlab.sim`)

The exact layers can't cheaply give the *distribution of table states over
time* — how often each true count occurs under given penetration, and the
realized EV/variance there. That is measured by Monte Carlo: deal shoes, play
every hand per the Layer 2 charts with Hi-Lo counting and true-count
conversion, bucket each round by the floored true count at bet time.
`TrueCountBucket` stats are per one-unit flat bet; bet sizing is applied
later so one sim serves many spreads.

### Layer 4: session/bankroll math (`bjlab.session`)

Combines sim buckets with a `BetSpread` (a step function of floored true
count; 0 = wong out) and table speed to produce `SessionStats`. Closed forms
used (all documented in-source with assumptions):

- Kelly fraction: `f* = EV / Var` per round (`betting.py`).
- Risk of ruin: `RoR = exp(−2·EV·B / Var)` — diffusion approximation
  (`risk.py`; reference: Schlesinger, *Blackjack Attack*).
- N0: `Var / EV²` rounds (`risk.py`).
- Overall variance across counts via the law of total variance (`stats.py`).

The reverse direction — derive an optimal spread from bankroll + sim results
via (fractional) Kelly, respecting betting increments and max bet — lives in
`betting.optimal_spread`.

**"Layer 5" was folded into Layer 4**: rather than a separate
overall-vs-session bankroll layer, there is one bankroll and spreads are
sized session by session against it.

### Caching (`bjlab.store`)

The fetch-or-compute pattern is uniform: `store.get_or_compute(key, compute)`.
Keys are stable strings built from the inputs — `Rules.stable_id()` (a
sha256 of the sorted-JSON ruleset, 16 hex chars) anchors every key, plus
layer-specific parts (composition, hand, upcard, spot flags for Layer 1;
n_rounds/seed/chart ids for Layer 3). Stores move JSON payloads only; each
layer owns its object↔dict serialization. `JsonStore` hashes keys into
filenames (Windows forbids `:` in paths); `InMemoryStore` backs tests.

## Conventions (important! breaking these breaks the stack)

- **EV units**: all EVs are in units of the *initial* bet. DOUBLE and SPLIT
  EVs already include the extra stake, so "optimal = max EV" holds with no
  bookkeeping, and Layers 3/4 scale by the wager directly.
- **Ranks**: `Rank.TEN` aggregates 10/J/Q/K; suits don't exist. A deck is 4
  of each of A–9 plus 16 tens. `Rank` is an IntEnum with ACE = 1.
- **True count** = running count / *exact* decks remaining (no flooring).
  Flooring happens at the consumer: `BetSpread.bet_for` floors; deviation
  indexes compare exact values.
- **Immutability in core**: `Rules`, `Hand`, `Composition`,
  `DecisionContext` are frozen dataclasses; transitions (`Hand.add`,
  `Composition.remove`) return new objects. Validation runs in
  `__post_init__` so invalid objects cannot exist.
- **Blackjack tracked separately from 21**: dealer/player two-card 21 pays
  differently, so `DealerDistribution` carries `p_blackjack` apart from
  `p_21`, and `Hand.is_blackjack` requires exactly two cards.
- **Action legality is the engine's job** (rules + spot flags), never the
  enum's or the chart's.

## Decisions log

- **2026-07-17** Restored the pre-wipe core (`types`/`rules`/`hand`) with
  fixes: `soft_total` is now a property (it was called as one but defined as
  a method, silently corrupting `best_total`/`is_soft`), `BlackjackPayout`
  casing unified, `surrender_after_split` typo fixed, `Rules` now
  auto-validates on construction.
- **2026-07-17** GPLv3 (restored from the pre-wipe repo — the license
  deletion in the environment-revamp commit looked incidental).
- **2026-07-17** src-layout + setuptools + pyproject only; `requires-python
  >= 3.11` even though dev runs 3.14, for open-source reach.
- **2026-07-17** Layer packages named by role (`ev`, `strategy`, `sim`,
  `session`) rather than `layer1..4`; the mapping is documented here and in
  each package docstring.
- **2026-07-17** Stubs raise `NotImplementedError` and carry docstrings
  specifying the planned algorithm — the spec lives in the code, not in
  chat logs. Implemented vs. planned status is tracked in CLAUDE.md.
- **2026-07-17** `composition_for_true_count` will likely need a
  float-valued sibling of `Composition` (expected compositions are
  fractional); noted in its docstring, deferred until Layer 2.

## Roadmap

- [ ] `dealer_distribution`: exact dealer recursion (H17/S17, peek).
- [ ] `action_evs`: memoized player recursion; `DecisionContext.available_actions`.
- [ ] `generate_basic_strategy` + tests against published charts.
- [ ] `composition_for_true_count` + `generate_deviations` + tests against
      the Illustrious 18.
- [ ] `Shoe` + `simulate` (Monte Carlo, seeded, cached).
- [ ] `derive_session_stats` + `optimal_spread` (fractional Kelly, increments).
- [ ] Chart/data plotting (matplotlib) and pretty chart printing in the CLI.
- [ ] Wire CLI handlers as each layer lands.
