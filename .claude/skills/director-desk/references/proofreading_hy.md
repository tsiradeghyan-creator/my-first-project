# Սցենարի սրբագրման կանոններ (Maghakian Scripts)

Used by Claude (director-desk) and by the ChatGPT pack. The editor (model) reads the script scene by scene and
returns a JSON list of corrections; `scripts/proofread.py` applies them. The editor never rewrites the script.

## 0. Golden rules
1. **Ani's text is the author's text.** Fix errors, never "improve" style, never shorten, never add scenes or lines.
2. **Dialogue keeps the character's voice.** Colloquial and dialect forms are intentional:
   `ա` (instead of է), `էկար, էսա, էդ, էն, նենց, սենց, ոնց, ըլնելու, ասեցի, ինչի, հեսա, թվումա, պետքա`, Russian
   words (`կլյուչ, խոդ, պեռաշկի`), slang. **Do not convert them to literary Armenian.** In dialogue fix only:
   obvious typos (letters swapped or missing, words glued together by mistake), punctuation, question/exclamation marks.
3. **Remarks (action lines, parentheticals, scene headings) are literary Armenian:** fix spelling, grammar, case
   endings, missing auxiliary «է», missing spaces, punctuation.
4. When unsure, do not change: make a **remark** (no `replace`) with the question in `why`.
5. Meaning problems (continuity, logic, names, facts) are **remarks only**, with a suggested fix in `why`.

## 1. Done automatically by proofread.py (don't list these)
`,,,` / `,,` → `...` · Latin `:` after an Armenian word at sentence end → `։` · spaces before `։ ,` · double spaces.

## 2. Punctuation (կետադրություն)
- **Վերջակետ** `։` ends a sentence (never Latin `:` or `.`).
- **Հարցական** `՞` sits **on the stressed vowel of the word that is asked about**, not at the end of the sentence;
  one per sentence: `ուր ես՞` → `ո՞ւր ես`, `բերել ես՞` → `բերե՞լ ես`, `Կասկածում էիր՞` → `Կասկածո՞ւմ էիր`,
  `Ինչ էղաք՞` → `Ի՞նչ էղաք`, `Ինչի չէ՞` → `Ինչի՞ չէ`. With «ու» the mark goes on ու: `ո՞ւր`, `գնո՞ւմ`.
  Remove doubled `՞՞`. A question without any mark gets one (`Ինչ եղավ երաժշտությունը` → `Ի՞նչ եղավ…`).
- **Բացականչական** `՜` on the stressed vowel (`Վա՜յ`, `Հայրի՜կ`). Latin `!` at the end: replace with `՜` on the vowel.
- **Շեշտ** `՛` for emphasis, address or command (`Արի՛`, `Լսի՛ր`); don't add where Ani didn't stress.
- **Ստորակետ** `,`: after a vocative (`Արշակ, իմ պապն ա`), before `որ, թե, երբ, եթե, քանի որ, որովհետև, բայց, իսկ`,
  between homogeneous members (`ձեռքերը, հագուստը մրոտ`), after interjections and `հա, չէ, լավ` at the start.
- **Բութ** `՝`: a pause where a word is omitted, before an explanation, after an introductory phrase
  (`համոզի՝ տա`, `կանգնած՝ հուսահատված, ապշած`). Never `` ` `` or `'` instead of `՝`.
- **Միջակետ** `․` (not `.`) inside a sentence for lists/abbreviations is optional; don't force it.
- **Չակերտներ** `« »` for titles, songs, quoted words. **Կախման կետեր** `...` (three dots, no space before).
- **Գծիկ / անջատման գիծ**: `—` for a dash with spaces, `-` only inside words (`ինչ-որ`).

## 3. Spelling (ուղղագրություն) and typos (տառասխալ)
- Reformed orthography used in Armenia: `և` (not `եւ`) inside and at the start of words; `ու`, `վ`.
  Names written in the old orthography (`ԵՐԵՒԱՆ, ԼԵՒՈՆ`) are **not** changed silently: one remark per script
  asking whether to unify (`ԵՐԵՎԱՆ, ԼԵՎՈՆ`).
- Missing space before the auxiliary: `գնումէ` → `գնում է`, `էհարվածի` → `է հարվածի`.
- Glued or split words, doubled letters (`ՎՎԻԼՈ`), Latin/Cyrillic letters inside Armenian words (`Rոբը` → `Ռոբը`).
- Case endings and articles in remarks: `վինիլ վրա` → `վինիլի վրա`, `Ռոբերտը արդեն` → `Ռոբերտն արդեն`
  (before a vowel the article is «ն»), `դուրս գա` (after «չի հասցնում») → `դուրս գալ`.
- Proper names start with a capital letter (`(արշակին)` → `(Արշակին)`); a capital after a comma is an error.
- Parentheticals are lowercase except names.

## 4. Meaning and continuity (իմաստ) — remarks
- A character speaks but is not in the scene's cast line; a cast member never appears (only if it looks like an error).
- The same character or place written two ways (`ԼԵՒՈՆ` / `ԼԵՒՈՆԻԿ`, `ՏՆՕՐԵՆ` / `ԾԵՐԱՆՈՑԻ ՏՆՕՐԵՆ`):
  for character cues you may `replace` (they must match), otherwise remark.
- Garbled text (`կանՌոբերտ`): remark with the probable reading.
- Facts that contradict earlier scenes (ages, dates, numbers of years, who knows what), wrong cross-references
  (`Տեսարան 3-ի երգն է`), period tags (`1984Թ` / `ՄԵՐ ՕՐԵՐ`) that don't fit, time of day jumps, duplicated scene numbers.
- Do not critique the story, jokes or structure unless asked.

## 5. Output: corrections JSON (one list per episode)
```json
[
 {"scene": "1", "find": "Ավտոն՞... բերել ես՞", "replace": "Ավտո՞ն... բերե՞լ ես",
  "type": "կետադրություն", "why": "Հարցական նշանը շեշտված ձայնավորի վրա"},
 {"scene": "3", "find": "@ԼԵՒՈՆ", "replace": "@ԼԵՒՈՆԻԿ", "type": "իմաստ", "why": "Նույն կերպարը"},
 {"scene": "2", "find": "Ինչ եք կանՌոբերտ՞", "type": "իմաստ",
  "why": "Տեքստը խառնվել է. հավանաբար՝ «Ի՞նչ եք կանգնել, Ռոբերտ». Անին թող հաստատի"}
]
```
- `scene`: the number between `#…#` in the scene heading of the .fountain file.
- `find`: copied **exactly** from the .fountain (after the automatic fixes), within one line, long enough to be
  unique in the scene (5+ words is safest). Character cues are written with `@` (`"@ԼԵՒՈՆ"`).
- `replace`: the corrected text of the same span. No `replace` = remark only (turquoise in Word).
- `type`: `կետադրություն` · `ուղղագրություն` · `տառասխալ` · `իմաստ`.
- `why`: short, in Armenian; for remarks, the suggested fix.
- `all: true` only for repeated identical errors (e.g. a misspelled name), with or without `scene`.
Work in chunks of ~8 scenes; append to one list; then run proofread.py once.

## 6. What the user receives
- `*_WORK.docx`: working version for Ani: yellow = changed, turquoise = remark, every mark has a Word comment.
- `*_FINAL.pdf`: clean final version in American format with the Maghakian logo (for buyers, crew).
- `*_FINAL.docx / .fdx / .fountain`: clean final text in other formats; `*_corrections.md`: the full table +
  automatic checks. Report numbers: how many fixes by type, and the remarks Ani must decide on.
