import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, Img, Sequence, continueRender, delayRender, interpolate, random, staticFile, useCurrentFrame, Easing} from 'remotion';
import {Defs, Paper, Stroke, Arrow, Scribble, RedBlock, Brackets, Wipe} from './Drama';

const INK = '#111111', RED = '#D90429', GREY = '#8a857d';
const SERIF = 'ArmSerif, DejaVu Serif', SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const outx = Easing.bezier(0.16, 1, 0.3, 1);
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = outx) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});

// ---------- timeline (frames @30) ----------
const T = {hook: 0, title: 150, conflict: 345, curve: 510, flat: 1050, end: 1185};
export const L_TOTAL = 1350;
const STAGE = 108;

// narration = subtitles (and the recording script)
export const LINES: {at: number; to: number; text: string}[] = [
  {at: 8, to: 145, text: 'Ինչո՞ւ մի ֆիլմը նայում ես մինչև վերջ, իսկ մյուսն անջատում ես հինգերորդ րոպեին։'},
  {at: 158, to: 250, text: 'Պատասխանը դրամատուրգիան է՝ պատմությունը կառուցելու արվեստը։'},
  {at: 255, to: 340, text: 'Հունարեն «դրամա» նշանակում է գործողություն։'},
  {at: 352, to: 505, text: 'Ամեն դրամա սկսվում է կոնֆլիկտից. հերոսը ինչ-որ բան ուզում է, ինչ-որ բան խանգարում է։'},
  {at: 514, to: 615, text: 'Էքսպոզիցիա․ ծանոթանում ենք հերոսին և նրա աշխարհին։'},
  {at: 622, to: 723, text: 'Հանգույց․ մի դեպք խախտում է հավասարակշռությունը։'},
  {at: 730, to: 831, text: 'Զարգացում․ խոչընդոտները շատանում են, խաղադրույքը՝ մեծանում։'},
  {at: 838, to: 939, text: 'Գագաթնակետ․ ամենաբարձր լարումը, որոշման պահը։'},
  {at: 946, to: 1045, text: 'Հանգուցալուծում․ հերոսն այլևս նույնը չէ։'},
  {at: 1058, to: 1180, text: 'Առանց կոնֆլիկտի դրամա չկա։ Կա միայն դեպքերի թվարկում։'},
  {at: 1192, to: 1345, text: 'Հաջորդ դասին՝ կոնֆլիկտի տեսակները։'},
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

const serif = (s: number, c = INK, w = 500): React.CSSProperties => ({fontFamily: SERIF, fontWeight: w, fontSize: s, color: c, lineHeight: 1.0, letterSpacing: -s * 0.01});
const sans = (s: number, c = INK, w = 600, track = 0.18): React.CSSProperties => ({fontFamily: SANS, fontWeight: w, fontSize: s, color: c, letterSpacing: s * track});

const Scatter: React.FC<{text: string; x: number; y: number; size: number; d?: number; color?: string; w?: number; seed?: string}> = ({text, x, y, size, d = 0, color = INK, w = 600, seed = 's'}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: x, top: y, display: 'flex', whiteSpace: 'pre'}}>
      {[...text].map((ch, i) => {
        const p = pr(f, d + i * 1.4, d + i * 1.4 + 20);
        const dx = (random(`${seed}x${i}`) - 0.5) * 700 * (1 - p), dy = (random(`${seed}y${i}`) - 0.5) * 500 * (1 - p);
        const r = (random(`${seed}r${i}`) - 0.5) * 90 * (1 - p);
        return <span key={i} style={{...serif(size, color, w), display: 'inline-block', opacity: Math.min(1, p * 2.5), transform: `translate(${dx}px,${dy}px) rotate(${r}deg) scale(${1 + (1 - p) * 0.8})`}}>{ch}</span>;
      })}
    </div>
  );
};
const Rise: React.FC<{d?: number; x: number; y: number; children: React.ReactNode; out?: number; w?: number}> = ({d = 0, x, y, children, out, w}) => {
  const f = useCurrentFrame();
  const p = pr(f, d, d + 16);
  const o = out ? 1 - pr(f, out - 8, out, io) : 1;
  return <div style={{position: 'absolute', left: x, top: y, width: w, opacity: p * o, transform: `translateY(${(1 - p) * 30}px)`}}>{children}</div>;
};
const Kicker: React.FC<{text: string}> = ({text}) => {
  const f = useCurrentFrame();
  const l = pr(f, 0, 14);
  return (
    <div style={{position: 'absolute', left: 90, top: 200, display: 'flex', alignItems: 'center', gap: 20, opacity: l}}>
      <div style={{width: 70 * l, height: 4, background: RED}} />
      <span style={sans(26)}>{text}</span>
    </div>
  );
};

