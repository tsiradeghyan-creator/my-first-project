import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, random, staticFile, useCurrentFrame, Easing} from 'remotion';

const PAPER = '#F3F1EC';
const INK = '#111111';
const RED = '#D90429';
const SRC = staticFile('in.mp4');
const SERIF = 'DBodoni', SERIF_IT = 'DBodoniIt', MONT = 'Mont';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const outx = Easing.bezier(0.16, 1, 0.3, 1);
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = outx) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});

// ---------- timeline ----------
const T = {hook: 0, b1: 150, b2: 258, b3: 372, b4: 495, b5: 627, plain: 780, story: 882, creds: 942, logo: 1134};
export const D_TOTAL = 1260;
const HIT = 606;

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const fs = [
      new FontFace(SERIF, `url(${staticFile('Bodoni.ttf')})`, {weight: '400 900'}),
      new FontFace(SERIF_IT, `url(${staticFile('BodoniIt.ttf')})`, {weight: '400 900'}),
      new FontFace(MONT, `url(${staticFile('dr/Montserrat.ttf')})`, {weight: '100 900'}),
    ];
    Promise.all(fs.map((f) => f.load())).then((l) => { l.forEach((x) => (document as any).fonts.add(x)); continueRender(h); });
  }, [h]);
};

// ---------- global brush filters ----------
const Defs: React.FC = () => (
  <svg width="0" height="0" style={{position: 'absolute'}}>
    <defs>
      <filter id="rough" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" result="t" />
        <feDisplacementMap in="SourceGraphic" in2="t" scale="22" />
      </filter>
      <filter id="brush" x="-10%" y="-20%" width="120%" height="140%">
        <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="9" result="t" />
        <feDisplacementMap in="SourceGraphic" in2="t" scale="26" result="d" />
        <feTurbulence type="fractalNoise" baseFrequency="0.012 0.35" numOctaves="2" seed="2" result="b" />
        <feColorMatrix in="b" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.55" result="m" />
        <feComposite in="d" in2="m" operator="in" />
      </filter>
    </defs>
  </svg>
);

