import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill, Audio, Freeze, OffthreadVideo, Sequence, continueRender, delayRender,
  interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing, random,
} from 'remotion';

const RED = '#E10531';
const ICE = '#DDE8F2';
const SRC = staticFile('in.mp4');
const SERIF = 'Bodoni';
const SERIF_IT = 'BodoniIt';
const WIDE = 'Syncopate';
const MONO = 'SpaceMono';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// ---------- timeline (frames @30fps) ----------
const A = {from: 0, dur: 75};
const FZ = {from: 75, dur: 36};
const B = {from: 111, dur: 232};
const C = {from: 343, dur: 90};
const D = {from: 433, dur: 218};
const E = {from: 651, dur: 180};
const F = {from: 831, dur: 282};
export const TOTAL = F.from + F.dur;
const BURST = E.from + 102;

// ---------- fonts ----------
const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const fonts = [
      new FontFace(SERIF, `url(${staticFile('Bodoni.ttf')})`, {weight: '400 900'}),
      new FontFace(SERIF_IT, `url(${staticFile('BodoniIt.ttf')})`, {weight: '400 900', style: 'normal'}),
      new FontFace(WIDE, `url(${staticFile('Syncopate.ttf')})`),
      new FontFace(MONO, `url(${staticFile('SpaceMono.ttf')})`),
    ];
    Promise.all(fonts.map((f) => f.load())).then((ls) => {
      ls.forEach((f) => (document as any).fonts.add(f));
      continueRender(h);
    });
  }, [h]);
};

// ---------- SVG filters: RGB split + directional (whip) blur ----------
const Filters: React.FC<{id: string; rgb: number; whip: number}> = ({id, rgb, whip}) => (
  <svg width="0" height="0" style={{position: 'absolute'}}>
    <filter id={id} x="-10%" y="-10%" width="120%" height="120%" colorInterpolationFilters="sRGB">
      <feGaussianBlur in="SourceGraphic" stdDeviation={`${whip} ${whip * 0.05}`} result="b" />
      <feColorMatrix in="b" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
      <feOffset in="r" dx={rgb} dy="0" result="r2" />
      <feColorMatrix in="b" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g" />
      <feColorMatrix in="b" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="bl" />
      <feOffset in="bl" dx={-rgb} dy="0" result="b2" />
      <feBlend in="r2" in2="g" mode="screen" result="rg" />
      <feBlend in="rg" in2="b2" mode="screen" />
    </filter>
  </svg>
);

type Fx = 'none' | 'zoom' | 'whip' | 'glitch' | 'iris' | 'fade';
// ---------- footage with grade + entry transition ----------
const Clip: React.FC<{start: number; rate?: number; zoom?: [number, number]; dur: number; shake?: number; fx?: Fx; id: string}> = ({start, rate = 1, zoom = [1.04, 1.12], dur, shake = 0, fx = 'none', id}) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, 12], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  let s = interpolate(f, [0, dur], zoom, clamp);
  let tx = 0, rgb = 0, whip = 0, op = 1;
  let clip: string | undefined;
  if (fx === 'zoom') { s *= interpolate(t, [0, 1], [1.7, 1]); rgb = (1 - t) * 30; }
  if (fx === 'whip') { tx = (1 - t) * 900; whip = (1 - t) * 90; }
  if (fx === 'glitch') { rgb = f < 10 ? (random(`g${f}`) - 0.3) * 50 : 0; tx = f < 8 ? (random(`gx${f}`) - 0.5) * 60 : 0; }
  if (fx === 'iris') { const r = interpolate(f, [0, 16], [0, 1500], {...clamp, easing: Easing.inOut(Easing.cubic)}); clip = `circle(${r}px at 50% 42%)`; }
  if (fx === 'fade') op = interpolate(f, [0, 18], [0, 1], clamp);
  if (shake) { tx += (random(`x${f}`) - 0.5) * shake; rgb += Math.abs(random(`rs${f}`) - 0.5) * shake * 0.8; }
  const sy = shake ? (random(`y${f}`) - 0.5) * shake : 0;
  const fid = `f-${id}`;
  return (
    <AbsoluteFill style={{clipPath: clip, opacity: op}}>
      <Filters id={fid} rgb={rgb} whip={whip} />
      <AbsoluteFill style={{transform: `translate(${tx}px,${sy}px) scale(${s})`, filter: rgb || whip ? `url(#${fid})` : undefined}}>
        <OffthreadVideo src={SRC} muted startFrom={Math.round(start * 30)} playbackRate={rate}
          style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'contrast(1.28) saturate(0.5) brightness(1.04)'}} />
      </AbsoluteFill>
      <Grade />
    </AbsoluteFill>
  );
};