// subtitles: the narration, word by word (works muted)
const Subs: React.FC = () => {
  const f = useCurrentFrame();
  const line = LINES.find((l) => f >= l.at && f < l.to);
  if (!line) return null;
  const words = line.text.split(' ');
  const span = Math.max(1, (line.to - line.at - 14) / words.length);
  const o = 1 - pr(f, line.to - 6, line.to, io);
  return (
    <div style={{position: 'absolute', left: 90, right: 150, top: 1450, opacity: o}}>
      <div style={{display: 'flex', flexWrap: 'wrap', gap: '6px 14px'}}>
        {words.map((w, i) => {
          const p = pr(f, line.at + i * span * 0.6, line.at + i * span * 0.6 + 8);
          return <span key={i} style={{...sans(44, INK, 500, 0), lineHeight: 1.3, opacity: 0.25 + 0.75 * p}}>{w}</span>;
        })}
      </div>
    </div>
  );
};

// ---------- S1 hook ----------
const FilmCard: React.FC<{x: number; y: number; p: number; label: string; bad?: boolean; mark: number}> = ({x, y, p, label, bad, mark}) => (
  <div style={{position: 'absolute', left: x, top: y, width: 380, height: 300, opacity: p, transform: `translateY(${(1 - p) * 80}px) rotate(${bad ? 3 : -3}deg)`}}>
    <div style={{position: 'absolute', inset: 0, background: INK, borderRadius: 8}} />
    {Array.from({length: 7}).map((_, i) => <React.Fragment key={i}>
      <div style={{position: 'absolute', left: 18 + i * 52, top: 14, width: 26, height: 18, background: '#F3F1EC', borderRadius: 3}} />
      <div style={{position: 'absolute', left: 18 + i * 52, bottom: 14, width: 26, height: 18, background: '#F3F1EC', borderRadius: 3}} />
    </React.Fragment>)}
    <div style={{position: 'absolute', left: 24, right: 24, top: 52, bottom: 52, background: bad ? '#3a3a3a' : '#e9e6df', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
    </div>
    <div style={{position: 'absolute', left: 0, right: 0, top: 320, textAlign: 'center', ...sans(34, bad ? RED : INK, 700, 0.02)}}>{label}</div>
    <svg width={380} height={300} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
      {bad
        ? <><path d="M 60 60 L 320 240" pathLength={1} strokeDasharray={`${mark} 2`} stroke={RED} strokeWidth={22} strokeLinecap="round" filter="url(#rough)" />
            <path d="M 320 60 L 60 240" pathLength={1} strokeDasharray={`${Math.max(0, mark * 2 - 1)} 2`} stroke={RED} strokeWidth={22} strokeLinecap="round" filter="url(#rough)" /></>
        : <path d="M 110 160 L 170 220 L 290 80" pathLength={1} strokeDasharray={`${mark} 2`} stroke={RED} strokeWidth={22} fill="none" strokeLinecap="round" strokeLinejoin="round" filter="url(#rough)" />}
    </svg>
  </div>
);
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <Kicker text="Սցենարի դաս · 01" />
      <Scatter text="Ինչո՞ւ" x={86} y={320} size={210} d={2} seed="q" w={700} />
      <Scribble cx={330} cy={445} rx={290} ry={120} p={pr(f, 22, 46)} />
      <FilmCard x={90} y={760} p={pr(f, 40, 58)} label="մինչև վերջ" mark={pr(f, 70, 86)} />
      <FilmCard x={600} y={820} p={pr(f, 52, 70)} label="5-րդ րոպե" bad mark={pr(f, 92, 112)} />
    </AbsoluteFill>
  );
};