// ---------- paper ----------
const Paper: React.FC = () => {
  const f = useCurrentFrame();
  const blots = Array.from({length: 9}).map((_, i) => ({x: random(`bx${i}`) * 1080, y: random(`by${i}`) * 1920, r: 60 + random(`br${i}`) * 140}));
  return (
    <AbsoluteFill style={{background: PAPER}}>
      {blots.map((b, i) => <div key={i} style={{position: 'absolute', left: b.x - b.r, top: b.y - b.r, width: b.r * 2, height: b.r * 2, borderRadius: '50%', background: 'radial-gradient(circle, rgba(60,55,50,0.045), rgba(60,55,50,0) 70%)', filter: 'url(#rough)'}} />)}
      <AbsoluteFill style={{opacity: 0.22, mixBlendMode: 'multiply', backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.75' seed='${f % 6}'/><feColorMatrix values='0 0 0 0 0.5  0 0 0 0 0.48  0 0 0 0 0.45  0 0 0 1.4 -0.35'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`}} />
    </AbsoluteFill>
  );
};

// ---------- graphic primitives ----------
const Stroke: React.FC<{d: string; p: number; color?: string; w?: number; brush?: boolean; tail?: number}> = ({d, p, color = INK, w = 8, brush = false, tail = 0}) => (
  <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
    <path d={d} pathLength={1} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round"
      strokeDasharray={`${Math.max(0.0001, p - tail)} 2`} strokeDashoffset={-tail} filter={brush ? 'url(#brush)' : 'url(#rough)'} />
  </svg>
);
const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; p: number; color?: string; bend?: number}> = ({x1, y1, x2, y2, p, color = INK, bend = 60}) => {
  const mx = (x1 + x2) / 2 - (y2 - y1) * bend / 300, my = (y1 + y2) / 2 + (x2 - x1) * bend / 300;
  const ang = Math.atan2(y2 - my, x2 - mx);
  const h = 34, a1 = ang + 2.6, a2 = ang - 2.6;
  const head = `M ${x2 + h * Math.cos(a1)} ${y2 + h * Math.sin(a1)} L ${x2} ${y2} L ${x2 + h * Math.cos(a2)} ${y2 + h * Math.sin(a2)}`;
  return <>
    <Stroke d={`M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`} p={Math.min(1, p * 1.3)} color={color} w={7} />
    <Stroke d={head} p={interpolate(p, [0.7, 1], [0, 1], clamp)} color={color} w={7} />
  </>;
};
const Scribble: React.FC<{cx: number; cy: number; rx: number; ry: number; p: number; color?: string}> = ({cx, cy, rx, ry, p, color = RED}) => {
  let d = '';
  for (let i = 0; i <= 80; i++) {
    const t = (i / 80) * Math.PI * 2 * 1.35 - 0.6;
    const r = 1 + 0.08 * Math.sin(i * 0.7);
    d += `${i ? 'L' : 'M'} ${cx + Math.cos(t) * rx * r} ${cy + Math.sin(t) * ry * r * (1 + i / 400)} `;
  }
  return <Stroke d={d} p={p} color={color} w={9} />;
};
const RedBlock: React.FC<{x: number; y: number; w: number; h: number; p: number; color?: string; fromRight?: boolean}> = ({x, y, w, h, p, color = RED, fromRight}) => (
  <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
    <rect x={fromRight ? x + w * (1 - p) : x} y={y} width={w * p} height={h} fill={color} filter="url(#rough)" />
  </svg>
);
const Brackets: React.FC<{x: number; y: number; w: number; h: number; p: number; color?: string}> = ({x, y, w, h, p, color = INK}) => {
  const o = (1 - p) * 60, L = 70;
  const c = [[x - 24 - o, y - 24 - o, 1, 1], [x + w + 24 + o, y - 24 - o, -1, 1], [x - 24 - o, y + h + 24 + o, 1, -1], [x + w + 24 + o, y + h + 24 + o, -1, -1]];
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, opacity: p}}>
      {c.map(([cx, cy, sx, sy], i) => <path key={i} d={`M ${cx} ${cy + sy * L} L ${cx} ${cy} L ${cx + sx * L} ${cy}`} stroke={color} strokeWidth={4} fill="none" />)}
    </svg>
  );
};
// B&W photo box with video
const Photo: React.FC<{x: number; y: number; w: number; h: number; start: number; rate?: number; p?: number; pos?: string; color?: boolean; tilt?: number}> = ({x, y, w, h, start, rate = 1, p = 1, pos = '50% 50%', color = false, tilt = 0}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, overflow: 'hidden', clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`, transform: `rotate(${tilt}deg)`, boxShadow: '0 18px 40px rgba(0,0,0,0.18)'}}>
    <OffthreadVideo src={SRC} muted startFrom={Math.round(start * 30)} playbackRate={rate}
      style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, filter: color ? 'contrast(1.08) saturate(1.05)' : 'grayscale(1) contrast(1.35) brightness(1.06)'}} />
  </div>
);

// ---------- type ----------
const serif = (s: number, c = INK, it = false): React.CSSProperties => ({fontFamily: it ? SERIF_IT : SERIF, fontWeight: it ? 500 : 500, fontSize: s, color: c, lineHeight: 0.92, letterSpacing: -s * 0.02});
const mont = (s: number, c = INK, w = 600): React.CSSProperties => ({fontFamily: MONT, fontWeight: w, fontSize: s, color: c, letterSpacing: s * 0.28, textTransform: 'uppercase'});
// letters fly in from scattered positions (reference intro)
const Scatter: React.FC<{text: string; x: number; y: number; size: number; d?: number; color?: string; it?: boolean; seed?: string}> = ({text, x, y, size, d = 0, color = INK, it, seed = 's'}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: x, top: y, display: 'flex', whiteSpace: 'pre'}}>
      {text.split('').map((ch, i) => {
        const p = pr(f, d + i * 1.6, d + i * 1.6 + 20);
        const dx = (random(`${seed}x${i}`) - 0.5) * 700 * (1 - p), dy = (random(`${seed}y${i}`) - 0.5) * 500 * (1 - p);
        const r = (random(`${seed}r${i}`) - 0.5) * 90 * (1 - p);
        const sc = 1 + (random(`${seed}s${i}`) - 0.3) * 1.2 * (1 - p);
        return <span key={i} style={{...serif(size, color, it), display: 'inline-block', opacity: Math.min(1, p * 2.5), transform: `translate(${dx}px,${dy}px) rotate(${r}deg) scale(${sc})`}}>{ch}</span>;
      })}
    </div>
  );
};
// letters cycle through random glyphs, then settle
const Decode: React.FC<{text: string; x: number; y: number; size: number; d?: number; color?: string}> = ({text, x, y, size, d = 0, color = INK}) => {
  const f = useCurrentFrame();
  const A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  return (
    <div style={{position: 'absolute', left: x, top: y, ...serif(size, color), whiteSpace: 'pre'}}>
      {text.split('').map((ch, i) => {
        const settle = d + 6 + i * 3;
        if (f < d + i) return <span key={i} style={{opacity: 0}}>{ch}</span>;
        const c = f >= settle || ch === ' ' || ch === '.' ? ch : A[Math.floor(random(`${i}-${Math.floor(f / 2)}`) * 26)];
        return <span key={i} style={{color: f >= settle ? color : RED}}>{c}</span>;
      })}
    </div>
  );
};
const Rise: React.FC<{d?: number; x: number; y: number; children: React.ReactNode; out?: number}> = ({d = 0, x, y, children, out}) => {
  const f = useCurrentFrame();
  const p = pr(f, d, d + 16);
  const o = out ? 1 - pr(f, out - 8, out, io) : 1;
  return <div style={{position: 'absolute', left: x, top: y, opacity: p * o, transform: `translateY(${(1 - p) * 30}px)`, clipPath: `inset(0 0 ${(1 - p) * 100}% 0)`}}>{children}</div>;
};

// beat header: "BEAT 01" + outline number + title word
const Header: React.FC<{n: number; word: string; red?: boolean}> = ({n, word, red}) => {
  const f = useCurrentFrame();
  const line = pr(f, 0, 14);
  return (
    <>
      <div style={{position: 'absolute', left: 90, top: 250, display: 'flex', alignItems: 'center', gap: 20, opacity: line}}>
        <div style={{width: 70 * line, height: 4, background: RED}} />
        <span style={mont(24)}>Beat 0{n} / 05</span>
      </div>
      <div style={{position: 'absolute', right: 150, top: 110, ...serif(220, 'transparent'), WebkitTextStroke: `2px ${INK}`, opacity: pr(f, 4, 20), transform: `translateY(${(1 - pr(f, 4, 24)) * -60}px)`}}>0{n}</div>
      <Scatter text={word} x={86} y={380} size={160} d={4} color={red ? RED : INK} seed={word} />
    </>
  );
};

// full-screen brush wipe between scenes
const Wipe: React.FC<{color?: string}> = ({color = INK}) => {
  const f = useCurrentFrame();
  const p = pr(f, 0, 9, io), q = pr(f, 9, 18, io);
  return <Stroke d="M -200 300 C 300 200, 700 500, 1300 380 M 1300 380 C 700 900, 300 800, -200 1100 M -200 1100 C 300 1300, 800 1400, 1300 1700" p={p} tail={q} color={color} w={760} brush />;
};

// ---------- scenes ----------
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <Scatter text="Dramaturgy" x={86} y={430} size={168} d={2} seed="h" />
      <Stroke d="M 100 640 C 300 610, 600 660, 980 615" p={pr(f, 28, 46)} color={RED} w={26} brush />
      <Rise d={34} x={92} y={680}><span style={mont(30)}>in 40 seconds</span></Rise>
      <RedBlock x={300} y={900} w={600} h={560} p={pr(f, 54, 70, io)} />
      <Photo x={200} y={840} w={620} h={560} start={0.3} p={pr(f, 62, 80, io)} pos="50% 45%" />
      <Brackets x={200} y={840} w={620} h={560} p={pr(f, 72, 90)} />
      <Rise d={88} x={150} y={1470}><span style={serif(92, INK, true)}>One car. <span style={{color: RED}}>Five beats.</span></span></Rise>
      <Arrow x1={130} y1={1460} x2={230} y2={1330} p={pr(f, 100, 118)} bend={-80} />
    </AbsoluteFill>
  );
};
const Want: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <Header n={1} word="Want." />
      <Photo x={140} y={720} w={800} h={720} start={0.6} p={pr(f, 6, 24, io)} pos="50% 50%" />
      <Brackets x={140} y={720} w={800} h={720} p={pr(f, 18, 34)} />
      <Scribble cx={500} cy={1085} rx={120} ry={80} p={pr(f, 30, 52)} />
      <Rise d={40} x={600} y={1480}><span style={serif(74, RED, true)}>the goal</span></Rise>
      <Arrow x1={640} y1={1490} x2={590} y2={1150} p={pr(f, 50, 66)} color={RED} bend={50} />
    </AbsoluteFill>
  );
};
const Obstacle: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <Header n={2} word="Obstacle." />
      <RedBlock x={60} y={700} w={720} h={660} p={pr(f, 4, 18, io)} />
      <Photo x={290} y={800} w={700} h={640} start={9.2} rate={1.2} p={pr(f, 12, 28, io)} pos="50% 62%" tilt={-1.5} />
      <Stroke d="M 120 1500 C 400 1420, 700 1460, 1000 1380" p={pr(f, 34, 50)} color={INK} w={40} brush />
      <Rise d={46} x={90} y={1530}><span style={serif(78, INK, true)}>Snow, up to the bumper.</span></Rise>
    </AbsoluteFill>
  );
};
const Stakes: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <Header n={3} word="Stakes." red />
      {Array.from({length: 6}).map((_, i) => {
        const p = pr(f, 8 + i * 7, 26 + i * 7);
        const dir = i % 2 ? 1 : -1;
        return <div key={i} style={{position: 'absolute', left: 80 + dir * (1 - p) * 500, top: 690 + i * 148, opacity: p, ...serif(170, i === 3 ? RED : INK, i === 3)}}>more{i === 5 ? '.' : ''}</div>;
      })}
      <Photo x={560} y={820} w={420} h={560} start={27} rate={1.6} p={pr(f, 40, 56, io)} pos="50% 60%" tilt={3} />
      <Brackets x={560} y={820} w={420} h={560} p={pr(f, 50, 66)} color={RED} />
      <Rise d={70} x={560} y={1440}><span style={mont(22)}>every metre costs more</span></Rise>
    </AbsoluteFill>
  );
};
const Turn: React.FC = () => {
  const f = useCurrentFrame();
  const h = HIT - T.b4;
  const shake = f >= h && f < h + 20 ? (random(`t${f}`) - 0.5) * 30 * (1 - (f - h) / 20) : 0;
  const strips = 7;
  return (
    <AbsoluteFill style={{background: INK}}>
      <AbsoluteFill style={{transform: `translate(${shake}px, ${shake * 0.4}px) scale(${interpolate(f, [0, 132], [1.05, 1.18])})`}}>
        <Photo x={0} y={0} w={1080} h={1920} start={40.85} rate={0.5} />
      </AbsoluteFill>
      {f >= h && f < h + 14 && Array.from({length: strips}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: (random(`sx${i}${Math.floor(f / 2)}`) - 0.5) * 160, top: (1920 / strips) * i, width: 1080, height: 1920 / strips, overflow: 'hidden'}}>
          <div style={{position: 'absolute', top: -(1920 / strips) * i, width: 1080, height: 1920, background: i % 3 === 0 ? RED : 'transparent', mixBlendMode: 'multiply', opacity: 0.85}} />
        </div>
      ))}
      <AbsoluteFill style={{background: PAPER, opacity: f >= h ? 1 - pr(f, h, h + 8) : 0}} />
      <div style={{position: 'absolute', left: 90, top: 250, ...mont(24, '#fff')}}>Beat 04 / 05</div>
      <Rise d={6} x={86} y={340} out={h}><span style={{...serif(150, '#fff', true), textShadow: '0 4px 30px rgba(0,0,0,0.5)'}}>The turn.</span></Rise>
      <Stroke d="M -60 1250 C 300 1050, 700 1000, 1160 760" p={pr(f, h, h + 8)} color={RED} w={150} brush />
      <Scatter text="TURN" x={110} y={1290} size={300} d={h + 2} color={INK} seed="turn" />
    </AbsoluteFill>
  );
};
const Change: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Paper />
      <div style={{position: 'absolute', left: 90, top: 250, display: 'flex', alignItems: 'center', gap: 20}}>
        <div style={{width: 70 * pr(f, 0, 14), height: 4, background: RED}} />
        <span style={mont(24)}>Beat 05 / 05</span>
      </div>
      <div style={{position: 'absolute', right: 150, top: 110, ...serif(220, 'transparent'), WebkitTextStroke: `2px ${INK}`, opacity: pr(f, 4, 20)}}>05</div>
      <Decode text="Change." x={86} y={380} size={160} d={2} />
      <Stroke d="M 90 560 C 300 590, 520 540, 700 575" p={pr(f, 30, 44)} color={RED} w={20} brush />
      <Photo x={140} y={700} w={800} h={720} start={46} p={pr(f, 8, 26, io)} pos="50% 55%" />
      <Brackets x={140} y={700} w={800} h={720} p={pr(f, 20, 36)} />
      <Rise d={70} x={140} y={1480}><span style={serif(80, INK, true)}>not the same <span style={{color: RED}}>driver.</span></span></Rise>
      <Arrow x1={860} y1={1500} x2={560} y2={1150} p={pr(f, 84, 100)} color={RED} bend={-60} />
    </AbsoluteFill>
  );
};
const Plain: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <Photo x={0} y={0} w={1080} h={1920} start={30} color />
    <div style={{position: 'absolute', bottom: 470, left: 0, right: 0, textAlign: 'center', fontFamily: MONT, fontWeight: 500, fontSize: 34, color: 'rgba(255,255,255,0.9)', letterSpacing: 1}}>just a car in the snow.</div>
  </AbsoluteFill>
);
const Story: React.FC = () => {
  const f = useCurrentFrame();
  const p = pr(f, 0, 10);
  return (
    <AbsoluteFill>
      <Paper />
      <RedBlock x={0} y={480} w={1080} h={760} p={pr(f, 0, 6, io)} />
      <Photo x={170} y={400} w={740} h={900} start={33.4} p={pr(f, 2, 10, io)} tilt={-2} />
      <Brackets x={170} y={400} w={740} h={900} p={pr(f, 6, 16)} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 1330, textAlign: 'center', transform: `scale(${interpolate(p, [0, 1], [2.2, 1])})`, opacity: p}}>
        <span style={serif(250, INK, true)}>a story.</span>
      </div>
      <Arrow x1={100} y1={300} x2={230} y2={470} p={pr(f, 8, 20)} />
      <Arrow x1={990} y1={1640} x2={900} y2={1360} p={pr(f, 10, 22)} color={RED} />
      <Stroke d="M 60 330 C 300 250, 700 380, 1020 260" p={pr(f, 12, 24)} color={INK} w={36} brush />
    </AbsoluteFill>
  );
};
const Creds: React.FC = () => {
  const f = useCurrentFrame();
  const rows = [
    {big: '48', it: 'projects', d: 60},
    {big: '2,300+', it: 'episodes', d: 108},
    {big: 'since', it: '2016', d: 150},
  ];
  return (
    <AbsoluteFill>
      <Paper />
      <Rise d={6} x={90} y={330}><span style={serif(84, INK, true)}>We build them</span></Rise>
      <Rise d={14} x={90} y={420}><span style={serif(84, INK, true)}>for a living.</span></Rise>
      <Stroke d="M 90 540 C 300 520, 500 560, 640 530" p={pr(f, 22, 36)} color={RED} w={18} brush />
      {rows.map((r, i) => {
        const p = pr(f, r.d, r.d + 18);
        return (
          <div key={i} style={{position: 'absolute', left: 90, top: 630 + i * 300, display: 'flex', flexDirection: 'column', opacity: p, transform: `translateX(${(1 - p) * (i % 2 ? 300 : -300)}px)`}}>
            <span style={serif(190, INK)}>{r.big}</span>
            <span style={{...serif(92, RED, true), marginTop: -6, marginLeft: 8}}>{r.it}</span>
          </div>
        );
      })}
      <Rise d={160} x={640} y={700}><span style={{...mont(20), lineHeight: 2}}>Series<br/>Film<br/>Stage<br/>Children's</span></Rise>
      <Brackets x={70} y={620} w={880} h={920} p={pr(f, 170, 186)} />
    </AbsoluteFill>
  );
};
const Logo: React.FC = () => {
  const f = useCurrentFrame();
  const reveal = pr(f, 4, 36, io);
  return (
    <AbsoluteFill>
      <Paper />
      <div style={{position: 'absolute', left: 90, top: 380, width: 900, height: 900, clipPath: `inset(0 ${(1 - reveal) * 100}% 0 0)`}}>
        <Img src={staticFile('dr/logo.svg')} style={{width: 900, height: 900}} />
      </div>
      <Stroke d="M 200 1180 C 420 1150, 700 1200, 900 1160" p={pr(f, 30, 48)} color={RED} w={14} brush />
      <Rise d={44} x={0} y={1270}><div style={{width: 1080, textAlign: 'center', ...serif(84, INK, true)}}>Send us your idea.</div></Rise>
      <Rise d={56} x={0} y={1400}><div style={{width: 1080, textAlign: 'center', ...mont(26)}}>maghakianscripts.com</div></Rise>
    </AbsoluteFill>
  );
};

export const Drama: React.FC = () => {
  useFonts();
  const S = (from: number, to: number, el: React.ReactNode) => <Sequence from={from} durationInFrames={to - from}>{el}</Sequence>;
  return (
    <AbsoluteFill style={{background: PAPER}}>
      <Defs />
      <Audio src={staticFile('dr/mix.wav')} />
      {S(T.hook, T.b1, <Hook />)}
      {S(T.b1, T.b2, <Want />)}
      {S(T.b2, T.b3, <Obstacle />)}
      {S(T.b3, T.b4, <Stakes />)}
      {S(T.b4, T.b5, <Turn />)}
      {S(T.b5, T.plain, <Change />)}
      {S(T.plain, T.story, <Plain />)}
      {S(T.story, T.creds, <Story />)}
      {S(T.creds, T.logo, <Creds />)}
      {S(T.logo, D_TOTAL, <Logo />)}
      {[T.b1, T.b2, T.b3, T.b5, T.creds, T.logo].map((t, i) => <Sequence key={t} from={t - 9} durationInFrames={18}><Wipe color={i % 2 ? RED : INK} /></Sequence>)}
    </AbsoluteFill>
  );
};