// editorial grade: icy split-tone, crushed top band, deep blacks, grain
const Grade: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, #1d3b5c 0%, #7d9bb8 45%, #2a2018 100%)', mixBlendMode: 'soft-light', opacity: 0.75}} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(4,8,14,0.92) 0%, rgba(4,8,14,0.55) 16%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 62%, rgba(0,0,0,0.85) 100%)'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 42%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.6) 100%)'}} />
      <AbsoluteFill style={{opacity: 0.1, mixBlendMode: 'overlay', backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' seed='${f % 9}'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`}} />
    </AbsoluteFill>
  );
};

// ---------- typography ----------
// line reveals from behind a mask, fashion-editorial style
const Reveal: React.FC<{children: React.ReactNode; delay?: number; style?: React.CSSProperties}> = ({children, delay = 0, style}) => {
  const f = useCurrentFrame();
  const p = interpolate(f - delay, [0, 16], [0, 1], {...clamp, easing: Easing.out(Easing.exp)});
  return (
    <div style={{overflow: 'hidden', paddingBottom: '0.12em', ...style}}>
      <div style={{transform: `translateY(${(1 - p) * 110}%) skewY(${(1 - p) * 6}deg)`, opacity: p > 0 ? 1 : 0}}>{children}</div>
    </div>
  );
};
const Out: React.FC<{at: number; children: React.ReactNode}> = ({at, children}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at - 8, at], [1, 0], clamp);
  const b = interpolate(f, [at - 8, at], [0, 12], clamp);
  return <AbsoluteFill style={{opacity: o, filter: b ? `blur(${b}px)` : undefined}}>{children}</AbsoluteFill>;
};
const serif = (size: number, color = ICE): React.CSSProperties => ({fontFamily: SERIF_IT, fontStyle: 'italic', fontWeight: 640, fontSize: size, lineHeight: 0.95, color, letterSpacing: -2, textShadow: '0 2px 6px rgba(0,0,0,0.6), 0 8px 40px rgba(0,0,0,0.85)'});
const wide = (size: number, color = '#fff'): React.CSSProperties => ({fontFamily: WIDE, fontSize: size, color, letterSpacing: size * 0.35, textTransform: 'uppercase'});