// ---------- S2 title ----------
const Title: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <Kicker text="Սցենարի դաս · 01" />
      <Rise d={4} x={90} y={330}><span style={serif(110, INK, 400)}>Ի՞նչ է</span></Rise>
      <Scatter text="դրամատուրգիան" x={80} y={460} size={104} d={10} color={RED} seed="t" w={700} />
      <Stroke d="M 90 640 C 350 610, 700 660, 990 620" p={pr(f, 34, 52)} color={INK} w={22} brush />
      <RedBlock x={90} y={780} w={360} h={170} p={pr(f, 104, 116, io)} />
      <Rise d={108} x={120} y={808}><span style={{...serif(96, '#fff', 500), fontFamily: 'DejaVu Serif'}}>δρᾶμα</span></Rise>
      <Arrow x1={480} y1={865} x2={600} y2={865} p={pr(f, 118, 132)} bend={0} />
      <Rise d={126} x={630} y={820}><span style={serif(76, INK, 600)}>գործողու-</span><br /><span style={serif(76, INK, 600)}>թյուն</span></Rise>
      <Brackets x={90} y={1040} w={900} h={300} p={pr(f, 40, 56)} />
      <Rise d={46} x={130} y={1080} w={820}><span style={{...serif(64, INK, 400), lineHeight: 1.25}}>պատմությունը<br/>կառուցելու <span style={{color: RED, fontStyle: 'italic'}}>արվեստը</span></span></Rise>
    </AbsoluteFill>
  );
};

// ---------- S3 conflict ----------
const Conflict: React.FC = () => {
  const f = useCurrentFrame();
  const hit = 70;
  const sh = f >= hit && f < hit + 14 ? (random(`c${f}`) - 0.5) * 26 * (1 - (f - hit) / 14) : 0;
  const push = pr(f, 30, hit, Easing.in(Easing.cubic));
  return (
    <AbsoluteFill style={{transform: `translate(${sh}px,${sh * 0.5}px)`}}>
      <Paper />
      <Kicker text="Ամեն ինչի սկիզբը" />
      <Scatter text="կոնֆլիկտ" x={86} y={300} size={170} d={2} seed="k" w={700} />
      <Rise d={20} x={90} y={640}><span style={sans(30, GREY)}>ՀԵՐՈՍԸ</span></Rise>
      <div style={{position: 'absolute', left: 90 + push * 110, top: 690, opacity: pr(f, 24, 36)}}>
        <span style={serif(96, INK, 700)}>ուզում է</span>
      </div>
      <Arrow x1={90} y1={860} x2={470 + push * 60} y2={860} p={pr(f, 36, 60)} bend={0} />
      <RedBlock x={640} y={600} w={90} h={420} p={pr(f, 50, 62, io)} />
      <Rise d={58} x={470} y={1050}><span style={serif(84, RED, 700)}>խանգարում է</span></Rise>
      <Rise d={58} x={470} y={1010}><span style={sans(30, GREY)}>ԻՆՉ-ՈՐ ԲԱՆ</span></Rise>
      <AbsoluteFill style={{background: RED, opacity: f >= hit ? 0.5 * (1 - pr(f, hit, hit + 8)) : 0, mixBlendMode: 'multiply'}} />
    </AbsoluteFill>
  );
};

