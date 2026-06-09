// rates.js — the conversion core of the platform.
// Fetches live crypto prices in many fiat currencies and converts a
// fiat-priced order into the crypto amount a buyer must pay right now.
//
// This module is intentionally framework-free so it can be reused by a
// web app, a React Native / Flutter mobile app, or a backend later.

export const CRYPTOS = {
  bitcoin:     { symbol: "BTC",  name: "Bitcoin" },
  ethereum:    { symbol: "ETH",  name: "Ethereum" },
  tether:      { symbol: "USDT", name: "Tether" },
  "usd-coin":  { symbol: "USDC", name: "USD Coin" },
  binancecoin: { symbol: "BNB",  name: "BNB" },
  solana:      { symbol: "SOL",  name: "Solana" },
};

export const FIATS = ["usd", "eur", "gbp", "jpy", "rub", "amd", "aed", "try"];

// Fallback rates: price of 1 unit of crypto in each fiat. Used only when the
// live API can't be reached, so the app never shows a broken screen.
// These are approximate and clearly flagged as stale in the UI.
const FALLBACK = {
  bitcoin:     { usd: 65000, eur: 60000, gbp: 51000, jpy: 9800000, rub: 6000000, amd: 25200000, aed: 238000, try: 2100000 },
  ethereum:    { usd: 3400,  eur: 3140,  gbp: 2670,  jpy: 512000,  rub: 314000,  amd: 1318000,  aed: 12480,  try: 110000 },
  tether:      { usd: 1,     eur: 0.92,  gbp: 0.78,  jpy: 150,     rub: 92,      amd: 387,      aed: 3.67,   try: 32 },
  "usd-coin":  { usd: 1,     eur: 0.92,  gbp: 0.78,  jpy: 150,     rub: 92,      amd: 387,      aed: 3.67,   try: 32 },
  binancecoin: { usd: 580,   eur: 535,   gbp: 455,   jpy: 87000,   rub: 53000,   amd: 224000,  aed: 2130,   try: 18700 },
  solana:      { usd: 150,   eur: 138,   gbp: 118,   jpy: 22500,   rub: 13800,   amd: 58000,   aed: 550,    try: 4850 },
};

const COINGECKO_URL =
  "https://api.coingecko.com/api/v3/simple/price" +
  `?ids=${Object.keys(CRYPTOS).join(",")}` +
  `&vs_currencies=${FIATS.join(",")}`;

/**
 * Fetch live rates. Returns { rates, live: boolean, fetchedAt: Date }.
 * Falls back to bundled rates if the network/API is unavailable.
 */
export async function getRates() {
  try {
    const res = await fetch(COINGECKO_URL, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    // Validate we got at least bitcoin/usd back.
    if (!data?.bitcoin?.usd) throw new Error("unexpected response");
    return { rates: data, live: true, fetchedAt: new Date() };
  } catch (err) {
    console.warn("Live rates unavailable, using fallback:", err.message);
    return { rates: FALLBACK, live: false, fetchedAt: new Date() };
  }
}

/**
 * Convert an order into a crypto amount.
 * @param {Array<{price:number, currency:string}>} items
 * @param {string} cryptoId  e.g. "bitcoin"
 * @param {object} rates     output of getRates().rates
 * @returns {number} amount of the chosen crypto to pay
 */
export function orderToCrypto(items, cryptoId, rates) {
  return items.reduce((sum, item) => {
    const price = rates[cryptoId]?.[item.currency];
    if (!price) throw new Error(`No rate for ${cryptoId}/${item.currency}`);
    return sum + item.price / price;
  }, 0);
}

/**
 * Convert a crypto amount into a fiat display value.
 */
export function cryptoToFiat(amount, cryptoId, fiat, rates) {
  const price = rates[cryptoId]?.[fiat];
  if (!price) throw new Error(`No rate for ${cryptoId}/${fiat}`);
  return amount * price;
}

/** Pretty-print a crypto amount with a sensible number of decimals. */
export function formatCrypto(amount, symbol) {
  const decimals = amount < 1 ? 8 : amount < 1000 ? 6 : 2;
  return `${amount.toFixed(decimals)} ${symbol}`;
}

/** Format a fiat amount using the browser's locale. */
export function formatFiat(amount, currency) {
  try {
    return new Intl.NumberFormat(undefined, {
      style: "currency",
      currency: currency.toUpperCase(),
    }).format(amount);
  } catch {
    return `${amount.toFixed(2)} ${currency.toUpperCase()}`;
  }
}