// two-line editorial block: small tracked caps + big italic serif
const Editorial: React.FC<{kicker?: string; lines: {t: string; red?: boolean}[]; y?: number; size?: number; out?: number; align?: 'left' | 'center' | 'right'}> = ({kicker, lines, y = 1070, size = 150, out = 9999, align = 'left'}) => {
  const f = useCurrentFrame();
  const line = interpolate(f, [0, 20], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return (
    <Out at={out}>
      <div style={{position: 'absolute', top: y - 260, left: 0, right: 0, height: 760, opacity: line,
        background: 'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(3,6,10,0.55) 35%, rgba(3,6,10,0.55) 70%, rgba(0,0,0,0) 100%)'}} />
      <div style={{position: 'absolute', top: y, left: 80, right: 80, textAlign: align}}>
        {kicker && (
          <div style={{display: 'flex', alignItems: 'center', gap: 22, justifyContent: align === 'center' ? 'center' : align === 'right' ? 'flex-end' : 'flex-start', marginBottom: 26}}>
            <div style={{width: 90 * line, height: 2, background: RED}} />
            <Reveal><span style={wide(22)}>{kicker}</span></Reveal>
          </div>
        )}
        {lines.map((l, i) => (
          <Reveal key={i} delay={4 + i * 7}><span style={serif(size, l.red ? RED : ICE)}>{l.t}</span></Reveal>
        ))}
      </div>
    </Out>
  );
};

// big wide-caps hit
const Hit: React.FC<{t: string; size?: number; y?: number; sub?: string; color?: string}> = ({t, size = 120, y = 820, sub, color = '#fff'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 200, stiffness: 120}});
  const track = interpolate(p, [0, 1], [1.2, 0.18]);
  return (
    <div style={{position: 'absolute', top: y, left: 0, right: 0, textAlign: 'center'}}>
      <div style={{fontFamily: WIDE, fontSize: size, color, letterSpacing: size * track, opacity: p, filter: `blur(${(1 - p) * 16}px)`, marginRight: -size * track, textShadow: '0 10px 50px rgba(0,0,0,0.6)'}}>{t}</div>
      {sub && <Reveal delay={10} style={{marginTop: 18}}><span style={serif(64)}>{sub}</span></Reveal>}
    </div>
  );
};

// ---------- transitions overlays ----------
const Flash: React.FC<{dur?: number; color?: string; max?: number}> = ({dur = 8, color = '#fff', max = 0.9}) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{background: color, opacity: interpolate(f, [0, dur], [max, 0], clamp), mixBlendMode: color === '#fff' ? 'screen' : 'normal'}} />;
};
// horizontal blinds: cover in, reveal out (centered on the cut)
const Blinds: React.FC<{n?: number; color?: string}> = ({n = 10, color = '#0a0a0a'}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      {Array.from({length: n}).map((_, i) => {
        const d = i * 1.2;
        const inP = interpolate(f - d, [0, 9], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
        const outP = interpolate(f - 12 - d, [0, 9], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
        return <div key={i} style={{position: 'absolute', top: (1920 / n) * i, height: 1920 / n + 1, left: 0, width: 1080,
          background: i % 3 === 1 ? RED : color, transformOrigin: outP > 0 ? 'right' : 'left', transform: `scaleX(${outP > 0 ? 1 - outP : inP})`}} />;
      })}
    </AbsoluteFill>
  );
};
// warm light-leak burn
const Leak: React.FC<{dur?: number}> = ({dur = 24}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, dur * 0.35, dur], [0, 1, 0], clamp);
  const x = interpolate(f, [0, dur], [-20, 120]);
  return <AbsoluteFill style={{mixBlendMode: 'screen', opacity: o,
    background: `radial-gradient(circle at ${x}% 35%, rgba(255,120,40,0.95), rgba(225,5,49,0.6) 25%, rgba(0,0,0,0) 60%), radial-gradient(circle at ${100 - x}% 80%, rgba(255,200,120,0.7), rgba(0,0,0,0) 45%)`}} />;
};
// cinema bars opening
const Bars: React.FC = () => {
  const f = useCurrentFrame();
  const h = interpolate(f, [0, 22], [960, 0], {...clamp, easing: Easing.inOut(Easing.exp)});
  return <AbsoluteFill><div style={{position: 'absolute', top: 0, left: 0, right: 0, height: h, background: '#000'}} /><div style={{position: 'absolute', bottom: 0, left: 0, right: 0, height: h, background: '#000'}} /></AbsoluteFill>;
};

