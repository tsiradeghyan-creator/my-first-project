# -I-

Լուսանկարի կերպարը դարձնում է դերասան. նա քայլում է, վազում, խոսում, թարթում ու ժեստեր անում։ Ամեն ինչ կոդով է, առանց վիդեո գեներատորների ու առանց ինտերնետի։ Կադրը նկարագրում ես մի քանի տողով, ստանում ես MP4՝ ձայնով։

```
-I- 1
size 1280 536
fps 24
letterbox 720

shot 5.5 "Տիգրանը խոսում է"
  actor king ../storyboard/panels/10.png
  king idle
  king say "Մենք չենք նահանջում։ Մենք կվերադառնանք։" at 0.5 pitch 22 speed 120
  camera push 1.05

shot 5.0 "Սուրհանդակը քայլում է"
  actor m ../storyboard/refs/REF_E_king_full_hall.png
  m walk speed 0.8 from 0.3 to 4.8
  camera pan -30 0
```

```
PYTHONPATH=tools/I python -m i run film.i -o film.mp4
PYTHONPATH=tools/I python -m i rig photo.png --debug rig.png     # տես, ինչպես է կմախքը նստել
```

## Ինչպես է աշխատում

1. **Rig (`i/rig.py`).** mediapipe-ի offline մոդելները (մարմնի 33 կետ, սեգմենտացիա, դեմքի 478 կետ) նկարից հանում են կմախքն ու դիմակը։ GrabCut-ը սրում է եզրերը։ Դիմակը լցվում է եռանկյունային ցանցով (~1300 գագաթ, հոդերի մոտ ավելի խիտ), և ամեն գագաթ կշիռ է ստանում մոտակա ոսկորներից (linear blend skinning)։ Կերպարին նկարից ջնջում ենք, իսկ ֆոնը լրացնում ենք FSR inpaint-ով։ Rig-ը cache է արվում `.i_cache/`-ում։
2. **Motion (`i/motion.py`).** 2D forward kinematics + skinning։ Շարժման գրադարան. `idle`, `walk` (պրոֆիլով և դեմքով դեպի կամերան), `run`, `raise_arm`, `point`, `look`, `nod`, `crouch`։ Clip-երը շերտավորվում են fade-երով, իսկ քայլքով անցած ճանապարհը պահպանվում է։
3. **Face (`i/face.py`).** դեմքի ցանցը շարժում է ծնոտն ու շուրթերը (visemes), կոպերն ու հոնքերը։ Բերանը բացվում է նկարված խոռոչի վրա՝ ատամների ակնարկով։ Ավտոմատ թարթում է ամեն 2.4–4.8 վայրկյանը մեկ։
4. **Voice (`i/voice.py`).** խոսքը սինթեզվում է espeak-ng-ով (արևելահայերեն, `voice en` և այլն), կամ վերցվում է պատրաստի ֆայլից (`wav file.wav`, օրինակ ElevenLabs)։ Շուրթերի ժամանակացույցը կազմվում է տեքստի տառերից (հայերեն viseme աղյուսակով) և ձայնի ամպլիտուդից։
5. **Scene (`i/scene.py`).** -I- լեզուն, կամերան (push, pan, shake), letterbox-ը և ձայնի միքսը։ Ռենդերը skia-ով է (textured triangles)։

## Լեզվի տեղեկատու

| Հրաման | Իմաստ |
|---|---|
| `size W H`, `fps N`, `letterbox H` | ձևաչափ |
| `shot DUR "Անուն"` | նոր կադր |
| `actor NAME IMAGE [at X Y] [scale S]` | դերասան նկարից (rig-ը ավտոմատ է), լռությամբ լցնում է կադրը |
| `bg IMAGE` | այլ ֆոն (մաքուր plate) |
| `NAME idle` | շնչառություն, միկրոշարժումներ |
| `NAME walk [speed S] [stride K] [direction right/left] from T0 to T1` | քայլք |
| `NAME run ...` | վազք |
| `NAME raise_arm side r/l from T0 to T1` | ձեռքը բարձրացնել (նշան) |
| `NAME point side r/l`, `look ANGLE`, `nod`, `crouch [depth D]` | ժեստեր |
| `NAME say "ՏԵՔՍՏ" at T [voice hy] [pitch P] [speed S] [wav FILE]` | խոսք + lip-sync |
| `NAME blink at T`, `NAME brow from T0 to T1`, `NAME still` | աչքեր, հոնքեր, առանց ավտոթարթման |
| `camera push F`, `camera pan DX DY`, `camera shake A` | կամերա (կադրի ընթացքում, ease-ով) |
| `fade F` | clip-ի մուտք/ելք (վայրկյան) |

## Տեղադրում
Python 3.12 (mediapipe 0.10.14-ն ունի ներկառուցված մոդելներ). `pip install mediapipe==0.10.14 skia-python scipy soundfile opencv-contrib-python-headless`, համակարգում՝ `espeak-ng` և `ffmpeg`։

## Ինչ է հիմա լավ ստացվում, ինչ՝ ոչ (0.1)
- **Լավ.** խոսքը front կամ 3/4 դեմքով close-up-ում, թարթումը, պրոֆիլով քայլքը, դեմքով դեպի կամերան քայլքը, idle-ը, կամերան։
- **Սահմանափակ.** թիկնոցների ու երկար զգեստների տակ ձեռքերը չեն կարող ազատ բարձրանալ (գործվածքը ձգվում է)։ Երբ կերպարը հեռանում է իր տեղից, ֆոնի բացը լցվում է մշուշոտ, դրա համար լավագույնը մաքուր `bg` տալն է։ Պրոֆիլով դեմքը (պանել 14) չի ճանաչվում։
- **Հաջորդ քայլերը.** ձեռքով հոդեր նշելու տարբերակ (`joints_override`, արդեն կա API-ում), ձիու/քառոտանու rig, շերտավոր զգեստ (թիկնոցն առանձին ֆիզիկայով), գլխի պտույտ 3/4-ից, mocap վիդեոյից (pose-ը վիդեոյից → կերպարին)։
