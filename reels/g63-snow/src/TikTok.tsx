import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill, Audio, OffthreadVideo, Sequence, continueRender, delayRender,
  interpolate, staticFile, useCurrentFrame, Easing, random,
} from 'remotion';

// ---------- design tokens: maison x keynote ----------
const CREAM = '#F2EDE4';
const INK = '#141210';
const GREY = '#8A847C';
const ACCENT = '#D4602A'; // burnt orange, one accent only
const SRC = staticFile('in.mp4');
const SANS = 'InterV';
const SERIF = 'BodoniIt';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = Easing.bezier(0.65, 0, 0.35, 1);
const outx = Easing.bezier(0.16, 1, 0.3, 1);
const ease = (f: number, a: number, b: number, from: number, to: number, e = io) => interpolate(f, [a, b], [from, to], {...clamp, easing: e});

// ---------- timeline (cuts on the 100 bpm grid: 1.8s + n*0.6s) ----------
const S1 = {from: 0, dur: 108};    // HOOK: climax teaser, burst at 0.8s
const S2 = {from: 108, dur: 72};   // knockout G 63
const S3 = {from: 180, dur: 162};  // drive
const S4 = {from: 342, dur: 180};  // specs
const S5 = {from: 522, dur: 90};   // triptych
const S6 = {from: 612, dur: 144};  // burst (drop at 23.4s)
const S7 = {from: 756, dur: 210};  // release + end titles
export const T_TOTAL = S7.from + S7.dur; // 966 = 32.2s
const BURST = S6.from + 90;

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const fonts = [
      new FontFace(SANS, `url(${staticFile('Inter.ttf')})`, {weight: '100 900'}),
      new FontFace(SERIF, `url(${staticFile('BodoniIt.ttf')})`, {weight: '400 900'}),
    ];
    Promise.all(fonts.map((f) => f.load())).then((ls) => { ls.forEach((f) => (document as any).fonts.add(f)); continueRender(h); });
  }, [h]);
};

// ---------- film grade: warm, soft, editorial ----------
const Footage: React.FC<{start: number; rate?: number; pos?: string; scale?: number}> = ({start, rate = 1, pos = '50% 55%', scale = 1}) => (
  <AbsoluteFill style={{overflow: 'hidden', background: '#1a1714'}}>
    <AbsoluteFill style={{transform: `scale(${scale})`}}>
      <OffthreadVideo src={SRC} muted startFrom={Math.round(start * 30)} playbackRate={rate}
        style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos,
          filter: 'contrast(1.12) saturate(1.05) brightness(1.05)'}} />
    </AbsoluteFill>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #1f5f99 0%, #ffd29a 40%, #ffc79a 60%, #173a66 100%)', mixBlendMode: 'soft-light', opacity: 0.85}} />
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(14,32,60,0.55) 0%, rgba(14,32,60,0) 26%, rgba(0,0,0,0) 55%, rgba(10,18,34,0.75) 100%)'}} />
    <Grain />
  </AbsoluteFill>
);
const Grain: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{opacity: 0.08, mixBlendMode: 'overlay', backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.8' seed='${f % 8}'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`}} />;
};

const Canvas: React.FC<{children?: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const a = Math.sin(f / 40) * 80, b = Math.cos(f / 50) * 90;
  return (
    <AbsoluteFill style={{background: CREAM}}>
      <div style={{position: 'absolute', width: 1100, height: 1100, left: -380 + a, top: -260 + b, borderRadius: '50%', background: 'radial-gradient(circle, rgba(232,120,60,0.55), rgba(232,120,60,0) 65%)'}} />
      <div style={{position: 'absolute', width: 1300, height: 1300, right: -520 - a, bottom: -300 + b, borderRadius: '50%', background: 'radial-gradient(circle, rgba(70,140,215,0.5), rgba(70,140,215,0) 65%)'}} />
      <div style={{position: 'absolute', width: 800, height: 800, left: 500 + b, top: 700 - a, borderRadius: '50%', background: 'radial-gradient(circle, rgba(245,190,90,0.35), rgba(245,190,90,0) 65%)'}} />
      <Grain />
      {children}
    </AbsoluteFill>
  );
};