// ---------- gauges ----------
const RPM_K: [number, number][] = [[0, 850], [55, 950], [75, 6900], [100, 3100], [111, 4900], [200, 5700], [262, 4400], [330, 6300], [343, 6000], [433, 5100], [560, 5900], [640, 4600], [651, 3900], [745, 3600], [BURST, 7700], [800, 7100], [831, 3600], [960, 2500], [1060, 1400], [TOTAL, 850]];
const THR_K: [number, number][] = [[0, 4], [55, 6], [75, 100], [100, 28], [111, 78], [262, 62], [330, 95], [433, 72], [651, 55], [745, 48], [BURST, 100], [800, 92], [831, 40], [960, 22], [1060, 6], [TOTAL, 0]];
const kf = (k: [number, number][], f: number) => interpolate(f, k.map((x) => x[0]), k.map((x) => x[1]), clamp);
const polar = (cx: number, cy: number, r: number, deg: number) => [cx + r * Math.cos((deg * Math.PI) / 180), cy + r * Math.sin((deg * Math.PI) / 180)];
const arc = (cx: number, cy: number, r: number, a0: number, a1: number) => {
  const [x0, y0] = polar(cx, cy, r, a0); const [x1, y1] = polar(cx, cy, r, a1);
  return `M ${x0} ${y0} A ${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1}`;
};

const Tacho: React.FC<{rpm: number; size?: number}> = ({rpm, size = 400}) => {
  const c = size / 2, r = size / 2 - 18;
  const A0 = 135, SW = 270; // start angle, sweep
  const ang = (v: number) => A0 + (v / 8000) * SW;
  const na = ang(rpm);
  const [nx, ny] = polar(c, c, r - 24, na);
  const [tx, ty] = polar(c, c, -26, na);
  const red = rpm > 6500;
  return (
    <svg width={size} height={size}>
      <defs><filter id="glow"><feGaussianBlur stdDeviation="5" /><feMerge><feMergeNode /><feMergeNode in="SourceGraphic" /></feMerge></filter></defs>
      <circle cx={c} cy={c} r={r + 10} fill="rgba(5,8,12,0.55)" />
      <path d={arc(c, c, r, A0, ang(6500))} stroke="rgba(255,255,255,0.85)" strokeWidth={2} fill="none" />
      <path d={arc(c, c, r, ang(6500), ang(8000))} stroke={RED} strokeWidth={10} fill="none" />
      <path d={arc(c, c, r - 40, A0, na)} stroke={red ? RED : 'rgba(221,232,242,0.35)'} strokeWidth={6} fill="none" />
      {Array.from({length: 33}).map((_, i) => {
        const v = i * 250; const a = ang(v); const major = i % 4 === 0;
        const [x0, y0] = polar(c, c, r - (major ? 24 : 12), a); const [x1, y1] = polar(c, c, r, a);
        const [lx, ly] = polar(c, c, r - 52, a);
        return <g key={i}>
          <line x1={x0} y1={y0} x2={x1} y2={y1} stroke={v >= 6500 ? RED : '#fff'} strokeWidth={major ? 3 : 1.4} />
          {major && <text x={lx} y={ly + 9} textAnchor="middle" fontFamily={MONO} fontSize={24} fill={v >= 6500 ? RED : '#fff'}>{v / 1000}</text>}
        </g>;
      })}
      <line x1={tx} y1={ty} x2={nx} y2={ny} stroke={RED} strokeWidth={5} strokeLinecap="round" filter="url(#glow)" />
      <circle cx={c} cy={c} r={14} fill="#111" stroke={RED} strokeWidth={3} />
      <text x={c} y={c + 78} textAnchor="middle" fontFamily={MONO} fontSize={44} fill={red ? RED : '#fff'}>{String(Math.round(rpm / 10) * 10).padStart(4, '0')}</text>
      <text x={c} y={c + 108} textAnchor="middle" fontFamily={WIDE} fontSize={14} letterSpacing={5} fill="rgba(255,255,255,0.7)">RPM ×1000</text>
    </svg>
  );
};

