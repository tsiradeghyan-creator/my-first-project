# MyBusinessApp — iPhone (SwiftUI) starter

A working starter app for iPhone, built with SwiftUI. It is a foundation
you can turn into a real, paying business app.

## Honest note on earnings

No app earns money by itself. An app earns money when **people pay you for
something valuable** — a product, a service, a subscription. This starter
gives you the structure for that: offerings (what you sell), sales (what
people bought), and an earnings dashboard. The income depends on having
something people actually want and reaching enough customers.

## What's inside

- `Models/Models.swift` — `Offering` (what you sell) and `Sale` (a purchase).
- `Services/AppStore.swift` — app data + on-device saving. Replace the
  sample offerings and connect a real payment provider where marked `TODO`.
- `Views/` — three tabs:
  - **Earnings** — today's and total earnings, recent sales.
  - **Offerings** — list, add, and "sell" your products/services.
  - **Profile** — a summary and your next steps.

## How to run it on your iPhone

1. On a Mac, install **Xcode** (free, from the Mac App Store).
2. Create a new Xcode project: *App* → SwiftUI → name it `MyBusinessApp`.
3. Drag these `.swift` files into the project (replace the generated ones).
4. Plug in your iPhone, select it as the run target, press **Run** (▶).

> Building and installing iOS apps requires a Mac with Xcode. A free Apple
> ID lets you run it on your own phone; a paid Apple Developer account
> ($99/year) is needed to publish on the App Store.

## To make it actually earn money

1. Replace the sample offerings with your real products or services.
2. Add real payments — Apple In-App Purchase (StoreKit) for digital goods,
   or Stripe for services. The `recordSale` function marks where to do this.
3. Get customers — this is the hard part and where real income comes from.

## Watch out for scams

Any app, course, or person promising a fixed "$X per day, guaranteed" with
no work is almost certainly a scam. Real income is variable and depends on
the value you create.