// ---------- type ----------
const sans = (size: number, weight = 600, color = INK): React.CSSProperties => ({fontFamily: SANS, fontWeight: weight, fontSize: size, color, letterSpacing: -size * 0.035, lineHeight: 1.04});
const serif = (size: number, color = INK): React.CSSProperties => ({fontFamily: SERIF, fontWeight: 500, fontSize: size, color, letterSpacing: -size * 0.02, lineHeight: 1});
const caps = (size: number, color = GREY): React.CSSProperties => ({fontFamily: SANS, fontWeight: 600, fontSize: size, color, letterSpacing: size * 0.32, textTransform: 'uppercase'});

// keynote-style line: fade + rise + unblur
const Line: React.FC<{d?: number; out?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({d = 0, out, children, style}) => {
  const f = useCurrentFrame();
  const p = ease(f, d, d + 22, 0, 1, outx);
  const o = out ? ease(f, out - 10, out, 1, 0) : 1;
  return <div style={{opacity: p * o, transform: `translateY(${(1 - p) * 40 - (1 - o) * 20}px)`, filter: `blur(${(1 - p) * 10 + (1 - o) * 8}px)`, ...style}}>{children}</div>;
};

// ---------- instruments (minimal, watch-dial style) ----------
const polar = (cx: number, cy: number, r: number, deg: number) => [cx + r * Math.cos((deg * Math.PI) / 180), cy + r * Math.sin((deg * Math.PI) / 180)];
const arcPath = (cx: number, cy: number, r: number, a0: number, a1: number) => {
  const [x0, y0] = polar(cx, cy, r, a0); const [x1, y1] = polar(cx, cy, r, a1);
  return `M ${x0} ${y0} A ${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1}`;
};
const Dial: React.FC<{v: number; max: number; size: number; draw?: number; color?: string; red?: number; labels?: number[]; unit: string; readout: string; sweep?: number}> = ({v, max, size, draw = 1, color = INK, red, labels = [], unit, readout, sweep = 270}) => {
  const c = size / 2, r = size / 2 - 30;
  const A0 = 90 + (360 - sweep) / 2;
  const ang = (x: number) => A0 + (x / max) * sweep;
  const [nx, ny] = polar(c, c, r - 18, ang(v));
  const [bx, by] = polar(c, c, -30, ang(v));
  const ticks = 60;
  return (
    <svg width={size} height={size}>
      <path d={arcPath(c, c, r, A0, A0 + sweep * Math.max(0.001, draw))} stroke={color} strokeWidth={1.6} fill="none" />
      {red !== undefined && draw > 0.95 && <path d={arcPath(c, c, r - 6, ang(red), ang(max))} stroke={ACCENT} strokeWidth={5} fill="none" />}
      {Array.from({length: ticks + 1}).map((_, i) => {
        if (i / ticks > draw) return null;
        const a = A0 + (i / ticks) * sweep; const major = i % (ticks / Math.max(1, labels.length - 1 || 1)) === 0;
        const [x0, y0] = polar(c, c, r - (major ? 22 : 10), a); const [x1, y1] = polar(c, c, r, a);
        return <line key={i} x1={x0} y1={y0} x2={x1} y2={y1} stroke={color} strokeWidth={major ? 2 : 1} opacity={major ? 1 : 0.55} />;
      })}
      {labels.map((l, i) => {
        const a = A0 + (i / (labels.length - 1)) * sweep; const [x, y] = polar(c, c, r - 52, a);
        return <text key={i} x={x} y={y + 9} textAnchor="middle" fontFamily={SANS} fontWeight={500} fontSize={size * 0.055} fill={color} opacity={draw > i / (labels.length - 1) ? 1 : 0}>{l}</text>;
      })}
      <line x1={bx} y1={by} x2={nx} y2={ny} stroke={ACCENT} strokeWidth={3} strokeLinecap="round" opacity={draw} />
      <circle cx={c} cy={c} r={9} fill={color} opacity={draw} />
      <text x={c} y={c + size * 0.31} textAnchor="middle" fontFamily={SANS} fontWeight={300} fontSize={size * 0.13} fill={color} letterSpacing={-2}>{readout}</text>
      <text x={c} y={c + size * 0.38} textAnchor="middle" fontFamily={SANS} fontWeight={600} fontSize={size * 0.03} letterSpacing={6} fill={GREY}>{unit}</text>
    </svg>
  );
};

// ---------- S1: HOOK — climax teaser ----------
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const b = 24;
  const shake = f > b && f < b + 20 ? (random(`h${f}`) - 0.5) * 22 * (1 - (f - b) / 20) : 0;
  const flash = f >= b ? ease(f, b, b + 12, 1, 0) : 0;
  const rpm = (f < b ? 5200 : interpolate(f, [b, b + 14, 108], [7900, 7300, 6200], clamp)) + jitter(f, 200);
  const zoom = interpolate(f, [0, b, 108], [1.0, 1.18, 1.3], clamp);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{transform: `translateX(${shake}px)`}}><Footage start={42.3} rate={0.5} scale={zoom} /></AbsoluteFill>
      <MiniTacho rpm={rpm} o={ease(f, 2, 12, 0, 1)} />
      <AbsoluteFill style={{background: '#fff', opacity: flash * 0.85}} />
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 1040}}>
        <Line d={b + 2}><span style={{...sans(250, 900, '#fff'), textShadow: '0 10px 60px rgba(0,0,0,0.5)'}}>585 HP</span></Line>
        <Line d={70}><span style={{...serif(140, ACCENT), textShadow: '0 6px 40px rgba(0,0,0,0.5)'}}>vs. zero road.</span></Line>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- S2: knockout type, zoom-through ----------
