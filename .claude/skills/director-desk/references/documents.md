# Documents menu: ask first, then make only what is needed

Tigran's rule (2026-11-03): the tool asks before it makes anything. Never dump every file.

## 1. Ask (AskUserQuestion, in Armenian, one screen)
1. **Ում համար է** (multi-select): Գլխավոր պրոդյուսեր · Պրոդյուսեր · Պլատֆորմ/հեռուստաընկերություն ·
   Ֆոնդ/մրցույթ · Ռեժիսոր · Ադմին/տնօրեն/երկրորդ ռեժիսոր · Հաշվապահ · Կաստինգ · Դերասաններ ·
   Կոստյում/ռեկվիզիտ/գրիմ · Միջազգային գործընկեր · «Բոլորը»
2. **Ինչի համար** (free text is fine: "շաբաթական հաշվետվություն", "ներկայացնել ֆոնդին", "վաղվա նկարահանում").
3. **Ժամանակահատված** when money or progress is involved: օր · շաբաթ · ամիս · ամբողջ նախագիծ (+ date).
Then show the matching documents below as a checklist (multi-select, "Բոլորը" first) and make only those.
If something is missing for a document (rates, receipts, scripts), say what and ask for it.

## 2. What each recipient can get
| Recipient | Documents | Command |
|---|---|---|
| Գլխավոր պրոդյուսեր / Պրոդյուսեր | Ծախսերի հաշվետվություն (օր/շաբաթ/ամիս/ամբողջը) | `plan.py report finance project.xlsx --period week --date 18.06.2026` |
| | Արտադրության ընթացք (% նկարված, մնացած էջեր/օրեր, ով քանի օր) | `plan.py report progress project.xlsx --master master.xlsx` |
| | One-pager, synopsis | `pack.py build` (01 Producer) |
| Պլատֆորմ / հեռուստաընկերություն | Pitch deck / series bible, սերիաների բովանդակություն | `pack.py build` (02 Platform) |
| Ֆոնդ / մրցույթ | Հայտ ըստ կանոնների, անգլերեն one-pager, բյուջեի ամփոփ | `pack.py build --preset …`, `report finance --period all` |
| Ռեժիսոր | Սցենար PDF/Word/FDX, տեսարանների ցուցակ, օրվա տեքստեր | `pack.py build` (03), `plan.py day --texts` |
| Ադմին / տնօրեն / երկրորդ ռեժիսոր | Օրվա ռազբիվկա, գլխավոր ցուցակ (Չնկարված ըստ օբյեկտների) | `plan.py day`, `plan.py master` |
| Հաշվապահ | Վճարների ցուցակ (ով քանի օր × դրույք), ծախսերի մատյան | `plan.py report payroll`, `report finance` |
| Կաստինգ | Դերերի ցուցակ համարներով, casting breakdown, CSV | `pack.py build` (05), master «Դերասաններ» |
| Դերասաններ | Sides | `pack.py build` (06) |
| Կոստյում / ռեկվիզիտ / գրիմ | Օրվա թերթիկներ (Հագուստ, Ռեկվիզիտ, Մասսովկա էջերը օրվա xlsx-ում) | `plan.py day` |
| Միջազգային | Անգլերեն one-pager | `pack.py build` (07) |

## 3. Money: how data gets in
- `plan.py init project.xlsx --master master.xlsx` once: Կազմ has the standard crew positions + every
  character from the master; fill names, rates and rate type (Օրական / Ամսական / Միանգամյա).
- Every shooting day: `plan.py day … --project project.xlsx` ticks the actors of the day's scenes and the crew
  with daily rates (Ներկայություն sheet; the admin can fix ticks by hand).
- Receipts: Tigran sends a photo or text → read it → `plan.py expense project.xlsx --date … --category …
  --amount … --desc … --payee … --by … --receipt photo.jpg` (the photo is copied to Չեկեր/). Ask when the
  category or amount is unclear; never guess an amount.
- Reports read the workbook every time, so hand edits count.

## 4. Look (all reports)
Answer first (hero row: one red number = the main answer), then structure (bars), then detail tables.
Type scale 1.25 on 9 pt, 4 pt spacing, numbers right-aligned and tabular, red only for the main figure.
Every page: recipient in red at the top, page X / Y at the bottom.
