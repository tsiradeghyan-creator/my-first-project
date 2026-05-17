"""Paper trading simulator — fake money, real prices."""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

import yfinance as yf


STATE_FILE = Path(__file__).parent / "portfolio.json"


@dataclass
class Position:
    symbol: str
    quantity: float
    avg_price: float


@dataclass
class Trade:
    timestamp: str
    symbol: str
    side: str
    quantity: float
    price: float
    pnl: float = 0.0


@dataclass
class Portfolio:
    cash: float = 1000.0
    positions: dict[str, Position] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)

    @classmethod
    def load(cls) -> "Portfolio":
        if not STATE_FILE.exists():
            return cls()
        data = json.loads(STATE_FILE.read_text())
        positions = {s: Position(**p) for s, p in data.get("positions", {}).items()}
        trades = [Trade(**t) for t in data.get("trades", [])]
        return cls(cash=data["cash"], positions=positions, trades=trades)

    def save(self) -> None:
        data = {
            "cash": self.cash,
            "positions": {s: asdict(p) for s, p in self.positions.items()},
            "trades": [asdict(t) for t in self.trades],
        }
        STATE_FILE.write_text(json.dumps(data, indent=2))

    def price(self, symbol: str) -> float:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            raise ValueError(f"No price data for {symbol}")
        return float(data["Close"].iloc[-1])

    def buy(self, symbol: str, quantity: float) -> None:
        price = self.price(symbol)
        cost = price * quantity
        if cost > self.cash:
            raise ValueError(f"Not enough cash: need ${cost:.2f}, have ${self.cash:.2f}")
        self.cash -= cost
        if symbol in self.positions:
            pos = self.positions[symbol]
            total_qty = pos.quantity + quantity
            pos.avg_price = (pos.avg_price * pos.quantity + price * quantity) / total_qty
            pos.quantity = total_qty
        else:
            self.positions[symbol] = Position(symbol, quantity, price)
        self.trades.append(Trade(datetime.now().isoformat(), symbol, "BUY", quantity, price))
        print(f"BUY  {quantity} {symbol} @ ${price:.2f} (cost ${cost:.2f})")

    def sell(self, symbol: str, quantity: float) -> None:
        if symbol not in self.positions or self.positions[symbol].quantity < quantity:
            raise ValueError(f"Not enough {symbol} to sell")
        price = self.price(symbol)
        pos = self.positions[symbol]
        pnl = (price - pos.avg_price) * quantity
        self.cash += price * quantity
        pos.quantity -= quantity
        if pos.quantity == 0:
            del self.positions[symbol]
        self.trades.append(Trade(datetime.now().isoformat(), symbol, "SELL", quantity, price, pnl))
        print(f"SELL {quantity} {symbol} @ ${price:.2f} (PnL ${pnl:+.2f})")

    def status(self) -> None:
        print(f"\nCash: ${self.cash:.2f}")
        total = self.cash
        if self.positions:
            print("Positions:")
            for sym, pos in self.positions.items():
                cur = self.price(sym)
                value = cur * pos.quantity
                pnl = (cur - pos.avg_price) * pos.quantity
                total += value
                print(f"  {sym}: {pos.quantity} @ avg ${pos.avg_price:.2f} | now ${cur:.2f} | value ${value:.2f} | unreal PnL ${pnl:+.2f}")
        realized = sum(t.pnl for t in self.trades)
        print(f"Total portfolio value: ${total:.2f}")
        print(f"Realized PnL (all time): ${realized:+.2f}")
        print(f"Total trades: {len(self.trades)}")


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="Paper trading simulator")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("reset")
    b = sub.add_parser("buy")
    b.add_argument("symbol")
    b.add_argument("quantity", type=float)
    s = sub.add_parser("sell")
    s.add_argument("symbol")
    s.add_argument("quantity", type=float)

    args = p.parse_args()
    pf = Portfolio.load()

    if args.cmd == "status":
        pf.status()
    elif args.cmd == "reset":
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("Portfolio reset.")
        return
    elif args.cmd == "buy":
        pf.buy(args.symbol.upper(), args.quantity)
    elif args.cmd == "sell":
        pf.sell(args.symbol.upper(), args.quantity)

    pf.save()


if __name__ == "__main__":
    main()