const Knockout: React.FC = () => {
  const f = useCurrentFrame();
  const appear = ease(f, 0, 18, 0, 1, outx);
  const z = interpolate(f, [20, 70], [1, 26], {...clamp, easing: Easing.in(Easing.exp)});
  const fade = ease(f, 58, 72, 1, 0);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{filter: `brightness(${interpolate(f, [0, 50, 72], [0.55, 0.6, 1], clamp)}) contrast(1.2)`}}><Footage start={4} scale={interpolate(f, [0, 100], [1.25, 1.08])} /></AbsoluteFill>
      <AbsoluteFill style={{background: 'linear-gradient(160deg, #FBE3CF, #F2EDE4 50%, #DCE8F6)', mixBlendMode: 'screen', opacity: fade, alignItems: 'center', justifyContent: 'center'}}>
        <div style={{...sans(400, 900, '#000'), letterSpacing: -26, transform: `scale(${z * (0.9 + appear * 0.1)})`, transformOrigin: '43% 52%', opacity: appear, whiteSpace: 'nowrap'}}>G63</div>
      </AbsoluteFill>
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 690, opacity: ease(f, 4, 14, 0, 1) * ease(f, 20, 28, 1, 0)}}>
        <div style={caps(22, INK)}>Meet the</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// small white instrument for full-bleed scenes
const MiniTacho: React.FC<{rpm: number; o: number}> = ({rpm, o}) => (
  <div style={{position: 'absolute', left: 405, top: 200, opacity: o}}>
    <Dial v={rpm} max={8000} size={270} color="#fff" red={6500} labels={[0, 2, 4, 6, 8]} unit="RPM × 1000" readout={String(Math.round(rpm / 10) * 10)} />
  </div>
);
const jitter = (f: number, amp: number) => (random(`j${f}`) - 0.5) * amp + Math.sin(f / 2.6) * amp * 0.4;

