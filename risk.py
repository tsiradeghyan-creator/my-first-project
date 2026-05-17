"""Position sizing calculator — how much to risk per trade."""
from __future__ import annotations

import argparse


def position_size(account: float, risk_pct: float, entry: float, stop: float) -> dict:
    if entry == stop:
        raise ValueError("Entry and stop cannot be equal")
    risk_amount = account * (risk_pct / 100)
    risk_per_share = abs(entry - stop)
    shares = risk_amount / risk_per_share
    position_value = shares * entry
    return {
        "risk_amount": risk_amount,
        "risk_per_share": risk_per_share,
        "shares": shares,
        "position_value": position_value,
        "position_pct": position_value / account * 100,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Calculate position size for a trade")
    p.add_argument("--account", type=float, required=True, help="Total account size in $")
    p.add_argument("--risk", type=float, default=1.0, help="Risk %% per trade (default 1%%)")
    p.add_argument("--entry", type=float, required=True, help="Entry price")
    p.add_argument("--stop", type=float, required=True, help="Stop-loss price")
    args = p.parse_args()

    r = position_size(args.account, args.risk, args.entry, args.stop)
    print(f"\nAccount:         ${args.account:.2f}")
    print(f"Risk per trade:  {args.risk}% = ${r['risk_amount']:.2f}")
    print(f"Entry → Stop:    ${args.entry} → ${args.stop} (${r['risk_per_share']:.2f}/share)")
    print(f"Shares to buy:   {r['shares']:.2f}")
    print(f"Position value:  ${r['position_value']:.2f} ({r['position_pct']:.1f}% of account)")
    print(f"\nIf stop hits, you lose ${r['risk_amount']:.2f} — no more.")


if __name__ == "__main__":
    main()
