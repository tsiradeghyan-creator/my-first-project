import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, Freeze, Img, Sequence, continueRender, delayRender, interpolate, random, staticFile, useCurrentFrame, Easing} from 'remotion';
import {Defs, Paper, Stroke, Arrow, Scribble, RedBlock, Brackets, Wipe} from './Drama';

const INK = '#111111', RED = '#D90429', GREY = '#8a857d', PAPER = '#F3F1EC';
const SERIF = 'ArmSerif, DejaVu Serif', SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const outx = Easing.bezier(0.16, 1, 0.3, 1);
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = outx) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});

// ---------- timeline ----------
export const ST = {hook: 0, e1: 105, e2: 255, e3: 390, e4: 570, e5: 735, rw: 900, rc: 975, sum: 1305, end: 1425};
export const S_TOTAL = 1545;
const RC_STEP = 66;

// narration (on-screen story text + recording script)
export const NARR = [
  {at: 0, text: 'Այս պատմությունը 30 վայրկյան է։', sub: 'Վերջում կհասկանաս՝ ինչու չկարողացար կտրվել։'},
  {at: ST.e1, text: 'Սա Լիլիթն է։', sub: 'Նա երազում է երգել մեծ բեմում։'},
  {at: ST.e2, text: 'Մի օր մրցույթ են հայտարարում՝', sub: 'վաղը, ժամը յոթին։'},
  {at: ST.e3, text: 'Առավոտյան Լիլիթը ձայնը կորցնում է։', sub: 'Իսկ դահլիճում արդեն հազար մարդ է։'},
  {at: ST.e4, text: 'Վարագույրը բացվում է։', sub: 'Լույս։ Լռություն։'},
  {at: ST.e5, text: 'Եվ նա երգում է՝', sub: 'կոտրված ձայնով, բայց առաջին անգամ՝ առանց վախի։'},
];
const TERMS = [
  {n: '01', t: 'Էքսպոզիցիա', d: 'ով է հերոսը և ինչ է ուզում'},
  {n: '02', t: 'Հանգույց', d: 'դեպքը, որ սկսում է պատմությունը'},
  {n: '03', t: 'Զարգացում', d: 'խոչընդոտներ, խաղադրույքը մեծանում է'},
  {n: '04', t: 'Գագաթնակետ', d: 'ամենաբարձր լարումը'},
  {n: '05', t: 'Հանգուցալուծում', d: 'հերոսն այլևս նույնը չէ'},
];

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const fs = [
      new FontFace('ArmSerif', `url(${staticFile('dr/NotoSerifArm.ttf')})`, {weight: '100 900', stretch: '62.5% 100%'}),
      new FontFace('ArmSans', `url(${staticFile('dr/NotoArm.ttf')})`, {weight: '100 900', stretch: '62.5% 100%'}),
    ];
    Promise.all(fs.map((x) => x.load())).then((l) => { l.forEach((x) => (document as any).fonts.add(x)); continueRender(h); });
  }, [h]);
};
const serif = (s: number, c = INK, w = 600): React.CSSProperties => ({fontFamily: SERIF, fontWeight: w, fontSize: s, color: c, lineHeight: 1.08});
const sans = (s: number, c = INK, w = 600, track = 0.16): React.CSSProperties => ({fontFamily: SANS, fontWeight: w, fontSize: s, color: c, letterSpacing: s * track});