// ---------- S3: full-bleed drive -> collapses into floating card, pushed left ----------
const Drive: React.FC = () => {
  const f = useCurrentFrame();
  const col = ease(f, 122, 150, 0, 1);         // collapse into card
  const push = ease(f, 146, 162, 0, 1, Easing.in(Easing.cubic));
  const w = interpolate(col, [0, 1], [1080, 760]);
  const h = interpolate(col, [0, 1], [1920, 1100]);
  const rpm = interpolate(f, [0, 60, 150, 210], [3200, 5600, 6100, 4000], clamp) + jitter(f, 380);
  return (
    <Canvas>
      <div style={{position: 'absolute', left: (1080 - w) / 2 - push * 1100, top: (1920 - h) / 2 - col * 80, width: w, height: h,
        borderRadius: col * 44, overflow: 'hidden', boxShadow: `0 ${40 * col}px ${120 * col}px rgba(40,30,20,${0.35 * col})`}}>
        <Footage start={6} rate={2.2} scale={interpolate(f, [0, 162], [1.06, 1.16])} />
        <MiniTacho rpm={rpm} o={ease(f, 10, 30, 0, 1) * (1 - col)} />
        <AbsoluteFill style={{padding: '1150px 90px 0', opacity: 1 - col}}>
          <Line d={4} out={44}><div style={sans(96, 650, '#fff')}>Snow up to</div><div style={sans(96, 650, '#fff')}>the bumper.</div></Line>
        </AbsoluteFill>
        <AbsoluteFill style={{padding: '1150px 90px 0', opacity: 1 - col}}>
          <Line d={48} out={120}><div style={sans(96, 650, '#fff')}>He never</div><div style={{...serif(124, '#fff')}}>lifts off.</div></Line>
        </AbsoluteFill>
      </div>
      <div style={{position: 'absolute', top: 1620, left: 0, right: 0, textAlign: 'center', opacity: col * (1 - push)}}>
        <div style={caps(20, INK)}>Chapter I — The Forest</div>
      </div>
    </Canvas>
  );
};

// ---------- S4: spec sheet with dials ----------
const Specs: React.FC = () => {
  const f = useCurrentFrame();
  const enter = ease(f, 0, 22, 1, 0, outx); // slide in from right
  const draw = ease(f, 4, 34, 0, 1);
  const rpm = f < 30 ? 0 : interpolate(f, [30, 60, 95, 130, 180], [800, 7400, 5200, 6800, 4200], clamp) + jitter(f, 120);
  const thr = interpolate(f, [30, 55, 95, 130, 180], [0, 100, 70, 96, 55], clamp);
  const specs = [
    {n: 4.0, unit: 'L V8', label: 'Biturbo', d: 6, dec: 1},
    {n: 850, unit: 'Nm', label: 'Torque', d: 58, dec: 0},
    {n: 3, unit: 'locks', label: 'Differentials, 100%', d: 108, dec: 0},
  ];
  return (
    <AbsoluteFill style={{transform: `translateX(${enter * 1080}px)`}}><Canvas>
      <div style={{position: 'absolute', top: 150, left: 90, right: 90, display: 'flex', justifyContent: 'space-between'}}>
        <Line d={10}><span style={caps(20, INK)}>Instruments</span></Line>
        <Line d={14}><span style={caps(20)}>G 63 · 4.0 L</span></Line>
      </div>
      <div style={{position: 'absolute', top: 196, left: 90, width: 900 * draw, height: 1.5, background: INK}} />
      <div style={{position: 'absolute', top: 250, left: 90}}>
        <Dial v={rpm} max={8000} size={620} draw={draw} red={6500} labels={[0, 1, 2, 3, 4, 5, 6, 7, 8]} unit="RPM × 1000" readout={String(Math.round(Math.max(0, rpm) / 10) * 10)} />
      </div>
      <div style={{position: 'absolute', top: 560, left: 690}}>
        <Dial v={thr} max={100} size={330} draw={draw} sweep={180} labels={[0, 50, 100]} unit="THROTTLE" readout={`${Math.round(thr)}%`} />
      </div>
      {specs.map((s, i) => {
        const p = ease(f, s.d, s.d + 30, 0, 1, outx);
        const n = interpolate(f, [s.d, s.d + 34], [0, s.n], {...clamp, easing: outx}).toFixed(s.dec);
        return (
          <div key={i} style={{position: 'absolute', left: 90, right: 90, top: 960 + i * 250, opacity: p, transform: `translateY(${(1 - p) * 50}px)`}}>
            <div style={{height: 1.5, background: 'rgba(20,18,16,0.25)', width: `${p * 100}%`, marginBottom: 30}} />
            <div style={{display: 'flex', alignItems: 'baseline', gap: 18}}>
              <span style={sans(180, 700)}>{n}</span>
              <span style={serif(80, ACCENT)}>{s.unit}</span>
            </div>
            <div style={{...caps(20), marginTop: 6}}>{s.label}</div>
          </div>
        );
      })}
    </Canvas></AbsoluteFill>
  );
};

