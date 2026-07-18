"""Command-line interface. Subcommands mirror the layer stack:

    bjlab ev          price one hand vs one upcard        (Layer 1)
    bjlab strategy    basic-strategy chart for a ruleset  (Layer 2)
    bjlab deviations  deviation chart for a ruleset       (Layer 2)
    bjlab sim         Monte Carlo shoe simulation         (Layer 3)
    bjlab session     bankroll math from sim output       (Layer 4)

Every subcommand is currently a stub that documents its intended interface;
handlers land as their layers are implemented.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__

_MODULE_FOR = {
    "ev": "bjlab.ev.actions",
    "strategy": "bjlab.strategy.basic",
    "deviations": "bjlab.strategy.deviations",
    "sim": "bjlab.sim.engine",
    "session": "bjlab.session.stats",
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bjlab",
        description="Open, legible blackjack advantage-play lab.",
    )
    parser.add_argument("--version", action="version", version=f"bjlab {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    ev = sub.add_parser("ev", help="EV of each action for one hand vs one upcard (Layer 1)")
    ev.add_argument("--hand", required=True, help='comma-separated cards, e.g. "A,7" or "10,10"')
    ev.add_argument("--upcard", required=True, help='dealer upcard, e.g. "6" or "A"')
    ev.add_argument("--decks", type=int, default=6, help="fresh-shoe decks (default 6)")
    ev.add_argument("--rules", help="path to a Rules JSON file (default: Rules() defaults)")

    st = sub.add_parser("strategy", help="generate or fetch a basic-strategy chart (Layer 2)")
    st.add_argument("--rules", help="path to a Rules JSON file (default: Rules() defaults)")

    dv = sub.add_parser("deviations", help="generate or fetch a deviation chart (Layer 2)")
    dv.add_argument("--rules", help="path to a Rules JSON file (default: Rules() defaults)")

    sm = sub.add_parser("sim", help="run the Monte Carlo shoe sim (Layer 3)")
    sm.add_argument("--rules", help="path to a Rules JSON file (default: Rules() defaults)")
    sm.add_argument("--rounds", type=int, default=1_000_000)
    sm.add_argument("--seed", type=int)

    se = sub.add_parser("session", help="bankroll math from sim output (Layer 4)")
    se.add_argument("--sim", help="path to saved sim results")
    se.add_argument("--bankroll", type=float)
    se.add_argument("--spread", help='true-count->wager map as JSON, e.g. \'{"1": 25, "3": 100}\'')
    se.add_argument("--rounds-per-hour", type=float, default=100.0)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    print(
        f"bjlab {args.command}: not implemented yet -- see {_MODULE_FOR[args.command]} "
        "for the planned behavior",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
