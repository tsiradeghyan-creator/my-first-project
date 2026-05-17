"""Backtest a simple moving-average crossover strategy on historical data."""
from __future__ import annotations

import argparse

import yfinance as yf


def backtest(symbol: str, period: str, fast: int, slow: int, capital: float) -> None:
    data = yf.download(symbol, period=period, interval="1d", auto_adjust=True, progress=False)
    if data.empty:
        print(f"No data for {symbol}")
        return

    close = data["Close"].squeeze()
    data["fast"] = close.rolling(fast).mean()
    data["slow"] = close.rolling(slow).mean()
    data = data.dropna()

    cash = capital
    shares = 0.0
    trades = 0
    wins = 0
    entry_price = 0.0

    for i in range(1, len(data)):
        prev = data.iloc[i - 1]
        cur = data.iloc[i]
        price = float(cur["Close"])
        prev_fast, prev_slow = float(prev["fast"]), float(prev["slow"])
        cur_fast, cur_slow = float(cur["fast"]), float(cur["slow"])

        # Golden cross — buy
        if prev_fast <= prev_slow and cur_fast > cur_slow and shares == 0:
            shares = cash / price
            entry_price = price
            cash = 0
            trades += 1
        # Death cross — sell
        elif prev_fast >= prev_slow and cur_fast < cur_slow and shares > 0:
            cash = shares * price
            if price > entry_price:
                wins += 1
            shares = 0

    final = cash + shares * float(data.iloc[-1]["Close"])
    pnl = final - capital
    pct = (final / capital - 1) * 100
    win_rate = (wins / trades * 100) if trades else 0

    buy_hold = capital * (float(data.iloc[-1]["Close"]) / float(data.iloc[0]["Close"]))

    print(f"\nBacktest: {symbol} | {period} | MA({fast}/{slow})")
    print(f"Starting capital: ${capital:.2f}")
    print(f"Final value:      ${final:.2f}")
    print(f"Strategy PnL:     ${pnl:+.2f} ({pct:+.2f}%)")
    print(f"Buy & hold value: ${buy_hold:.2f} ({(buy_hold/capital-1)*100:+.2f}%)")
    print(f"Trades: {trades} | Win rate: {win_rate:.1f}%")
    if final < buy_hold:
        print("\nNote: simple buy-and-hold beat this strategy. This is COMMON.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", default="SPY")
    p.add_argument("--period", default="2y", help="e.g. 6mo, 1y, 2y, 5y")
    p.add_argument("--fast", type=int, default=20)
    p.add_argument("--slow", type=int, default=50)
    p.add_argument("--capital", type=float, default=1000.0)
    args = p.parse_args()
    backtest(args.symbol.upper(), args.period, args.fast, args.slow, args.capital)


if __name__ == "__main__":
    main()