// ---------- S5: triptych with depth ----------
const TRI = [
  {src: 9, word: 'Snow.', pos: '50% 60%'},
  {src: 41.2, word: 'Steel.', pos: '50% 62%'},
  {src: 27, word: 'Nerve.', pos: '50% 58%'},
];
const Triptych: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{perspective: 2400}}><Canvas />
      <div style={{position: 'absolute', top: 210, left: 90}}><Line d={4}><span style={caps(20, INK)}>Three conditions</span></Line></div>
      {TRI.map((t, i) => {
        const d = 0 + i * 6;
        const p = ease(f, d, d + 26, 0, 1, outx);
        const x = 60 + i * 330;
        const drift = interpolate(f, [0, 90], [0, -40 * (i - 1)]);
        const exit = i === 1 ? 0 : ease(f, 64, 86, 0, 1);
        return (
          <div key={i} style={{position: 'absolute', left: x + drift + (i - 1) * exit * 700, top: 420, width: 300, height: 960, borderRadius: 30, overflow: 'hidden',
            transform: `translateY(${(1 - p) * 600}px) rotateY(${(1 - p) * (i - 1) * -35}deg) scale(${0.9 + p * 0.1})`, opacity: p * (1 - exit),
            boxShadow: '0 30px 80px rgba(40,30,20,0.3)'}}>
            <Sequence from={d} layout="none"><Footage start={t.src} pos={t.pos} scale={1.15 + f * 0.002} /></Sequence>
          </div>
        );
      })}
      {TRI.map((t, i) => (
        <div key={i} style={{position: 'absolute', top: 1430, left: 60 + i * 330, width: 300, textAlign: 'center', opacity: i === 1 ? 1 : 1 - ease(f, 60, 80, 0, 1)}}>
          <Line d={[4, 22, 42][i]}><span style={serif(84, ['#2F6FB0', INK, ACCENT][i])}>{t.word}</span></Line>
        </div>
      ))}
    </AbsoluteFill>
  );
};

// ---------- S6: middle card expands to full bleed, slow-mo burst ----------
const Burst: React.FC = () => {
  const f = useCurrentFrame();
  const ex = ease(f, 0, 26, 0, 1);
  const w = interpolate(ex, [0, 1], [300, 1080]), h = interpolate(ex, [0, 1], [960, 1920]);
  const l = interpolate(ex, [0, 1], [390, 0]), t = interpolate(ex, [0, 1], [420, 0]);
  const b = BURST - S6.from;
  const shake = f > b && f < b + 24 ? (random(`s${f}`) - 0.5) * 18 * (1 - (f - b) / 24) : 0;
  const flash = f >= b ? ease(f, b, b + 16, 1, 0) : 0;
  const rpm = (f < b ? interpolate(f, [0, b], [3400, 4200]) : interpolate(f, [b, b + 20, 144], [7800, 7200, 5600], clamp)) + jitter(f, 200);
  return (
    <AbsoluteFill><Canvas />
      <div style={{position: 'absolute', left: l, top: t, width: w, height: h, borderRadius: (1 - ex) * 30, overflow: 'hidden', transform: `translateX(${shake}px)`}}>
        <Footage start={41.2} rate={0.5} scale={interpolate(f, [0, 144], [1.1, 1.24])} />
        <MiniTacho rpm={rpm} o={ease(f, 24, 40, 0, 1)} />
        <AbsoluteFill style={{background: CREAM, opacity: flash * 0.9}} />
        <AbsoluteFill style={{alignItems: 'center', paddingTop: 1200}}>
          <Line d={8} out={b - 4}><span style={sans(100, 650, '#fff')}>This isn't driving.</span></Line>
        </AbsoluteFill>
        <AbsoluteFill style={{alignItems: 'center', paddingTop: 1020}}>
          <Line d={b + 4}><span style={{...serif(200, CREAM), textShadow: '0 6px 40px rgba(20,14,10,0.7)'}}>a feeling.</span></Line>
        </AbsoluteFill>
      </div>
    </AbsoluteFill>
  );
};