// ---------- S4 the tension curve ----------
const ANCH: [number, number][] = [[110, 1300], [300, 1280], [400, 1170], [470, 1110], [530, 1150], [610, 990], [680, 1030], [790, 720], [880, 1040], [980, 1170]];
const STAGE_ANCHOR = [1, 2, 5, 7, 9];
const STAGES = [
  {n: '01', name: 'Էքսպոզիցիա', desc: 'ով է հերոսը, որտեղ է'},
  {n: '02', name: 'Հանգույց', desc: 'դեպքը, որ ամեն ինչ փոխում է'},
  {n: '03', name: 'Զարգացում', desc: 'խոչընդոտներ, խաղադրույքներ'},
  {n: '04', name: 'Գագաթնակետ', desc: 'ամենաբարձր լարումը'},
  {n: '05', name: 'Հանգուցալուծում', desc: 'հերոսն այլևս նույնը չէ'},
];
const SAMPLES = (() => {
  const pts: [number, number][] = []; const P = ANCH; const idx: number[] = [0];
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
    for (let k = 0; k < 24; k++) {
      const t = k / 24, t2 = t * t, t3 = t2 * t;
      const c = (a: number, b: number, cc: number, d: number) => 0.5 * (2 * b + (-a + cc) * t + (2 * a - 5 * b + 4 * cc - d) * t2 + (-a + 3 * b - 3 * cc + d) * t3);
      pts.push([c(p0[0], p1[0], p2[0], p3[0]), c(p0[1], p1[1], p2[1], p3[1])]);
    }
    idx.push(pts.length);
  }
  pts.push(P[P.length - 1]);
  return {pts, idx};
})();
const Curve: React.FC = () => {
  const f = useCurrentFrame();
  const stage = Math.min(4, Math.floor(f / STAGE));
  const lf = f - stage * STAGE;
  // how far along the curve (in samples) the pen is
  const prevA = stage === 0 ? 0 : SAMPLES.idx[STAGE_ANCHOR[stage - 1]];
  const curA = SAMPLES.idx[STAGE_ANCHOR[stage]];
  const pen = Math.round(interpolate(lf, [0, 36], [prevA, curA], {...clamp, easing: io}));
  const pts = SAMPLES.pts.slice(0, Math.max(2, pen + 1));
  const d = pts.map((p, i) => `${i ? 'L' : 'M'} ${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
  const tip = pts[pts.length - 1];
  const axis = pr(f, 0, 20);
  const st = STAGES[stage];
  const isPeak = stage === 3 && lf >= 36;
  return (
    <AbsoluteFill>
      <Paper />
      <Kicker text="Սյուժեի 5 տարրը" />
      {/* stage title block */}
      <div key={stage} style={{position: 'absolute', left: 90, top: 290}}>
        <div style={{...serif(150, 'transparent', 400), WebkitTextStroke: `2px ${INK}`, opacity: pr(lf, 0, 12), position: 'absolute', right: -880, top: -110}}>{st.n}</div>
      </div>
      <Sequence from={stage * STAGE} durationInFrames={STAGE} layout="none">
        <Scatter text={st.name} x={86} y={330} size={Math.min(130, 860 / ([...st.name].length * 0.7))} d={0} color={stage === 3 ? RED : INK} seed={st.name} w={700} />
        <Rise d={14} x={92} y={500}><span style={{...serif(58, GREY, 400), fontStyle: 'italic'}}>{st.desc}</span></Rise>
      </Sequence>
      {/* axes */}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d="M 90 1340 L 1000 1340" pathLength={1} strokeDasharray={`${axis} 2`} stroke={INK} strokeWidth={3} />
        <path d="M 90 1340 L 90 640" pathLength={1} strokeDasharray={`${axis} 2`} stroke={INK} strokeWidth={3} />
        {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={90} x2={1000} y1={1340 - (i + 1) * 140} y2={1340 - (i + 1) * 140} stroke={INK} strokeOpacity={0.07 * axis} strokeDasharray="6 10" />)}
      </svg>
      <div style={{position: 'absolute', left: 860, top: 1356, ...sans(22, GREY)}}>ԺԱՄԱՆԱԿ</div>
      <div style={{position: 'absolute', left: 62, top: 600, ...sans(22, GREY), transform: 'rotate(-90deg)', transformOrigin: 'left top'}}>ԼԱՐՈՒՄ</div>
      {/* the curve */}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
        <path d={d} fill="none" stroke={RED} strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" filter="url(#rough)" />
        {STAGE_ANCHOR.map((a, i) => {
          if (i > stage || (i === stage && lf < 30)) return null;
          const [x, y] = ANCH[a];
          const p = i === stage ? pr(lf, 30, 42) : 1;
          return <g key={i} opacity={p}>
            <circle cx={x} cy={y} r={14 * p + (i === stage ? 4 : 0)} fill={i === stage ? RED : INK} />
            <text x={x} y={y + (i === 3 ? -40 : 52)} textAnchor="middle" fontFamily="ArmSans" fontWeight={700} fontSize={30} fill={INK}>{STAGES[i].n}</text>
          </g>;
        })}
        <circle cx={tip[0]} cy={tip[1]} r={10} fill={INK} />
      </svg>
      {isPeak && <Scribble cx={790} cy={720} rx={80} ry={60} p={pr(lf, 36, 56)} color={INK} />}
      {isPeak && <AbsoluteFill style={{background: RED, mixBlendMode: 'multiply', opacity: 0.35 * (1 - pr(lf, 36, 46))}} />}
    </AbsoluteFill>
  );
};

// ---------- S5 flat line: no conflict ----------
const Flat: React.FC = () => {
  const f = useCurrentFrame();
  const items = ['արթնացավ', 'գնաց', 'կերավ', 'վերադարձավ'];
  return (
    <AbsoluteFill>
      <Paper />
      <Kicker text="Առանց կոնֆլիկտի" />
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d="M 110 1000 L 980 1000" pathLength={1} strokeDasharray={`${pr(f, 4, 30, io)} 2`} stroke={GREY} strokeWidth={8} strokeLinecap="round" />
        {items.map((_, i) => <circle key={i} cx={180 + i * 240} cy={1000} r={14} fill={GREY} opacity={pr(f, 14 + i * 6, 22 + i * 6)} />)}
      </svg>
      {items.map((t, i) => <Rise key={i} d={16 + i * 6} x={120 + i * 240} y={i % 2 ? 1050 : 890}><span style={{...sans(34, GREY, 500, 0)}}>{t}</span></Rise>)}
      <Rise d={10} x={90} y={330}><span style={serif(120, GREY, 400)}>դեպքերի</span></Rise>
      <Rise d={18} x={90} y={470}><span style={serif(120, GREY, 400)}>թվարկում</span></Rise>
      <Stroke d="M 80 420 C 300 400, 520 430, 700 405" p={pr(f, 50, 62)} color={RED} w={20} brush />
      <Stroke d="M 80 560 C 300 540, 560 580, 760 545" p={pr(f, 58, 70)} color={RED} w={20} brush />
      <Rise d={72} x={90} y={660}><span style={serif(96, RED, 700)}>դրամա չկա։</span></Rise>
    </AbsoluteFill>
  );
};

// ---------- S6 end ----------
const End: React.FC = () => {
  const f = useCurrentFrame();
  const reveal = pr(f, 50, 82, io);
  return (
    <AbsoluteFill>
      <Paper />
      <Kicker text="Սցենարի դաս · 01" />
      <Rise d={4} x={90} y={300}><span style={serif(64, GREY, 400)}>Հաջորդ դասը՝</span></Rise>
      <Scatter text="կոնֆլիկտի" x={86} y={390} size={130} d={10} color={INK} seed="e1" w={700} />
      <Scatter text="տեսակները" x={86} y={530} size={130} d={18} color={RED} seed="e2" w={700} />
      <div style={{position: 'absolute', left: 140, top: 640, width: 800, height: 800, clipPath: `inset(0 ${(1 - reveal) * 100}% 0 0)`}}>
        <Img src={staticFile('dr/logo.svg')} style={{width: 800, height: 800}} />
      </div>
      <Rise d={86} x={0} y={1300} w={1080}><div style={{textAlign: 'center', ...sans(26)}}>MAGHAKIANSCRIPTS.COM</div></Rise>
    </AbsoluteFill>
  );
};

export const Lesson: React.FC = () => {
  useFonts();
  const S = (a: number, b: number, el: React.ReactNode) => <Sequence from={a} durationInFrames={b - a}>{el}</Sequence>;
  return (
    <AbsoluteFill style={{background: '#F3F1EC'}}>
      <Defs />
      <Audio src={staticFile('dr/lesson_mix.wav')} />
      {S(T.hook, T.title, <Hook />)}
      {S(T.title, T.conflict, <Title />)}
      {S(T.conflict, T.curve, <Conflict />)}
      {S(T.curve, T.flat, <Curve />)}
      {S(T.flat, T.end, <Flat />)}
      {S(T.end, L_TOTAL, <End />)}
      <Subs />
      {[T.title, T.conflict, T.curve, T.flat, T.end].map((t, i) => <Sequence key={t} from={t - 9} durationInFrames={18}><Wipe color={i % 2 ? RED : INK} /></Sequence>)}
    </AbsoluteFill>
  );
};