const Throttle: React.FC<{v: number; size?: number}> = ({v, size = 300}) => {
  const c = size / 2, r = size / 2 - 16;
  const A0 = 180, SW = 180;
  const na = A0 + (v / 100) * SW;
  const [nx, ny] = polar(c, c, r - 18, na);
  return (
    <svg width={size} height={size / 2 + 90}>
      <path d={arc(c, c, r + 8, 180, 359.9)} stroke="none" fill="rgba(5,8,12,0.55)" />
      <path d={arc(c, c, r, 180, 359.9)} stroke="rgba(255,255,255,0.85)" strokeWidth={2} fill="none" />
      <path d={arc(c, c, r - 22, 180, Math.max(180.1, na))} stroke={v > 90 ? RED : ICE} strokeWidth={14} fill="none" opacity={0.9} />
      {Array.from({length: 11}).map((_, i) => {
        const a = A0 + i * 18; const [x0, y0] = polar(c, c, r - (i % 5 === 0 ? 14 : 7), a); const [x1, y1] = polar(c, c, r, a);
        return <line key={i} x1={x0} y1={y0} x2={x1} y2={y1} stroke="#fff" strokeWidth={i % 5 === 0 ? 3 : 1.5} />;
      })}
      <line x1={c} y1={c} x2={nx} y2={ny} stroke={RED} strokeWidth={4} strokeLinecap="round" />
      <circle cx={c} cy={c} r={9} fill={RED} />
      <text x={c} y={c + 48} textAnchor="middle" fontFamily={MONO} fontSize={40} fill="#fff">{Math.round(v)}%</text>
      <text x={c} y={c + 76} textAnchor="middle" fontFamily={WIDE} fontSize={14} letterSpacing={5} fill="rgba(255,255,255,0.7)">THROTTLE</text>
    </svg>
  );
};

const Cluster: React.FC = () => {
  const f = useCurrentFrame();
  const vis = interpolate(f, [8, 30, C.from - 6, C.from, C.from + C.dur, C.from + C.dur + 10, TOTAL - 70, TOTAL - 40], [0, 1, 1, 0, 0, 1, 1, 0], clamp);
  const jit = (random(`j${f}`) - 0.5) * 260 + Math.sin(f / 2.3) * 120;
  const rpm = Math.max(700, Math.min(7950, kf(RPM_K, f) + (kf(RPM_K, f) > 1200 ? jit : jit * 0.2)));
  const thr = Math.max(0, Math.min(100, kf(THR_K, f) + (random(`t${f}`) - 0.5) * 8));
  const gear = rpm > 6000 ? '2' : rpm > 3000 ? '3' : '1';
  return (
    <AbsoluteFill style={{opacity: vis, transform: `translateY(${(1 - vis) * 60}px)`}}>
      <div style={{position: 'absolute', left: 50, top: 1450}}><Tacho rpm={rpm} /></div>
      <div style={{position: 'absolute', right: 60, top: 1520}}><Throttle v={thr} /></div>
      <div style={{position: 'absolute', right: 70, top: 1760, display: 'flex', gap: 30, alignItems: 'baseline'}}>
        <span style={wide(16, 'rgba(255,255,255,0.7)')}>gear</span>
        <span style={{fontFamily: MONO, fontSize: 52, color: '#fff'}}>{gear}<span style={{color: RED, fontSize: 30}}>L</span></span>
        <span style={wide(16, 'rgba(255,255,255,0.7)')}>4matic</span>
      </div>
    </AbsoluteFill>
  );
};

