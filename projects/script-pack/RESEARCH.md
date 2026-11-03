# Script Pack: product research (2026-11-03)

Goal (Tigran): a tool that makes screenwriters' lives easier. A writer gives the script once and gets every
document each recipient needs. Three research rounds (Cloud web search + two external deep-research runs).

## Market
- Writing software: Final Draft is the standard (.fdx); WriterDuet and Arc Studio grow (cloud, co-writing);
  Fade In, Highland, Celtx; KIT Scenarist / Story Architect in Russia/CIS. A cited stat (59% Final Draft, 12% Celtx,
  8% Movie Magic, 7% WriterDuet, 4% Fade In of ~12,000 scripts) likely comes from Stephen Follows' PDF-metadata
  study; the original was not verified and looks old.
- Production: Movie Magic Scheduling/Budgeting (standard), StudioBinder, Filmustage (AI breakdown), Scriptation.
- Coverage: fastest growing, AI-driven: Prescene ($49/mo), Greenlight Coverage ($50–260/mo), ScreenplayIQ, Largo.ai.
- Selling: Black List, Stage 32 (Contest Hub replaced Coverfly), ISA, InkTip, FilmFreeway. Coverfly closed 2025-08-01.

## Documents writers must produce (from real rules)
Logline (Sundance ≤ 75 words), synopsis (Sundance ≤ 750, Micro-series ≤ 500, Eurimages 1 page), character bios
(Sundance 3 × ≤ 150), treatment, series bible, episode synopses, one-pager, query letter, casting breakdown, sides,
English script + synopsis for Eurimages/foreign buyers, lab application, personal statement.

## Competitors for "one script → full package" (2025–2026)
Prescene Workflows: coverage, finance plan, schedule, character/prop breakdown, series coverage; no logline,
synopsis, bible, deck, sides, translation. Studiovity: AI logline/synopsis help. Final Draft 13: logline generator.
Filmustage: breakdown, schedule, budget, cast tagging. Nobody does the writer's submission package; nobody
handles Armenian; Russian unverified.

## Gaps in the research
No reliable data on pain frequency, willingness to pay or market size. Only real conversations will answer that:
10–15 writers/producers in Armenia/CIS.

## Decision
Build it inside `director-desk` first (`scripts/pack.py`, 2026-11-03), test on Ani's real scripts
(84-ի ամառը), then decide on a standalone product. Differentiators: Armenian/Russian scripts, no training on
uploaded scripts, sides cut from real scenes, word limits checked against real lab rules.
Next: HY/RU → EN script translation in format; deck with images; submission tracker (post-Coverfly gap).
