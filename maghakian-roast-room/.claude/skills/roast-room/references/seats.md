# Seats

## Maghakian industry seats

Five composite archetypes built for Maghakian Scripts. They are not real people, carry no verbatim quotes, and cite their own ids. They are on the default board (except the Publisher, who is on call for book decisions).

| Seat | Agent | Pillar | Owns the question | Brain |
|---|---|---|---|---|
| Buyer | `council-buyer` | Platform sales and acquisitions | Will a platform or broadcaster buy this, for which slot, and on what terms? | `brains/platform-buyer/` |
| Showrunner | `council-showrunner` | Story and the writers' room | Is the story engine strong enough to carry this format, and can the room deliver it on schedule? | `brains/showrunner/` |
| Line Producer | `council-lineprod` | Budget, schedule and physical production | Can this be made at this budget, on this schedule, in Armenia, without the money running out mid-shoot? | `brains/line-producer/` |
| Co-pro | `council-copro` | Co-production, funds and rights ownership | Who else can pay for this, and what do we give up to get their money? | `brains/co-production/` |
| Publisher | `council-publisher` | Children's book publishing | Will parents, schools and libraries buy this book, and does the print run pay back? | `brains/childrens-publisher/` |

Tensions to expect:

- Buyer (fit the slot, sell fast, sell to three desks) against Showrunner (protect the engine and the voice) and Co-pro (keep the IP, wait for the right partners).
- Line Producer (cash calendar, contingency, locked script) against Gary V and Hormozi (say yes, move now) and against any turnkey offer priced without delivery risk.
- Co-pro (own the IP, build a finance plan) against Buffett (count only signed money) on timing; they agree on never risking ruin.
- Publisher (small first run, pre-sell, unit cost) against Showrunner and Sara Blakely on how big to bet on a first title.
- Downside seats for studio decisions: Buffett and the Line Producer. For book decisions: Buffett and the Publisher.

## Original seats

`roster.json` (one folder up) is the source of truth: every seat, its key, pillar, question, and scorecard dimension, plus the default board and how the board is picked. The seven seats that ship with the Roast Room:

| Seat | Agent | Pillar | Owns the question | Brain |
|---|---|---|---|---|
| Bezos | `council-bezos` | Strategy and decisions | Is this the right bet, and how reversible is it? | `brains/jeff-bezos/` |
| Graham | `council-graham` | Product and startups | Is this something people actually want, and is it growing? | `brains/paul-graham/` |
| Hormozi | `council-hormozi` | Offers, pricing, and sales | Will people pay, how much, and how do we close? | `brains/alex-hormozi/` |
| Gary V | `council-garyvee` | Marketing and attention | Where does the attention come from, and is it underpriced? | `brains/gary-vaynerchuk/` |
| Martell | `council-martell` | People, hiring, and founder time | Who does this, and what does it cost the founder's calendar? | `brains/dan-martell/` |
| Wickman | `council-wickman` | Operations and scaling | Can the business run this without the founder holding it together? | `brains/gino-wickman/` |
| Buffett | `council-buffett` | Money and capital | What does it do to cash, risk, and long-term value? | `brains/warren-buffett/` |

Brain paths are relative to `.claude/skills/roast-room/`. Seats added with `/newroaster` follow the same pattern: `council-<key>` and `brains/<slug>/`, listed in `roster.json`.

## Relevance weights

The Chair sets a weight per seat for each decision, before Round 1, and writes the reason in one line. Weights make the final score honest: a pricing call should lean on Hormozi, a hiring call on Martell.

| Weight | Meaning |
|---|---|
| 3 | This decision lives in the seat's pillar |
| 2 | The pillar is materially affected |
| 1 | The pillar is touched at the edges |

Every seat is at least 1. Exactly one or two seats get a 3.

## Quick council

