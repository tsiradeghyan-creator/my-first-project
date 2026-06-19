# QUALITY_GATE.md – Pre-Publish Self-Check

Skill-ի վերջին line of defense, որից առաջ ոչ մի post չպիտի անցնի։ 30 ☐, 3 minute audit, 0 exception։

## 🚦 The 4 Gates

Content պետք է անցնի ՉՈՐՍ gate-ով՝ Research Gate, Craft Gate, Brand Gate, Compliance Gate։ Որևէ ☐ չլրացրած → STOP, rework։

---

## Gate 1 — Research Gate (5 checks)

🔒 Foundation gate։ Ոչ մի craft չի արդարացնում fabrication-ը։

- ☐ Research Protocol-ը (RESEARCH_PROTOCOL.md) անցկացված է
- ☐ PROJECT_LIBRARY.md-ում project-ի entry-ն updated է
- ☐ Ամեն specific claim ունի source (research-ից, user-ից, կամ marked as hypothetical)
- ☐ Ոչ մի invented plot detail, line, scene, character (real project-ի մասին)
- ☐ User-ին հարցրած գրավադրված gap-ները լրացված են

**Fail → STOP, return to Քայլ 0 of SKILL.md workflow.**

---

## Gate 2 — Craft Gate (10 checks)

✍️ Writing-ի quality.

### Hook (3)
- ☐ Hook < 6 բառ
- ☐ Hook standalone-readable mute-ով
- ☐ Hook-ը provokes specific reaction (curiosity, nostalgia, anger, validation)

### Body / Story (4)
- ☐ Կիրառվում է գոնե մեկ framework (Pixar / PAS / BAB / AIDA / Hero's Journey)
- ☐ Conversational rhythm, ոչ corporate
- ☐ Մի ուղերձ, ոչ 3
- ☐ Caption < 2200 characters (IG limit)

### CTA (3)
- ☐ Մի CTA, ոչ 2-3
- ☐ CTA specific, ոչ generic
- ☐ Promised deliverable exists (եթե DM trigger)

**Fail → rework section.**

---

## Gate 3 — Brand Gate (8 checks)

🎬 Maghakian DNA-ի consistency։

### Maghakian Doctrine (2)
- ☐ Կիրառվում է գոնե մեկ Doctrine tactic-ից (12-ից)
- ☐ Tactic-ը post-ի goal-ին համապատասխանում է

### Voice (2)
- ☐ Voice-ը match է table-ին (Personal vs Agency)
- ☐ Tone-ը confident, intimate, cinematic, honest, reverent — ոչ corporate, ոչ desperate

### Visual (2)
- ☐ Image / poster գեներացված է IMAGE_PROMPTS.md-ով, brand-locked
- ☐ Color, lighting, typography match Maghakian aesthetic

### Manifesto (2)
- ☐ Plot > Promotion (post-ը plot/character ունի, ոչ առանց story-ի)
- ☐ Cinema > Content (cinematic, ոչ content-marketer feel)

**Fail → re-anchor to brand.**

---

## Gate 4 — Compliance Gate (7 checks)

⚠️ Risk avoidance.

### Anti-Patterns (4)
- ☐ Չի սկսում «Բարև բոլորին»-ով
- ☐ Չի պարունակում generic motivational quote
- ☐ Չի օգտագործում banned hashtag (#like4like, etc.)
- ☐ Չի պարունակում emoji-overload (max 5-7)

### Trigger Hygiene (2)
- ☐ Կա առնվազն 1 psychological trigger (PSYCHOLOGY.md)
- ☐ Trigger-ները authentic են, ոչ manipulative

### Legal / Platform (1)
- ☐ Չի օգտագործում unauthorized actor image / non-cleared photo (verify rights for cast images)

**Fail → fix or kill post.**

---

## ✅ Sufficiency Score

| Gate | Min checks to pass | All checks |
|------|---------------------|-------------|
| Research | 5/5 ⚠️ (zero tolerance) | 5 |
| Craft | 9/10 | 10 |
| Brand | 7/8 | 8 |
| Compliance | 7/7 ⚠️ (zero tolerance) | 7 |

**Total**: 30 checks. Publish requires Research + Compliance fully passed; Craft + Brand can have 1-2 flex points if conscious tradeoff.

---

## ⏱️ Quick Audit (3-minute version)

Time-pressed? Run this fast version.

1. **Research check (30s)**: Is every specific claim sourced or hypothetical-marked?
2. **Hook test (30s)**: Mute the video — is the hook visual + text enough?
3. **Aaron Sorkin test (30s)**: Would a real scriptwriter respect this?
4. **CTA specificity (30s)**: Specific or generic?
5. **Brand DNA (30s)**: Cinematic dark aesthetic? Maghakian voice?
6. **Anti-pattern scan (30s)**: Any forbidden moves?

All 6 ✅ → publish-ready (mini version).
Otherwise → run full 30-check gate.

---

## 🎯 Diagnostic Patterns (when checks fail)

### «Research gate fails repeatedly»
- Problem: User isn't providing project specifics, OR skill not running protocol
- Fix: Strengthen Step 0 enforcement, add to top of SKILL.md workflow

### «Craft gate: hook fails»
- Problem: Hook too long, too vague, or doesn't provoke
- Fix: Read HOOKS_LIBRARY.md, pick a tested pattern, customize

### «Brand gate: voice mismatch»
- Problem: Sounds like generic Instagram coach
- Fix: Add personal Maghakian detail, anchor to one of 6 manifesto principles

### «Compliance gate: trigger feels manipulative»
- Problem: Scarcity claim is fake, or reciprocity offer doesn't exist
- Fix: Don't deploy until promise is real

---

## 📋 Pre-Publish Final Checklist

Copy-paste before publishing:

```
GATE 1 — RESEARCH
☐ Protocol run
☐ Library updated
☐ Sources verified
☐ No invention
☐ Gaps closed

GATE 2 — CRAFT
☐ Hook < 6 words
☐ Hook standalone-readable
☐ Hook provokes
☐ Framework used
☐ Conversational
☐ One message
☐ Caption < 2200 chars
☐ One CTA
☐ CTA specific
☐ Deliverable exists

GATE 3 — BRAND
☐ Doctrine tactic
☐ Tactic-goal match
☐ Voice match
☐ Tone right
☐ Visual brand-locked
☐ Aesthetic consistent
☐ Plot > Promotion
☐ Cinema > Content

GATE 4 — COMPLIANCE
☐ No "Բարև բոլորին"
☐ No generic quote
☐ No banned hashtags
☐ No emoji overload
☐ ≥1 trigger
☐ Authentic
☐ Rights cleared

= [X]/30 — Publish? Y/N
```

---

## 🔄 Continuous Improvement

After each post (within 7 days of publishing):
1. Record which gates passed / failed
2. Track post performance
3. Identify correlations:
   - «Posts that passed all 30 → avg 2x better reach»
   - «Posts with weak Research gate → highest comment criticism»
4. Update gate weights quarterly based on outcomes
