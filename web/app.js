// app.js — wires the catalog, cart, and live conversion together.
import { PRODUCTS } from "./products.js";
import {
  CRYPTOS, FIATS, getRates, orderToCrypto, cryptoToFiat,
  formatCrypto, formatFiat,
} from "./rates.js";

const state = {
  cart: [],            // array of product objects (duplicates = quantity)
  rates: null,
  live: false,
  displayCurrency: "usd",
  cryptoId: "tether",
};

// ---- element refs ----
const el = (id) => document.getElementById(id);
const productGrid = el("productGrid");
const cartList = el("cartList");
const cartEmpty = el("cartEmpty");
const displaySel = el("displayCurrency");
const cryptoSel = el("payCrypto");
const totalFiatEl = el("totalFiat");
const totalCryptoEl = el("totalCrypto");
const rateNote = el("rateNote");
const payBtn = el("payBtn");
const rateBadge = el("rateBadge");

// ---- init ----
init();

async function init() {
  buildSelectors();
  renderProducts();
  await refreshRates();
  // Refresh live rates every 60s so prices stay current.
  setInterval(refreshRates, 60_000);
  wireEvents();
  render();
}

function buildSelectors() {
  displaySel.innerHTML = FIATS
    .map((f) => `<option value="${f}">${f.toUpperCase()}</option>`).join("");
  displaySel.value = state.displayCurrency;

  cryptoSel.innerHTML = Object.entries(CRYPTOS)
    .map(([id, c]) => `<option value="${id}">${c.name} (${c.symbol})</option>`).join("");
  cryptoSel.value = state.cryptoId;
}

function renderProducts() {
  productGrid.innerHTML = PRODUCTS.map((p) => `
    <div class="card" data-id="${p.id}">
      <div class="emoji">${p.emoji}</div>
      <div class="title">${p.title}</div>
      <div class="price">${formatFiat(p.price, p.currency)}</div>
    </div>`).join("");
}

async function refreshRates() {
  const { rates, live } = await getRates();
  state.rates = rates;
  state.live = live;
  rateBadge.textContent = live ? "● Live rates" : "● Cached rates";
  rateBadge.className = "rate-badge " + (live ? "live" : "stale");
  render();
}

function wireEvents() {
  productGrid.addEventListener("click", (e) => {
    const card = e.target.closest(".card");
    if (!card) return;
    const product = PRODUCTS.find((p) => p.id === card.dataset.id);
    state.cart.push(product);
    render();
  });

  cartList.addEventListener("click", (e) => {
    if (!e.target.classList.contains("x")) return;
    state.cart.splice(Number(e.target.dataset.index), 1);
    render();
  });

  displaySel.addEventListener("change", () => {
    state.displayCurrency = displaySel.value; render();
  });
  cryptoSel.addEventListener("change", () => {
    state.cryptoId = cryptoSel.value; render();
  });

  payBtn.addEventListener("click", openPayment);
  el("cancelPay").addEventListener("click", closePayment);
  el("confirmPay").addEventListener("click", () => {
    closePayment();
    state.cart = [];
    render();
    alert("Payment received (demo). Order confirmed!");
  });
}

function render() {
  // cart list
  cartEmpty.hidden = state.cart.length > 0;
  cartList.innerHTML = state.cart.map((p, i) => `
    <li class="cart-item">
      <span>${p.emoji} ${p.title}</span>
      <span>
        ${formatFiat(p.price, p.currency)}
        <button class="x" data-index="${i}" title="Remove">✕</button>
      </span>
    </li>`).join("");

  if (!state.rates || state.cart.length === 0) {
    totalFiatEl.textContent = "—";
    totalCryptoEl.textContent = "—";
    rateNote.textContent = "";
    payBtn.disabled = true;
    return;
  }

  const crypto = CRYPTOS[state.cryptoId];
  const cryptoAmount = orderToCrypto(state.cart, state.cryptoId, state.rates);
  const fiatTotal = cryptoToFiat(cryptoAmount, state.cryptoId, state.displayCurrency, state.rates);

  totalFiatEl.textContent = formatFiat(fiatTotal, state.displayCurrency);
  totalCryptoEl.textContent = formatCrypto(cryptoAmount, crypto.symbol);

  const unit = state.rates[state.cryptoId][state.displayCurrency];
  rateNote.textContent =
    `1 ${crypto.symbol} = ${formatFiat(unit, state.displayCurrency)} ` +
    `${state.live ? "(live)" : "(cached — connect to refresh)"}`;
  payBtn.disabled = false;
}

// ---- payment modal ----
let lockTimer = null;

function openPayment() {
  const crypto = CRYPTOS[state.cryptoId];
  const amount = orderToCrypto(state.cart, state.cryptoId, state.rates);
  const amountStr = formatCrypto(amount, crypto.symbol);
  const demoAddr = demoAddress(crypto.symbol);

  el("payAmount").textContent = amountStr;
  el("payAddr").textContent = demoAddr;
  el("qr").innerHTML =
    `<img alt="QR" src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(demoAddr + "?amount=" + amount)}" />`;
  el("payModal").hidden = false;

  let remaining = 15 * 60;
  const timerEl = el("lockTimer");
  clearInterval(lockTimer);
  lockTimer = setInterval(() => {
    remaining--;
    const m = String(Math.floor(remaining / 60)).padStart(2, "0");
    const s = String(remaining % 60).padStart(2, "0");
    timerEl.textContent = `${m}:${s}`;
    if (remaining <= 0) { closePayment(); alert("Rate expired. Please try again."); }
  }, 1000);
}

function closePayment() {
  el("payModal").hidden = true;
  clearInterval(lockTimer);
}

// A throwaway address for the demo so the QR looks real. Not a real wallet.
function demoAddress(symbol) {
  const prefixes = { BTC: "bc1q", ETH: "0x", USDT: "0x", USDC: "0x", BNB: "bnb1", SOL: "" };
  const chars = "abcdef0123456789";
  let body = "";
  for (let i = 0; i < 34; i++) body += chars[Math.floor(Math.random() * chars.length)];
  return (prefixes[symbol] ?? "") + body;
}