`--quick` seats four (recommended per SKILL.md "Pick the board", then confirmed): the two highest-weight seats, the seat that guards the downside (Buffett or Bezos out of the box; otherwise the board's money, capital, or risk seat), and the seat most likely to disagree with the others (the Chair names why). Use quick for reversible, low-stakes calls. Full council for anything a founder cannot easily undo.

## Natural tensions to expect

- Bezos and Buffett (long horizon, downside first) against Hormozi and Gary V (speed to cash, volume, act now).
- Graham (do things that don't scale, stay close to users) against Wickman (systems, process, accountability).
- Buffett (stay in your circle, avoid leverage) against Gary V (bet on the underpriced platform now).
- Martell (buy back your time, hire early) against Graham and Buffett (stay small and frugal until it works).

Seats added with `/newroaster` append their own tension lines here.

On-call seats (in `roster.json`, off the default board; the Chair recommends them when the decision is in their lane):

| Seat | Agent | Pillar | Owns the question | Brain |
|---|---|---|---|---|
| Naval | `council-naval` | Leverage and wealth | Does this build leverage and equity you own, or does it just rent out your time? | `brains/naval-ravikant/` |
| Codie | `council-sanchez` | Buying and owning small businesses | Should you build this, or buy something that already works? | `brains/codie-sanchez/` |
| Sara | `council-blakely` | Consumer product and brand from zero | Will customers love it enough to sell it for you, without outside money? | `brains/sara-blakely/` |
| Leila | `council-leila` | Leadership and scaling teams | Can your team and your leadership carry this, and who has to change? | `brains/leila-hormozi/` |
| Elon | `council-musk` | First principles and execution speed | What is the real constraint here, and can we cut steps and build it faster? | `brains/elon-musk/` |

- Naval (own the equity, tiny teams, self-fund) against Hormozi and Gary V (more volume, more offers, more output that the founder still has to rent their hours to).
- Codie (buy proven cash flow) against Graham and Naval (build something new people want).
- Sara (product good enough to sell itself, no ads, no outside money) against Gary V and Hormozi (attention and sales machines) and against any seat pushing to raise.
- Leila (fix lead flow and the founder's leadership before hiring) against Martell (hire early to buy back time). Leila and Wickman agree on accountability and split when process stands in for leadership.
- Elon (question the requirement, delete the step, attack the bottleneck now) against Wickman (give every process an owner and a cadence) and Buffett (keep cash, wait for the fat pitch). Elon and Graham agree on speed and split on whether a launch counts before the delivery system scales.
- Elon's aggressive dates are for the team, not for customers or lenders; Martell and Leila own what his pace costs the people.
- Leila Hormozi and Alex Hormozi are different seats and different people. Name them "Leila" and "Hormozi".
- Deakins (one camera, small crew, light built into the set, wait for the right light) against Line Producer (13 to 30 pages in a 12 hour day, every hour costs). Deakins concedes speed on a series and names what is lost; Line Producer prices his ask instead of refusing it.
- Deakins (every image and every camera move must serve the story) against any seat chasing a showy, "beautiful" or trailer-friendly shot.

If Round 1 comes back unanimous, the Chair should be suspicious and press the seat whose pillar is most at risk in Round 2.
- Rhimes (a series engine that runs for seasons, character first, know the ending) against Line Producer (every extra character, set and episode costs pages and days) and against Quinn (one festival film over a long run).
- Villeneuve (image over dialogue, storyboard everything, real locations, bond with actors before the shoot) against Line Producer (prep days and locations cost money) and against Rhimes (a series runs on dialogue and volume).
- Blum (low budget, hard ceiling, scale plus backend, one hook) against Villeneuve and Vermette (real locations and built worlds) and Bloys (premium spend). Blum and Line Producer agree on cost; they split when Blum's backend has no market to pay it.
- Vermette (real, story-led worlds, built spaces for actors) against Line Producer and Blum (builds and dressing cost days and money). Vermette and Deakins agree when the light is designed into the set.
- Murch (emotion first, shortest working length, fresh eye) against Rhimes (more scenes, more episodes) and Line Producer (post days are cut first). Murch and Villeneuve agree on image over talk and split on pace when a series needs volume.
- Bloys (premium, creator voice, brand over volume, no testing) against Bajaria (local hits at global scale, more volume) and Blum (cheap and fast). All buyer seats agree an Armenian studio reaches them through agents, co-producers or festivals, not cold pitches.