// ---------- kinetic story text: words pop in one by one ----------
const Words: React.FC<{text: string; size: number; color?: string; d?: number; rate?: number; w?: number; hi?: string[]}> = ({text, size, color = INK, d = 0, rate = 3, w = 700, hi = []}) => {
  const f = useCurrentFrame();
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', gap: `0 ${size * 0.26}px`}}>
      {text.split(' ').map((word, i) => {
        const p = pr(f, d + i * rate, d + i * rate + 12);
        const isHi = hi.some((h) => word.includes(h));
        return <span key={i} style={{...serif(size, isHi ? RED : color, w), display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 40}px) rotate(${(1 - p) * (i % 2 ? 6 : -6)}deg) scale(${1 + (1 - p) * 0.3})`}}>{word}</span>;
      })}
    </div>
  );
};
const StoryText: React.FC<{i: number; hi?: string[]; light?: boolean}> = ({i, hi, light}) => {
  const n = NARR[i];
  return (
    <div style={{position: 'absolute', left: 80, right: 140, top: 230}}>
      <Words text={n.text} size={86} d={4} hi={hi} color={light ? PAPER : INK} />
      <div style={{height: 18}} />
      <Words text={n.sub} size={56} d={4 + n.text.split(' ').length * 3 + 10} w={400} color={light ? '#cfcac0' : GREY} hi={hi} />
    </div>
  );
};

// ---------- doodle layer ----------
const SketchDefs: React.FC = () => (
  <svg width="0" height="0" style={{position: 'absolute'}}><defs>
    <filter id="sketch" filterUnits="userSpaceOnUse" x="-400" y="-400" width="1900" height="2800">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="7" result="t" />
      <feDisplacementMap in="SourceGraphic" in2="t" scale="6" />
    </filter>
  </defs></svg>
);
const P: React.FC<{d: string; p: number; w?: number; c?: string; fill?: string}> = ({d, p, w = 6, c = INK, fill = 'none'}) =>
  <path d={d} pathLength={1} strokeDasharray={`${Math.max(0.0001, p)} 2`} stroke={c} strokeWidth={w} fill={fill} strokeLinecap="round" strokeLinejoin="round" />;
const Layer: React.FC<{children: React.ReactNode}> = ({children}) =>
  <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}><g filter="url(#sketch)">{children}</g></svg>;

type Mouth = 'smile' | 'flat' | 'open' | 'sad';
const Lilit: React.FC<{x: number; y: number; s?: number; p: number; mouth?: Mouth; arms?: 'down' | 'up' | 'throat'; color?: string}> = ({x, y, s = 1, p, mouth = 'smile', arms = 'down', color = INK}) => {
  const q = (a: number, b: number) => interpolate(p, [a, b], [0, 1], clamp);
  const armL = arms === 'up' ? 'M -15 100 C -70 60, -110 0, -120 -50' : arms === 'throat' ? 'M -15 100 C -60 120, -40 80, -8 70' : 'M -15 100 C -60 160, -80 200, -70 240';
  const armR = arms === 'up' ? 'M 15 100 C 70 60, 110 0, 120 -50' : arms === 'throat' ? 'M 15 100 C 60 120, 40 80, 8 72' : 'M 15 100 C 60 160, 80 200, 70 240';
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <P d="M 58 0 A 58 58 0 1 1 -58 0 A 58 58 0 1 1 58 0" p={q(0, 0.25)} c={color} />
      <P d="M -62 -8 C -72 -84, 60 -100, 64 -14" p={q(0.15, 0.35)} w={9} c={color} />
      <P d="M 52 -44 C 116 -44, 126 18, 98 62" p={q(0.25, 0.42)} w={9} c={color} />
      <P d="M 0 58 L 0 86" p={q(0.35, 0.45)} c={color} />
      <P d="M -22 86 L 22 86 L 80 300 L -80 300 Z" p={q(0.4, 0.65)} c={color} fill={p > 0.7 ? RED : 'none'} />
      <P d={armL} p={q(0.55, 0.72)} c={color} />
      <P d={armR} p={q(0.6, 0.77)} c={color} />
      <P d="M -30 300 L -36 410 L -60 412" p={q(0.7, 0.85)} c={color} />
      <P d="M 30 300 L 36 410 L 60 412" p={q(0.75, 0.9)} c={color} />
      {p > 0.85 && <><circle cx={-20} cy={-4} r={5} fill={color} /><circle cx={20} cy={-4} r={5} fill={color} /></>}
      {p > 0.9 && (mouth === 'smile' ? <P d="M -18 22 Q 0 38 18 22" p={1} w={5} c={color} />
        : mouth === 'flat' ? <P d="M -14 28 L 14 28" p={1} w={5} c={color} />
        : mouth === 'sad' ? <P d="M -16 32 Q 0 20 16 32" p={1} w={5} c={color} />
        : <ellipse cx={0} cy={28} rx={11} ry={15} fill={color} />)}
    </g>
  );
};
const Mic: React.FC<{x: number; y: number; p: number; s?: number; color?: string}> = ({x, y, p, s = 1, color = INK}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <P d="M 0 0 L 0 250" p={interpolate(p, [0, 0.5], [0, 1], clamp)} c={color} />
    <P d="M -50 250 L 50 250" p={interpolate(p, [0.4, 0.7], [0, 1], clamp)} c={color} />
    <P d="M 20 -22 A 20 26 0 1 1 -20 -22 A 20 26 0 1 1 20 -22" p={interpolate(p, [0.5, 1], [0, 1], clamp)} c={color} fill={p > 0.95 ? color : 'none'} />
  </g>
);

// ---------- story scenes ----------
const E1: React.FC = () => {
  const f = useCurrentFrame();
  const bub = pr(f, 60, 90);
  return (
    <AbsoluteFill>
      <Paper /><SketchDefs />
      <StoryText i={1} hi={['Լիլիթն']} />
      <Layer>
        <Lilit x={330} y={1020} p={pr(f, 6, 60, io)} />
        {/* thought bubble with a stage */}
        <circle cx={450} cy={900} r={10 * bub} fill="none" stroke={INK} strokeWidth={5} />
        <circle cx={500} cy={850} r={16 * bub} fill="none" stroke={INK} strokeWidth={5} />
        <P d="M 560 820 C 520 720, 600 640, 680 670 C 720 590, 860 600, 880 680 C 980 690, 990 820, 900 840 C 880 900, 720 910, 680 860 C 600 900, 540 870, 560 820 Z" p={pr(f, 66, 96, io)} />
        <P d="M 640 820 L 640 700 L 920 700 L 920 820" p={pr(f, 84, 104)} w={4} />
        <RedCurtain x={644} y={702} w={136} h={116} p={pr(f, 92, 108)} />
        <RedCurtain x={784} y={702} w={134} h={116} p={pr(f, 92, 108)} />
        <Mic x={780} y={770} s={0.22} p={pr(f, 100, 120)} />
      </Layer>
    </AbsoluteFill>
  );
};
const RedCurtain: React.FC<{x: number; y: number; w: number; h: number; p: number}> = ({x, y, w, h, p}) =>
  <rect x={x} y={y} width={w} height={h * p} fill={RED} opacity={0.85} />;

const E2: React.FC = () => {
  const f = useCurrentFrame();
  const slap = pr(f, 20, 30, Easing.out(Easing.back(2)));
  const hand = interpolate(f, [40, 135], [0, 210], clamp);
  return (
    <AbsoluteFill>
      <Paper /><SketchDefs />
      <StoryText i={2} hi={['մրցույթ', 'յոթին']} />
      <div style={{position: 'absolute', left: 120, top: 760, width: 520, height: 640, transform: `rotate(-5deg) scale(${interpolate(slap, [0, 1], [2.2, 1])})`, opacity: Math.min(1, slap * 2)}}>
        <div style={{position: 'absolute', inset: 0, background: RED, filter: 'url(#rough)'}} />
        <div style={{position: 'absolute', left: 40, top: 60, ...serif(74, PAPER, 800)}}>ՄՐՑՈՒՅԹ</div>
        <div style={{position: 'absolute', left: 44, top: 200, ...sans(30, PAPER, 600)}}>ԵՐԳԻ · ԲԵՄ · ՀԱՆԴԻՍԱՏԵՍ</div>
        <div style={{position: 'absolute', left: 40, top: 400, ...serif(150, PAPER, 800)}}>19:00</div>
        <div style={{position: 'absolute', left: 44, top: 570, ...sans(30, PAPER, 600)}}>ՎԱՂԸ</div>
      </div>
      <Layer>
        <P d="M 940 1040 A 150 150 0 1 1 640 1040 A 150 150 0 1 1 940 1040" p={pr(f, 30, 60, io)} w={7} />
        {[...Array(12)].map((_, i) => { const a = (i / 12) * Math.PI * 2; return <line key={i} x1={790 + Math.cos(a) * 130} y1={1040 + Math.sin(a) * 130} x2={790 + Math.cos(a) * 145} y2={1040 + Math.sin(a) * 145} stroke={INK} strokeWidth={5} opacity={pr(f, 50, 60)} />; })}
        <line x1={790} y1={1040} x2={790 + Math.sin((hand * Math.PI) / 180) * 100} y2={1040 - Math.cos((hand * Math.PI) / 180) * 100} stroke={RED} strokeWidth={8} strokeLinecap="round" opacity={pr(f, 50, 60)} />
        <line x1={790} y1={1040} x2={790} y2={960} stroke={INK} strokeWidth={8} strokeLinecap="round" opacity={pr(f, 50, 60)} />
        <Lilit x={820} y={1330} s={0.42} p={pr(f, 40, 70, io)} arms="up" />
      </Layer>
    </AbsoluteFill>
  );
};
const E3: React.FC = () => {
  const f = useCurrentFrame();
  const count = Math.round(interpolate(f, [70, 160], [0, 1000], {...clamp, easing: Easing.in(Easing.quad)}));
  const heads = Math.floor(interpolate(f, [70, 160], [0, 60], clamp));
  const shake = f > 150 ? (random(`e3${f}`) - 0.5) * 6 : 0;
  return (
    <AbsoluteFill style={{transform: `translateX(${shake}px)`}}>
      <Paper /><SketchDefs />
      <StoryText i={3} hi={['ձայնը', 'հազար']} />
      <Layer>
        <Lilit x={250} y={880} s={0.85} p={1} mouth="sad" arms="throat" />
        <Scribble cx={250} cy={945} rx={40} ry={18} p={pr(f, 14, 40)} />
        <Mic x={450} y={980} s={0.6} p={1} />
        <P d="M 400 900 L 500 1000 M 500 900 L 400 1000" p={pr(f, 34, 50)} w={14} c={RED} />
        {/* audience filling the hall */}
        {[...Array(60)].map((_, i) => {
          const col = i % 10, row = Math.floor(i / 10);
          const on = i < heads;
          return <g key={i} opacity={on ? 1 : 0}>
            <circle cx={120 + col * 92 + (row % 2) * 40} cy={1250 + row * 52} r={18} fill="none" stroke={INK} strokeWidth={4} />
            <path d={`M ${100 + col * 92 + (row % 2) * 40} ${1290 + row * 52} Q ${120 + col * 92 + (row % 2) * 40} ${1268 + row * 52} ${140 + col * 92 + (row % 2) * 40} ${1290 + row * 52}`} fill="none" stroke={INK} strokeWidth={4} />
          </g>;
        })}
      </Layer>
      <div style={{position: 'absolute', right: 150, top: 830, textAlign: 'right', opacity: pr(f, 66, 76)}}>
        <div style={{...serif(150, RED, 800)}}>{count}</div>
        <div style={{...sans(26, GREY)}}>ՀԱՆԴԻՍԱՏԵՍ</div>
      </div>
    </AbsoluteFill>
  );
};
const E4: React.FC = () => {
  const f = useCurrentFrame();
  const open = pr(f, 50, 100, io);
  const light = pr(f, 90, 110);
  const beat = Math.abs(Math.sin(f / 7)) ** 8;
  return (
    <AbsoluteFill style={{background: INK}}>
      <SketchDefs />
      {/* spotlight */}
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#fff" stopOpacity={0.0} /><stop offset="1" stopColor="#fff8e8" stopOpacity={0.55} /></linearGradient></defs>
        <polygon points="500,600 580,600 820,1450 260,1450" fill="url(#beam)" opacity={light} />
        <ellipse cx={540} cy={1450} rx={290} ry={46} fill="#fff8e8" opacity={0.5 * light} />
      </svg>
      <Layer><Lilit x={540} y={1030} s={0.9} p={pr(f, 80, 110)} mouth="flat" color={PAPER} /><Mic x={540} y={1100} s={0.45} p={pr(f, 90, 110)} color={PAPER} /></Layer>
      {/* curtains */}
      <div style={{position: 'absolute', left: -540 * open, top: 520, width: 560, height: 1100, background: RED, filter: 'url(#rough)'}} />
      <div style={{position: 'absolute', left: 520 + 540 * open, top: 520, width: 560, height: 1100, background: RED, filter: 'url(#rough)'}} />
      {[...Array(6)].map((_, i) => <div key={i} style={{position: 'absolute', left: -540 * open + i * 92 + 30, top: 520, width: 3, height: 1100, background: 'rgba(0,0,0,0.25)'}} />)}
      {[...Array(6)].map((_, i) => <div key={i} style={{position: 'absolute', left: 520 + 540 * open + i * 92 + 30, top: 520, width: 3, height: 1100, background: 'rgba(0,0,0,0.25)'}} />)}
      <StoryText i={4} hi={['Լռություն']} light />
      {/* heartbeat ring in the silence */}
      {f > 115 && <div style={{position: 'absolute', left: 540 - 60 - beat * 30, top: 1660 - beat * 30, width: 120 + beat * 60, height: 120 + beat * 60, borderRadius: '50%', border: `3px solid ${RED}`, opacity: 0.8 - beat * 0.6}} />}
    </AbsoluteFill>
  );
};
const E5: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: INK}}>
      <SketchDefs />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <polygon points="500,600 580,600 820,1450 260,1450" fill="#fff8e8" opacity={0.22} />
      </svg>
      <Layer>
        <Lilit x={540} y={1030} s={0.9} p={1} mouth={f % 20 < 14 ? 'open' : 'smile'} arms={f > 60 ? 'up' : 'down'} color={PAPER} />
        <Mic x={540} y={1100} s={0.45} p={1} color={PAPER} />
        {/* sound waves */}
        {[0, 1, 2, 3, 4].map((k) => {
          const t = ((f + k * 12) % 60) / 60;
          const r = 80 + t * 380;
          return <g key={k} opacity={(1 - t) * pr(f, 6, 20)}>
            <path d={`M ${540 + r * Math.cos(-0.6)} ${1060 + r * Math.sin(-0.6)} A ${r} ${r} 0 0 1 ${540 + r * Math.cos(0.6)} ${1060 + r * Math.sin(0.6)}`} stroke={RED} strokeWidth={8} fill="none" />
            <path d={`M ${540 - r * Math.cos(-0.6)} ${1060 + r * Math.sin(-0.6)} A ${r} ${r} 0 0 0 ${540 - r * Math.cos(0.6)} ${1060 + r * Math.sin(0.6)}`} stroke={RED} strokeWidth={8} fill="none" />
          </g>;
        })}
        {/* audience lights up */}
        {[...Array(30)].map((_, i) => {
          const on = pr(f, 50 + (i % 10) * 4 + Math.floor(i / 10) * 6, 60 + (i % 10) * 4 + Math.floor(i / 10) * 6);
          return <circle key={i} cx={110 + (i % 10) * 95 + (Math.floor(i / 10) % 2) * 40} cy={1560 + Math.floor(i / 10) * 60} r={20} fill={on > 0.5 ? '#fff8e8' : 'none'} stroke={PAPER} strokeWidth={3} opacity={0.4 + on * 0.6} />;
        })}
      </Layer>
      <StoryText i={5} hi={['առանց', 'վախի']} light />
    </AbsoluteFill>
  );
};

// ---------- scene snapshots (for rewind + recap) ----------
const SNAP: {C: React.FC; frame: number}[] = [
  {C: E1, frame: 140}, {C: E2, frame: 120}, {C: E3, frame: 170}, {C: E4, frame: 150}, {C: E5, frame: 140},
];
const Snap: React.FC<{i: number; w: number}> = ({i, w}) => {
  const S = SNAP[i];
  const s = w / 1080;
  return (
    <div style={{width: w, height: 1920 * s, overflow: 'hidden', position: 'relative', background: PAPER}}>
      <div style={{width: 1080, height: 1920, transform: `scale(${s})`, transformOrigin: 'top left', position: 'absolute'}}>
        <Freeze frame={S.frame}><S.C /></Freeze>
      </div>
    </div>
  );
};

// ---------- rewind (VHS) ----------
const Rewind: React.FC = () => {
  const f = useCurrentFrame();
  const idx = 4 - Math.min(4, Math.floor(f / 12));
  const jitter = (random(`rw${f}`) - 0.5) * 30;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <div style={{position: 'absolute', left: 0, top: 0, transform: `translateX(${jitter}px) skewX(${jitter * 0.2}deg)`, filter: 'contrast(1.3) saturate(0.6)'}}>
        <Snap i={idx} w={1080} />
      </div>
      <AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.25) 0 2px, rgba(0,0,0,0) 2px 6px)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: (f * 37) % 1920, height: 60, background: 'rgba(255,255,255,0.18)', filter: 'blur(4px)'}} />
      <div style={{position: 'absolute', left: 80, top: 160, ...sans(64, '#fff', 800, 0.05), textShadow: '0 0 12px rgba(0,0,0,0.6)'}}>◀◀ ՆՈՐԻՑ</div>
      <div style={{position: 'absolute', right: 150, top: 175, ...sans(40, '#fff', 600, 0.05)}}>00:{String(30 - Math.floor(f / 2.5)).padStart(2, '0')}</div>
    </AbsoluteFill>
  );
};

// ---------- recap: each scene gets its name ----------
const Recap: React.FC = () => {
  const f = useCurrentFrame();
  const i = Math.min(4, Math.floor(f / RC_STEP));
  const lf = f - i * RC_STEP;
  const t = TERMS[i];
  const pop = pr(lf, 0, 14);
  return (
    <AbsoluteFill>
      <Paper />
      <div style={{position: 'absolute', left: 80, top: 160, display: 'flex', alignItems: 'center', gap: 18}}>
        <div style={{width: 60, height: 4, background: RED}} />
        <span style={sans(26)}>ԻՍԿ ՀԻՄԱ՝ ԴԱՆԴԱՂ</span>
      </div>
      {/* thumbnail of that moment */}
      <div style={{position: 'absolute', left: 110, top: 260, transform: `rotate(${i % 2 ? 2.5 : -2.5}deg) scale(${0.9 + pop * 0.1})`, opacity: pop, boxShadow: '0 20px 50px rgba(0,0,0,0.25)'}}>
        <Snap i={i} w={500} />
      </div>
      <Brackets x={110} y={260} w={500} h={889} p={pop} color={RED} />
      {/* big outlined number */}
      <div style={{position: 'absolute', left: 660, top: 300, ...serif(220, 'transparent', 400), WebkitTextStroke: `2px ${INK}`, opacity: pop}}>{t.n}</div>
      {/* term stamp */}
      <div style={{position: 'absolute', left: 80, right: 140, top: 1210, transform: `scale(${interpolate(pop, [0, 1], [1.8, 1])})`, transformOrigin: 'left center', opacity: pop}}>
        <div style={{...serif(Math.min(130, 900 / ([...t.t].length * 0.68)), i === 3 ? RED : INK, 800)}}>{t.t}</div>
        <div style={{...serif(54, GREY, 400), marginTop: 14}}>{t.d}</div>
      </div>
      {/* progress curve along the bottom */}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d="M 100 1640 L 260 1630 L 420 1560 L 600 1500 L 760 1420 L 940 1600" fill="none" stroke="rgba(17,17,17,0.12)" strokeWidth={6} />
        <path d="M 100 1640 L 260 1630 L 420 1560 L 600 1500 L 760 1420 L 940 1600" pathLength={1} strokeDasharray={`${(i + pop) / 5} 2`} fill="none" stroke={RED} strokeWidth={8} strokeLinecap="round" filter="url(#rough)" />
        {[[260, 1630], [420, 1560], [600, 1500], [760, 1420], [940, 1600]].map(([x, y], k) => <circle key={k} cx={x} cy={y} r={k <= i ? 12 : 7} fill={k <= i ? (k === i ? RED : INK) : 'rgba(17,17,17,0.2)'} />)}
      </svg>
    </AbsoluteFill>
  );
};

// ---------- hook / summary / end ----------
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <div style={{position: 'absolute', left: 80, top: 160, display: 'flex', alignItems: 'center', gap: 18, opacity: pr(f, 0, 10)}}>
        <div style={{width: 60, height: 4, background: RED}} /><span style={sans(26)}>ՍՑԵՆԱՐԻ ԴԱՍ · 01</span>
      </div>
      <div style={{position: 'absolute', left: 80, right: 140, top: 560}}>
        <Words text="Այս պատմությունը" size={104} d={2} rate={4} />
        <Words text="30 վայրկյան է։" size={118} d={12} rate={4} hi={['30']} />
        <div style={{height: 40}} />
        <Words text="Վերջում կհասկանաս՝ ինչու չկարողացար կտրվել։" size={58} d={40} rate={3} w={400} color={GREY} />
      </div>
      <Stroke d="M 80 940 C 300 915, 520 955, 700 925" p={pr(f, 28, 42)} color={RED} w={18} brush />
    </AbsoluteFill>
  );
};
const Summary: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <div style={{position: 'absolute', left: 80, top: 380}}><Words text="Սա" size={70} d={2} w={400} color={GREY} /></div>
      <div style={{position: 'absolute', left: 80, top: 470}}><Words text="դրամատուրգիան" size={104} d={6} color={RED} /></div>
      <div style={{position: 'absolute', left: 80, top: 590}}><Words text="է՝ պատմության" size={104} d={14} /></div>
      <div style={{position: 'absolute', left: 80, top: 710}}><Words text="կմախքը։" size={104} d={22} /></div>
      <Stroke d="M 80 850 C 260 830, 420 860, 560 838" p={pr(f, 34, 46)} color={INK} w={12} brush />
      <div style={{position: 'absolute', left: 80, right: 140, top: 960}}>
        <Words text="Առանց դրա կա միայն դեպքերի թվարկում։" size={58} d={50} w={400} color={GREY} />
      </div>
    </AbsoluteFill>
  );
};
const End: React.FC = () => {
  const f = useCurrentFrame();
  const reveal = pr(f, 30, 62, io);
  return (
    <AbsoluteFill>
      <Paper />
      <div style={{position: 'absolute', left: 80, top: 300}}>
        <Words text="Հաջորդ դասը՝" size={60} d={2} w={400} color={GREY} />
        <Words text="կոնֆլիկտ" size={150} d={8} hi={['կոնֆլիկտ']} />
      </div>
      <div style={{position: 'absolute', left: 140, top: 600, width: 800, height: 800, clipPath: `inset(0 ${(1 - reveal) * 100}% 0 0)`}}>
        <Img src={staticFile('dr/logo.svg')} style={{width: 800, height: 800}} />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1260, textAlign: 'center', ...sans(26), opacity: pr(f, 60, 74)}}>MAGHAKIANSCRIPTS.COM</div>
    </AbsoluteFill>
  );
};

export const StoryLesson: React.FC = () => {
  useFonts();
  const S = (a: number, b: number, el: React.ReactNode) => <Sequence from={a} durationInFrames={b - a}>{el}</Sequence>;
  return (
    <AbsoluteFill style={{background: PAPER}}>
      <Defs />
      <Audio src={staticFile('dr/story_mix.wav')} />
      {S(ST.hook, ST.e1, <Hook />)}
      {S(ST.e1, ST.e2, <E1 />)}
      {S(ST.e2, ST.e3, <E2 />)}
      {S(ST.e3, ST.e4, <E3 />)}
      {S(ST.e4, ST.e5, <E4 />)}
      {S(ST.e5, ST.rw, <E5 />)}
      {S(ST.rw, ST.rc, <Rewind />)}
      {S(ST.rc, ST.sum, <Recap />)}
      {S(ST.sum, ST.end, <Summary />)}
      {S(ST.end, S_TOTAL, <End />)}
      {[ST.e1, ST.e2, ST.e3, ST.rc, ST.sum, ST.end].map((t, i) => <Sequence key={t} from={t - 9} durationInFrames={18}><Wipe color={i % 2 ? RED : INK} /></Sequence>)}
    </AbsoluteFill>
  );
};
