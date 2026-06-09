// products.js — sample catalog. Each item is priced in its own real-world
// currency, to prove the point: a buyer pays once, in crypto, and the
// platform converts every item from its native currency at live rates.

export const PRODUCTS = [
  { id: "jacket",   title: "Leather Jacket",   emoji: "🧥", price: 120, currency: "eur" },
  { id: "sneakers", title: "Running Sneakers", emoji: "👟", price: 95,  currency: "usd" },
  { id: "watch",    title: "Classic Watch",    emoji: "⌚", price: 40000, currency: "jpy" },
  { id: "tshirt",   title: "Cotton T-Shirt",   emoji: "👕", price: 25,  currency: "gbp" },
  { id: "bag",      title: "Designer Bag",     emoji: "👜", price: 350, currency: "aed" },
  { id: "scarf",    title: "Wool Scarf",       emoji: "🧣", price: 9000, currency: "amd" },
];
