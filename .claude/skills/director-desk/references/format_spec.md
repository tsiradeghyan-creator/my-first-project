# Format spec: Ani's house format → American screenplay format

## Ani's house format (KIT Scenarist export, Armenian)
```
Սերիա 1                                   (title line, before the first scene)
1. ՏԵՍԱՐԱՆ                                (scene number; also "15.1 ՏԵՍԱՐԱՆ", "ՏԵՍԱՐԱՆ X /ՍԵՐԻԱ 7/")
ՎԻԼՈՅԻ ՏՈՒՆ։ ՀՅՈՒՐԱՍԵՆՅԱԿ։ ԵՐԵԿՈ          (location: place։ room։ time of day; separators vary: ։ : , . - /)
ՎԻԼՈ, ՍԱՌԱ /ՎԻԼՈՅԻ ԿԻՆ/, ՄԱՍՈՎԿԱ          (cast of the scene; /…/ = description; ՄԱՍՈՎԿԱ = extras)
1984Թ                                     (period super; also ՄԵՐ ՕՐԵՐ, ՖԼԵՇԲԵՔԻ ՍԿԻԶԲ/ԱՎԱՐՏ, ՓԼԵՅՍՄԵՆԹ)
Action paragraph in literary Armenian.
ՎԻԿԱ /ՆԵՂՎԱԾ/                             (character cue; /…/ = parenthetical)
Dialogue /շշուկով Արշակին/ more dialogue,,,  (inline /…/ = parenthetical; ",,," = ellipsis)
ՊԵՐԵԽՈԴ                                   (transition)
```
Time words: ՑԵՐԵԿ, ԵՐԵԿՈ, ԳԻՇԵՐ, ԱՌԱՎՈՏ, ԻՐԻԿՈՒՆ… No INT/EXT in the original: add ՆԵՐՍ. / ԴՐՍ. / ՆԵՐՍ./ԴՐՍ.
(outside: ԴԻՄԱՑ, ԲԱԿ, ՓՈՂՈՑ, ՄՈՏ, ՃԱՆԱՊԱՐՀ, ԾՈՎԱՓ…; inside: rooms, house, restaurant…; ՍԵՆՅԱԿԻ ԴԻՄԱՑ = inside;
car = inside, car at an outside place = both). Mark unsure ones for Ani.

## Fountain (the text format the scripts read)
```
Title: 84-Ի ԱՄԱՌԸ
Credit: Սերիա 1
Author: Անի Մաղաքյան

.ՆԵՐՍ. ՀԱՆՐԱԿԱՑԱՐԱՆԻ ՄԻՋԱՆՑՔ - ԵՐԵԿՈ #1#
= CAST: ՌՈԲԵՐՏ (ԵՐԻՏԱՍԱՐԴ), ԱՐՇԱԿ, ՎԻԿԱ
!1984Թ

Action paragraph.

@ՎԻԿԱ
(նեղված)
Dialogue line.

> ՊԵՐԵԽՈԴ
```
- `.` forces a scene heading; `#N#` = scene number; `= CAST:` is not printed (feeds the breakdown).
- `!` forces an action line (used for supers in capitals); `@` forces a character cue; `>` = transition.
- Blank line between elements; dialogue lines directly under the cue; parentheticals on their own line.

## American layout (what screenplay.py prints)
Letter (A4 on request), Courier-metric 12 pt (FreeMono, has Armenian), 6 lines/inch, 1 page ≈ 1 minute.
Margins: left 1.5", right 1", top/bottom 1". Scene heading and action at 1.5" (60 chars), character cue at 3.7",
parenthetical at 3.1" (24 chars), dialogue at 2.5" (35 chars), transitions flush right. Page numbers top right
from page 2. Split dialogue: (ՇԱՐՈՒՆԱԿԵԼԻ) at the bottom, «NAME (ՇԱՐ.)» on the next page. Scene heading never
alone at the bottom of a page. Title page: logo, title, credit, author, contact, date. Small logo in the footer.
