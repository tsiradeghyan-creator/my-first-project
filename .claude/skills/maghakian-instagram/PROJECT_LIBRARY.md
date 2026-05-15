# PROJECT_LIBRARY.md – Cached Research per Project

Skill-ի **research cache**։ Մեկ անգամ research-ից հետո, project-ի facts-ը պահվում են այստեղ։ Հաջորդ անգամ նույն project-ի մասին գրելիս՝ ուղիղ այստեղից կարդում ենք, ոչ ինտերնետից։

## Update Rules

1. Skill-ը research-ից հետո **ՊԱՐՏԱԴԻՐ update է անում** այս ֆայլը նոր փաստերով
2. User-ի կողմից տրված info → marked as «user-confirmed»
3. Web research → marked with source URL
4. Outdated info → struck through, ոչ ջնջված (audit trail)
5. Format: structured YAML-like block per project

## Schema (per project)

```
### Project N. [Name]
- Status: aired / upcoming / ongoing / cancelled
- Years: YYYY – YYYY
- Channel: ...
- Production: ...
- Episode count: N
- Genre: ...
- Plot premise: [1-2 sentences]
- Main characters: [name (actor)]
- Cast IG handles: [@handle]
- Iconic moments / lines: [list]
- Deleted scenes / BTS available: yes/no/unknown
- Last researched: YYYY-MM-DD
- Sources: [URLs]
- User-confirmed: [facts]
- ⚠️ Gaps: [missing data points]
```

---

## 47-Project Index Status

| # | Project | Cache status |
|---|---------|--------------|
| 01 | Օտարը | 🔴 not researched |
| 02 | Ելենի օրագիրը | 🔴 not researched |
| 03 | Ելենի օրագիրը 2 | 🔴 not researched |
| 04 | Թղթե երազանք | 🔴 not researched |
| 05 | **Երկուսով** | 🟡 partial (cast + channel) |
| 06 | Երկուստով | 🔴 not researched |
| 07 | Խաղալիք | 🔴 not researched |
| 08 | Կհանդիպենք աստղի տակից | 🔴 not researched |
| 09 | Բեկորներ | 🔴 not researched |
| 10 | Բռնիր ձեռքս | 🔴 not researched |
| 11 | Երկու քույր ենք | 🔴 not researched |
| 12 | Հատուկ դասարան | 🔴 not researched |
| 13 | Հատուկ դասարան 2 | 🔴 not researched |
| 14 | Ապրիր ինձ հետ | 🔴 not researched |
| 15 | Մենա ինձ հետ | 🔴 not researched |
| 16 | 4 երազանք | 🔴 not researched |
| 17 | Կհանդիպենք աստղի տակից 2 | 🔴 not researched |
| 18 | Hotel Grand | 🔴 not researched |
| 19 | Hotel Grand 2 | 🔴 not researched |
| 20 | Hotel Grand 3 | 🔴 not researched |
| 21-47 | (rest) | 🔴 not researched |

Legend: 🟢 complete / 🟡 partial / 🔴 not researched

---

## Project Cache Entries

### 05. Երկուսով (Yerkusov / Erkusov)

- **Status**: aired (50+ episodes broadcast)
- **Years**: premiere October 21 (year TBD via user)
- **Channel**: Shant TV / Shant Premium
- **Streaming**: Shant Digital TV app, ArmKino, YouTube
- **Production**: Shant Production
- **Director**: Mher Khachaturyan (Մհեր Խաչատուրյան)
- **Episode count**: 147+ confirmed in search results (episodes 147, 148 referenced)
- **Genre**: Drama (love-triangle premise visible from poster)
- **Plot premise**: ⚠️ Not confirmed from web — poster suggests bride caught between two men + suitcase = baggage/secrets/departure motif. **Needs user confirmation.**
- **Main characters** (actor names found, character names unknown):
  - Inna Khojamiryan / Իննա Խոջամիրյան
  - Vahe Ziroyan / Վահե Զիրոյան
  - Marinka Khachatryan / Մարինկա Խաչատրյան
  - David Akobyan / Դավիթ Հակոբյան
  - Varuzhan Margaryan / Վարուժան Մարգարյան
  - Mary Yeremyan / Մերի Երեմյան
  - Nelly Heranyan / Նելլի Հերանյան
  - Gagik Madoyan / Գագիկ Մադոյան
- **Cast IG handles**: ⚠️ Unknown — needs verification
- **Iconic moments / lines**: ⚠️ Unknown — needs user
- **Deleted scenes / BTS**: ⚠️ Unknown — needs user
- **Last researched**: 2026-05-15
- **Sources**:
  - https://www.facebook.com/ShantDigitalTV/videos/677822796043399/
  - https://armfilm.co/en/series/
  - https://www.armkino.am/en/channel/shant-tv-armenia
  - https://hayertv.com/en/armenian-series/
  - https://www.youtube.com/watch?v=c95cHmGGdk4 (Episode 17)
  - https://www.youtube.com/watch?v=2goApSjMi_k (Episode 60)
- **User-confirmed**: [pending]
- **⚠️ Gaps**:
  - Plot premise (specific)
  - Main characters' names in show (not actors)
  - Iconic line / scene reference
  - Deleted scene availability for DM lead magnet
  - Premiere year
  - Cast IG handles
  - Production team (writers, executive producers from Maghakian side)

---

## How to Use This Library

### Workflow integration
1. User asks for content about project X
2. Skill checks PROJECT_LIBRARY.md for cached entry
3. **If 🟢 complete** → use cached info, no re-research
4. **If 🟡 partial** → fill gaps via WebSearch + ask user
5. **If 🔴 not researched** → run full Research Protocol (RESEARCH_PROTOCOL.md)
6. After every research run → update this file

### Re-research triggers
- Cache age >90 days
- User reports outdated info
- New season / continuation released
- Cast changes

### Cross-project queries
This file enables:
- «Universe Map» (Tactic 10) — find recurring actors across projects
- «Cross-Project Resurrection» (Tactic 11) — find legitimate connections
- Hashtag-set generation per project

---

## Maintenance

After each project research run, append/update entry above with:
1. New `### NN. ProjectName` block (if not exists)
2. Update index table status emoji
3. Add `Last researched: YYYY-MM-DD`
4. Source URLs
5. Mark gaps clearly

Update commit message: `chore(skill): cache research for [project name]`
