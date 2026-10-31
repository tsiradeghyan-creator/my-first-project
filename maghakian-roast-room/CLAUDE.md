# Maghakian Roast Room

This folder is the Roast Room, adapted for Maghakian Scripts: a council of simulated advisors that debates a decision for the studio or the children's publishing house. It is based on nateherkai/roast-room (MIT, see LICENSE).

Seventeen seats ship with it:

- **Five industry seats** built for Maghakian Scripts. They are composite archetypes, not real people: Platform Buyer, Showrunner, Line Producer, Co-production and Funds, Children's Publisher.
- **Twelve named seats** from the original project, simulations built from each person's public work: Bezos, Paul Graham, Hormozi, Gary Vaynerchuk, Dan Martell, Gino Wickman, Buffett, Naval Ravikant, Codie Sanchez, Leila Hormozi, Sara Blakely, Elon Musk.

The default board is Platform Buyer, Showrunner, Line Producer, Co-pro, Hormozi, Gary V and Buffett. Before each council the Chair recommends a board for the question and the user confirms it. For book questions, recommend the Children's Publisher, and usually Sara Blakely and Buffett.

- Read `business.md` before every council for the studio's real facts. Ask for any number marked TODO that the decision needs.
- When the user brings a decision ("should we...", pricing a series, a turnkey offer, a co-production, a first print run, a hire, a pivot), run `/roast-room`. For a quick question to one advisor, use `/roast-room ask <seat> ...`.
- Every advisor and the default board live in `.claude/skills/roast-room/roster.json`. To add an advisor, run `/newroaster`. To change who sits at the table by default, run `/roast-room board`.
- If the user asks to start or open the room, run `npm start` in the background and tell them to open http://localhost:4730. It needs Node 20 or newer and nothing else.
- Councils are saved in `sessions/<date>-<decision>/`. Follow `.claude/skills/roast-room/references/live-room.md` exactly so the room can read them.
- Named seats are simulations built from public work. Never present their words as something the real person said unless it is a verbatim quote with a source id from that seat's brain. Industry seats have no quotes at all; they cite their own ids (BUY-F1, SHO-P3 and so on). They never speak for Ani Maghakyan, Tigran, or any real executive.
- Language: the user may write in Armenian, English or Russian. Run the council and write the chat verdict and `verdict.md` in the user's language. Keep the card field labels and every JSON key in English. Write the text inside `verdict.json` in English, because the PDF export has no Armenian font yet.
- Write the Chair's parts in plain language: short sentences, no hype, no filler. Keep the verdict in chat short enough to decide from at a glance.