// magazine header + frame
const Masthead: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [10, 30, C.from - 4, C.from, C.from + C.dur - 2, C.from + C.dur + 8], [0, 1, 1, 0, 0, 1], clamp);
  const line = interpolate(f, [10, 40], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const sec = f / 30;
  const tc = `00:${String(Math.floor(sec)).padStart(2, '0')}:${String(f % 30).padStart(2, '0')}`;
  return (
    <AbsoluteFill style={{opacity: o}}>
      <div style={{position: 'absolute', top: 80, left: 70, right: 70, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end'}}>
        <span style={{fontFamily: SERIF, fontWeight: 700, fontSize: 72, color: '#fff', letterSpacing: -1}}>G<span style={{color: RED}}>—</span>63</span>
        <div style={{textAlign: 'right'}}>
          <div style={wide(16)}>the winter issue</div>
          <div style={{fontFamily: MONO, fontSize: 22, color: 'rgba(255,255,255,0.75)', marginTop: 6}}>№01 · {tc}</div>
        </div>
      </div>
      <div style={{position: 'absolute', top: 178, left: 70, width: 940 * line, height: 2, background: 'rgba(255,255,255,0.8)'}} />
      <div style={{position: 'absolute', left: 34, top: 760, transform: 'rotate(-90deg)', transformOrigin: 'left top', ...wide(13, 'rgba(255,255,255,0.6)')}}>off-road couture — shot on a phone</div>
    </AbsoluteFill>
  );
};

// ---------- collage ----------
const Collage: React.FC = () => {
  const f = useCurrentFrame();
  const panels = [
    {src: 9, word: 'Snow', n: '01'},
    {src: 41.2, word: 'Steel', n: '02'},
    {src: 27, word: 'Nerve', n: '03', red: true},
  ];
  return (
    <AbsoluteFill style={{background: '#0b0b0b'}}>
      {panels.map((p, i) => {
        const d = i * 6;
        const sp = interpolate(f - d, [0, 14], [0, 1], {...clamp, easing: Easing.out(Easing.exp)});
        return (
          <div key={i} style={{position: 'absolute', left: 40, width: 1000, top: 60 + i * 610, height: 580, overflow: 'hidden',
            clipPath: `inset(0 ${(1 - sp) * 100}% 0 0)`}}>
            <Sequence from={d} layout="none">
              <OffthreadVideo src={SRC} muted startFrom={Math.round(p.src * 30)}
                style={{position: 'absolute', width: 1080, height: 1920, left: -40, top: -700, objectFit: 'cover',
                  transform: `scale(${1.2 + f * 0.003})`, filter: 'contrast(1.35) saturate(0.35) brightness(1.05)'}} />
            </Sequence>
            <AbsoluteFill style={{background: 'linear-gradient(180deg, #1d3b5c, #2a2018)', mixBlendMode: 'soft-light', opacity: 0.8}} />
            <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(0,0,0,0.85), rgba(0,0,0,0.25) 60%, rgba(0,0,0,0.1))'}} />
            <div style={{position: 'absolute', left: 40, bottom: 20}}>
              <Reveal delay={d + 8}><span style={serif(200, p.red ? RED : ICE)}>{p.word}</span></Reveal>
            </div>
            <div style={{position: 'absolute', right: 34, top: 28, fontFamily: MONO, fontSize: 30, color: '#fff', opacity: sp}}>{p.n}/03</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Progress: React.FC = () => {
  const f = useCurrentFrame();
  return <div style={{position: 'absolute', left: 0, bottom: 0, height: 6, width: `${(f / TOTAL) * 100}%`, background: RED}} />;
};

export const Reel: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const vol = interpolate(f, [0, 10, TOTAL - 45, TOTAL], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Audio src={SRC} volume={vol} />

      {/* A — opening */}
      <Sequence from={A.from} durationInFrames={A.dur}>
        <Clip id="a" start={0} dur={A.dur} zoom={[1.0, 1.14]} />
        <Sequence from={18}><Editorial kicker="chapter one" lines={[{t: 'No road.'}]} y={1080} size={170} /></Sequence>
        <Bars />
      </Sequence>

      {/* freeze — Enter G 63 */}
      <Sequence from={FZ.from} durationInFrames={FZ.dur}>
        <Freeze frame={74}><Clip id="fz" start={0} dur={1} zoom={[1.22, 1.22]} /></Freeze>
        <AbsoluteFill style={{background: 'rgba(0,0,0,0.35)'}} />
        <div style={{position: 'absolute', top: 760, left: 0, right: 0, textAlign: 'center'}}><Reveal><span style={serif(130)}>enter the</span></Reveal></div>
        <Hit t="G 63" size={170} y={900} />
        <Flash dur={6} color={RED} max={0.75} />
      </Sequence>

      {/* B — plowing */}
      <Sequence from={B.from} durationInFrames={B.dur}>
        <Clip id="b" fx="whip" start={3} rate={2.2} dur={B.dur} zoom={[1.08, 1.16]} />
        <Sequence from={12} durationInFrames={104}><Editorial kicker="conditions" lines={[{t: 'Snow up'}, {t: 'to the bumper.'}]} out={104} size={128} y={1030} /></Sequence>
        <Sequence from={118} durationInFrames={114}><Editorial kicker="the driver" lines={[{t: 'He never'}, {t: 'lifts off.', red: true}]} out={114} size={170} /></Sequence>
      </Sequence>

      {/* C — collage */}
      <Sequence from={C.from} durationInFrames={C.dur}><Collage /></Sequence>

      {/* D */}
      <Sequence from={D.from} durationInFrames={D.dur}>
        <Clip id="d" fx="zoom" start={20} rate={2.2} dur={D.dur} zoom={[1.16, 1.06]} />
        <Sequence from={10} durationInFrames={92}><Editorial kicker="a note" lines={[{t: "This isn't"}, {t: 'driving.'}]} out={92} /></Sequence>
        <Sequence from={96} durationInFrames={122}><Editorial kicker="it is" align="center" lines={[{t: 'a feeling.', red: true}]} y={1060} size={200} out={122} /></Sequence>
      </Sequence>

      {/* E — slow-mo, burst */}
      <Sequence from={E.from} durationInFrames={BURST - E.from}>
        <Clip id="e" fx="fade" start={41} rate={0.5} dur={E.dur} zoom={[1.05, 1.18]} />
        <Sequence from={12}><Editorial kicker="chapter two" lines={[{t: 'We follow.'}]} /></Sequence>
      </Sequence>
      <Sequence from={BURST} durationInFrames={E.from + E.dur - BURST}>
        <Clip id="e2" fx="glitch" start={41 + ((BURST - E.from) / 30) * 0.5} rate={0.5} dur={E.from + E.dur - BURST} zoom={[1.25, 1.32]} shake={22} />
        <Flash dur={10} />
        <Hit t="HE OPENS" size={92} y={700} />
        <Sequence from={8}><Hit t="THE ROAD" size={92} y={830} color={RED} /></Sequence>
      </Sequence>

      {/* F — release */}
      <Sequence from={F.from} durationInFrames={F.dur}>
        <AbsoluteFill style={{background: '#000'}} />
        <Clip id="f" fx="iris" start={44} dur={F.dur} zoom={[1.12, 1.0]} />
        <Sequence from={16} durationInFrames={100}><Editorial kicker="fact" lines={[{t: 'Horsepower'}, {t: 'belongs'}, {t: 'to the car.'}]} y={960} size={140} out={100} /></Sequence>
        <Sequence from={104} durationInFrames={140}><Editorial kicker="truth" lines={[{t: 'Nerve belongs'}, {t: 'to the driver.', red: true}]} y={1060} size={140} out={140} /></Sequence>
      </Sequence>

      <Masthead />
      <Cluster />

      {/* transitions on cuts */}
      <Sequence from={FZ.from - 2} durationInFrames={10}><Flash dur={8} /></Sequence>
      <Sequence from={C.from - 12} durationInFrames={26}><Blinds /></Sequence>
      <Sequence from={C.from + C.dur - 6} durationInFrames={20}><Flash dur={10} /></Sequence>
      <Sequence from={E.from - 10} durationInFrames={30}><Leak dur={30} /></Sequence>
      <Sequence from={F.from - 14} durationInFrames={14}><Flash dur={14} color="#000" max={0} /></Sequence>
      <Sequence from={TOTAL - 30} durationInFrames={30}><AbsoluteFill style={{background: '#000', opacity: interpolate(f, [TOTAL - 30, TOTAL], [0, 1], clamp)}} /></Sequence>
      <Progress />
    </AbsoluteFill>
  );
};
