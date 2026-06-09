# CoinPay — pay anywhere with crypto

A working prototype (MVP) of a **crypto payment platform**: a buyer pays with
crypto, and the app converts the order from its real-world currency
(USD, EUR, JPY, AMD, AED, …) at **live exchange rates**. The merchant is
quoted in the fiat they want; the buyer pays in the coin they hold.

It's a web app on purpose: one codebase runs on **every operating system** —
iPhone (Safari), Android, Windows, Mac, Linux — and can later be wrapped
into native iOS/Android apps (Capacitor, React Native) or a desktop app.

## Run it

No build step. Just serve the `web/` folder:

```bash
cd web
python3 -m http.server 8099
```

Then open `http://localhost:8099` in any browser. On your iPhone, open the
same address (with your computer's IP) in Safari — it works as-is and you
can "Add to Home Screen" to use it like an app.

> Live rates come from the public CoinGecko API, fetched in the browser.
> If the network is unavailable, the app falls back to bundled rates and
> shows a "Cached rates" badge so it never breaks.

## How it works

- `rates.js` — the conversion core (framework-free, reusable):
  - `getRates()` — live crypto→fiat prices, with offline fallback.
  - `orderToCrypto(items, crypto, rates)` — how much crypto to pay now.
  - `cryptoToFiat(...)` — value the order in any display currency.
- `products.js` — sample catalog; each item priced in its **own** currency.
- `app.js` — shop, cart, live totals, and the payment screen.
- `index.html` / `styles.css` — the UI.

## Path to a real product

This prototype proves the idea. A production version needs, in order:

1. **A real wallet/settlement layer** — generate per-order addresses and
   detect incoming payments (e.g. via a provider like BTCPay Server,
   Coinbase Commerce, or a node + webhook). The `recordSale`/payment step
   in `app.js` is where this plugs in.
2. **A backend** — quotes, order state, rate-locking, and webhooks must
   live on a server you control, not only in the browser.
3. **Legal & compliance** — crypto payments are regulated. Depending on
   country you may need money-transmitter licensing, KYC/AML, and tax
   handling. Get legal advice before taking real money.
4. **Security** — never hold private keys in the frontend; use audited
   custody or non-custodial flows.

## Honest note

No app earns money on its own. This becomes income only when real merchants
and buyers use it and you take a small fee per transaction. Anyone promising
a guaranteed fixed daily income with no work is selling a scam.