// ---------- S7: release, card recedes into the page, end titles ----------
const Finale: React.FC = () => {
  const f = useCurrentFrame();
  const shrink = ease(f, 132, 162, 0, 1);
  const w = interpolate(shrink, [0, 1], [1080, 620]), h = interpolate(shrink, [0, 1], [1920, 820]);
  const top = interpolate(shrink, [0, 1], [0, 330]);
  const line = ease(f, 152, 180, 0, 1);
  const rpm = interpolate(f, [0, 60, 150], [4200, 2600, 1100], clamp) + jitter(f, 90);
  const fin = 1;
  return (
    <AbsoluteFill style={{opacity: fin}}><Canvas />
      <div style={{position: 'absolute', left: (1080 - w) / 2, top, width: w, height: h, borderRadius: shrink * 36, overflow: 'hidden',
        boxShadow: `0 ${30 * shrink}px ${100 * shrink}px rgba(40,30,20,${0.3 * shrink})`}}>
        <Footage start={44} scale={interpolate(f, [0, 210], [1.12, 1.0])} pos="50% 50%" />
        <MiniTacho rpm={rpm} o={ease(f, 0, 14, 0, 1) * (1 - shrink)} />
        <AbsoluteFill style={{padding: '1150px 90px 0', opacity: 1 - shrink}}>
          <Line d={16} out={72}><div style={sans(92, 650, '#fff')}>Horsepower</div><div style={sans(92, 650, '#fff')}>belongs to the car.</div></Line>
        </AbsoluteFill>
        <AbsoluteFill style={{padding: '1150px 90px 0', opacity: 1 - shrink}}>
          <Line d={80} out={136}><div style={sans(92, 650, '#fff')}>Nerve belongs</div><div style={serif(124, '#fff')}>to the driver.</div></Line>
        </AbsoluteFill>
      </div>
      <div style={{position: 'absolute', top: 1180, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <div style={{width: 520 * line, height: 1.5, background: INK, marginBottom: 40}} />
        <Line d={156}><div style={sans(150, 800)}>G 63</div></Line>
        <Line d={164}><div style={{...serif(70, ACCENT), marginTop: 6}}>Would you take this road?</div></Line>
        <Line d={174}><div style={{...caps(18, INK), marginTop: 36}}>Hiver — Collection No. 01</div></Line>
      </div>
    </AbsoluteFill>
  );
};

export const TikTok: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{background: CREAM}}>
      <Audio src={staticFile('mix.wav')} />
      <Sequence from={S1.from} durationInFrames={S1.dur}><Hook /></Sequence>
      <Sequence from={S2.from} durationInFrames={S2.dur}><Knockout /></Sequence>
      <Sequence from={S3.from} durationInFrames={S3.dur}><Drive /></Sequence>
      <Sequence from={S4.from} durationInFrames={S4.dur}><Specs /></Sequence>
      <Sequence from={S5.from} durationInFrames={S5.dur}><Triptych /></Sequence>
      <Sequence from={S6.from} durationInFrames={S6.dur}><Burst /></Sequence>
      <Sequence from={S7.from} durationInFrames={S7.dur}><Finale /></Sequence>
    </AbsoluteFill>
  );
};
