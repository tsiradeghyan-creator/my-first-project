import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame, interpolate, random, Easing} from 'remotion';
import {useGreekFonts} from '../Greece';
import {SC, TXT} from './common';

// broadcast comic 2D: thick ink lines, panels, Ben-Day dots, balloons, SFX lettering, camera travelling across a page
const PAPER = '#FBF3E4', K = '#111', CY = '#29B6F6', MG = '#EC407A', YL = '#FFD54F', WH = '#ffffff', SKIN = '#FFE0C2';
const SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = io) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});
const pop = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], {...clamp, easing: Easing.out(Easing.back(2.6))});
const boil = (f: number, k: string, a = 2) => (random(`${k}${Math.floor(f / 3)}`) - 0.5) * a;

const dots = (c: string, s = 14, r = 3.2) => ({backgroundImage: `radial-gradient(circle, ${c} ${r}px, transparent ${r + 0.6}px)`, backgroundSize: `${s}px ${s}px`});
const Panel: React.FC<{x: number; y: number; w: number; h: number; bg: string; dot?: string; children?: React.ReactNode}> = ({x, y, w, h, bg, dot, children}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, background: bg, border: `10px solid ${K}`, overflow: 'hidden', boxSizing: 'border-box'}}>
    {dot && <div style={{position: 'absolute', inset: 0, ...dots(dot), opacity: 0.55}} />}
    {children}
  </div>
);
const Caption: React.FC<{children: React.ReactNode; x: number; y: number; f: number; at: number; w?: number; bg?: string; size?: number}> = ({children, x, y, f, at, w, bg = YL, size = 44}) => {
  const p = pop(f, at);
  return <div style={{position: 'absolute', left: x, top: y, width: w, background: bg, border: `6px solid ${K}`, padding: '14px 22px', boxShadow: `8px 8px 0 ${K}`, transform: `scale(${p}) rotate(${boil(f, 'cap' + at, 1)}deg)`, transformOrigin: '0 0', opacity: p > 0.01 ? 1 : 0}}>
    <span style={{fontFamily: SANS, fontWeight: 800, fontSize: size, color: K, lineHeight: 1.15, textTransform: 'uppercase'}}>{children}</span></div>;
};
const Balloon: React.FC<{children: React.ReactNode; x: number; y: number; f: number; at: number; tail?: 'left' | 'right'; w?: number}> = ({children, x, y, f, at, tail = 'left', w = 620}) => {
  const p = pop(f, at, 9);
  return <div style={{position: 'absolute', left: x, top: y, width: w, transform: `scale(${p})`, transformOrigin: tail === 'left' ? '10% 100%' : '90% 100%', opacity: p > 0.01 ? 1 : 0}}>
    <div style={{background: WH, border: `6px solid ${K}`, borderRadius: '50% / 42%', padding: '34px 46px', textAlign: 'center'}}><span style={{fontFamily: SANS, fontWeight: 800, fontSize: 46, color: K, lineHeight: 1.15}}>{children}</span></div>
    <svg width={80} height={60} style={{position: 'absolute', [tail]: 80, bottom: -48}}><path d={tail === 'left' ? 'M 10 0 L 0 56 L 46 0' : 'M 70 0 L 80 56 L 34 0'} fill={WH} stroke={K} strokeWidth={6} strokeLinejoin="round" /><rect x={tail === 'left' ? 12 : 30} y={-6} width={36} height={10} fill={WH} /></svg>
  </div>;
};
const Burst: React.FC<{text: string; x: number; y: number; f: number; at: number; size?: number; color?: string; r?: number}> = ({text, x, y, f, at, size = 150, color = YL, r = 260}) => {
  const p = pop(f, at, 8);
  const pts = [...Array(28)].map((_, i) => { const a = (i / 28) * Math.PI * 2; const rr = i % 2 ? r * 0.72 : r + (random(`b${at}${i}`) - 0.5) * 50; return `${Math.cos(a) * rr},${Math.sin(a) * rr * 0.75}`; }).join(' ');
  return <div style={{position: 'absolute', left: x, top: y, transform: `scale(${p}) rotate(${-6 + boil(f, 'bu' + at, 3)}deg)`, opacity: p > 0.01 ? 1 : 0}}>
    <svg width={r * 2.4} height={r * 2} viewBox={`${-r * 1.2} ${-r} ${r * 2.4} ${r * 2}`} style={{position: 'absolute', left: -r * 1.2, top: -r}}><polygon points={pts} fill={color} stroke={K} strokeWidth={10} strokeLinejoin="round" /></svg>
    <div style={{position: 'absolute', left: -r, width: r * 2, top: -size * 0.6, textAlign: 'center', fontFamily: SANS, fontWeight: 900, fontStretch: '70%', fontSize: size, color: MG, WebkitTextStroke: `8px ${K}`, paintOrder: 'stroke fill', textShadow: `8px 8px 0 ${K}`}}>{text}</div>
  </div>;
};
// comic character (outlined, cel shaded)
const Guy: React.FC<{x: number; y: number; s?: number; walk?: number; face?: 'ok' | 'shock'; f: number; flip?: boolean}> = ({x, y, s = 1, walk = 0, face = 'ok', f, flip}) => {
  const lg = Math.sin(walk) * 24, bob = Math.abs(Math.sin(walk)) * 8;
  const ow = 7;
  return (
    <g transform={`translate(${x + boil(f, 'gx')} ${y - bob}) scale(${flip ? -s : s} ${s})`} strokeLinejoin="round" strokeLinecap="round">
      <path d={`M -20 90 L ${-20 + lg} 190`} stroke={K} strokeWidth={30} /><path d={`M -20 90 L ${-20 + lg} 190`} stroke={CY} strokeWidth={16} />
      <path d={`M 20 90 L ${20 - lg} 190`} stroke={K} strokeWidth={30} /><path d={`M 20 90 L ${20 - lg} 190`} stroke={CY} strokeWidth={16} />
      <path d="M -60 -40 Q -66 100 -40 110 L 40 110 Q 66 100 60 -40 Q 0 -66 -60 -40 Z" fill={MG} stroke={K} strokeWidth={ow} />
      <path d="M 10 -50 Q 50 -46 58 -30 L 58 100 Q 40 110 20 110 Z" fill="rgba(0,0,0,0.18)" />
      <circle cx={0} cy={-110} r={62} fill={SKIN} stroke={K} strokeWidth={ow} />
      <path d="M 18 -160 A 62 62 0 0 1 58 -96 Q 40 -120 20 -116 Z" fill="rgba(0,0,0,0.12)" />
      <path d="M -64 -118 Q -60 -186 6 -176 Q 66 -170 60 -120 Q 40 -150 -10 -146 Q -40 -140 -64 -118 Z" fill={K} />
      {face === 'shock' ? <><circle cx={-18} cy={-106} r={13} fill={WH} stroke={K} strokeWidth={5} /><circle cx={22} cy={-106} r={13} fill={WH} stroke={K} strokeWidth={5} /><circle cx={-18} cy={-106} r={4} fill={K} /><circle cx={22} cy={-106} r={4} fill={K} /><ellipse cx={4} cy={-72} rx={12} ry={16} fill={K} />
        <path d="M 60 -150 q 14 22 0 30 q -14 -8 0 -30 Z" fill={CY} stroke={K} strokeWidth={4} /></>
        : <><circle cx={-18} cy={-106} r={6} fill={K} /><circle cx={22} cy={-106} r={6} fill={K} /><path d="M -14 -80 Q 4 -66 24 -80" stroke={K} strokeWidth={6} fill="none" /></>}
    </g>
  );
};

// the page: 6 panels; the camera travels between them
const PANELS = [
  {x: 40, y: 40, w: 1000, h: 1000},     // 0 hook
  {x: 40, y: 1080, w: 1000, h: 800},    // 1 title splash
  {x: 1100, y: 40, w: 1000, h: 1840},   // 2 ponr (tall)
  {x: 2140, y: 40, w: 1000, h: 900},    // 3 example
  {x: 2140, y: 980, w: 1000, h: 900},   // 4 rule
  {x: 3180, y: 40, w: 1000, h: 1840},   // 5 cta
];
const STARTS = [SC.hook, SC.title, SC.ponr, SC.ex, SC.rule, SC.cta];

const Page: React.FC<{f: number}> = ({f}) => {
  const L = (i: number) => f - STARTS[i];
  const P2 = PANELS[2];
  const walkL = L(2);
  const gx = 520;
  const guyX = interpolate(walkL, [10, 120], [140, 760], clamp);
  const passed = walkL > 10 + ((gx + 60 - 140) / 620) * 110;
  const slam = 10 + ((gx + 60 - 140) / 620) * 110;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 4220, height: 1920, background: PAPER}}>
      <div style={{position: 'absolute', inset: 0, ...dots('#e9dcc4', 22, 2.5)}} />
      {/* 0 HOOK: speed lines, thumb, STOP */}
      <Panel {...PANELS[0]} bg={CY} dot={WH}>
        <svg width={1000} height={1000} style={{position: 'absolute'}}>
          {f < 24 && [...Array(24)].map((_, i) => <line key={i} x1={100 + i * 36} y1={0} x2={100 + i * 36 + boil(f, 'sl' + i, 30)} y2={1000} stroke={WH} strokeWidth={6} opacity={0.8} />)}
          <rect x={300} y={180} width={400} height={700} rx={50} fill={K} /><rect x={322} y={202} width={356} height={656} rx={34} fill={WH} />
          {[0, 1, 2, 3].map((i) => <rect key={i} x={346} y={((i * 170 - (f < 22 ? f * 60 : 22 * 60)) % 680 + 680) % 680 + 220} width={308} height={140} rx={16} fill={[MG, YL, CY, MG][i]} stroke={K} strokeWidth={5} />)}
          <g transform={`translate(${560} ${f < 22 ? 760 - (f % 6) * 50 : 700})`}><path d="M -50 0 Q -60 -120 0 -130 Q 60 -120 50 0 L 50 200 L -50 200 Z" fill={SKIN} stroke={K} strokeWidth={8} /><path d="M -30 -100 Q 0 -120 30 -100" stroke={K} strokeWidth={5} fill="none" /></g>
        </svg>
        {f < 22 && <div style={{position: 'absolute', left: 40, top: 60, fontFamily: SANS, fontWeight: 900, fontSize: 90, color: WH, WebkitTextStroke: `6px ${K}`, paintOrder: 'stroke fill', transform: 'rotate(-8deg)'}}>ՍՎԱՅՓ ՍՎԱՅՓ</div>}
      </Panel>
      {f >= 22 && f < SC.title + 10 && <Burst text="ՍՏՈՊ!" x={540} y={300} f={f} at={22} size={170} r={300} />}
      <Caption x={80} y={880} f={f} at={30} w={700}>{TXT.hook}</Caption>
      {/* 1 TITLE splash */}
      <Panel {...PANELS[1]} bg={MG} dot={YL}>
        <svg width={1000} height={800} style={{position: 'absolute'}}>{[...Array(30)].map((_, i) => { const a = (i / 30) * Math.PI * 2 + f * 0.01; return <polygon key={i} points={`500,400 ${500 + Math.cos(a) * 900},${400 + Math.sin(a) * 900} ${500 + Math.cos(a + 0.1) * 900},${400 + Math.sin(a + 0.1) * 900}`} fill={i % 2 ? YL : MG} opacity={0.6} />; })}</svg>
        <div style={{position: 'absolute', left: 60, top: 70, width: 200, height: 200, borderRadius: 100, background: YL, border: `8px solid ${K}`, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${pop(f, SC.title + 6)}) rotate(-10deg)`, fontFamily: SANS, fontWeight: 900, fontSize: 96, color: K}}>#01</div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 360, textAlign: 'center', transform: `scale(${pop(f, SC.title + 14)}) rotate(-4deg)`, fontFamily: SANS, fontWeight: 900, fontStretch: '72%', fontSize: 150, lineHeight: 0.95, color: YL, WebkitTextStroke: `10px ${K}`, paintOrder: 'stroke fill', textShadow: `12px 12px 0 ${K}`}}>{TXT.title.toUpperCase()}</div>
      </Panel>
      <Caption x={80} y={1110} f={f} at={SC.title + 4} bg={WH}>{TXT.kicker}</Caption>
      {/* 2 POINT OF NO RETURN */}
      <Panel {...P2} bg={YL} dot={MG}>
        <svg width={1000} height={1840} style={{position: 'absolute'}}>
          <rect x={0} y={1180} width={1000} height={660} fill={K} />
          {[...Array(9)].map((_, i) => { const x = 40 + i * 106; const behind = passed && x + 96 < gx; const t = behind ? Math.max(0, walkL - slam - (4 - i) * 3) : 0;
            return <g key={i} transform={`translate(${x} ${1110 + 0.9 * t * t}) rotate(${t * 5 * (i % 2 ? 1 : -1)} 48 35)`}><rect width={96} height={70} fill={CY} stroke={K} strokeWidth={6} /><line x1={10} y1={20} x2={60} y2={20} stroke={WH} strokeWidth={5} /></g>; })}
          {/* the door */}
          <rect x={gx} y={780} width={130} height={330} fill={MG} stroke={K} strokeWidth={8} />
          <rect x={gx + 12} y={792} width={106} height={306} fill={K} opacity={0.85} />
          <g transform={`translate(${gx} 780) scale(${passed ? interpolate(walkL, [slam, slam + 6], [0.1, 1], clamp) : 0.1} 1)`}><rect width={130} height={330} fill={CY} stroke={K} strokeWidth={8} /><circle cx={104} cy={170} r={10} fill={YL} stroke={K} strokeWidth={4} /></g>
          <Guy x={guyX} y={920} s={0.85} walk={walkL > 10 && walkL < 120 ? walkL * 0.3 : 0} face={passed && walkL > slam + 14 ? 'shock' : 'ok'} f={f} flip={passed && walkL > slam + 14} />
        </svg>
      </Panel>
      {passed && <Burst text="ԲԱՄ!" x={P2.x + gx + 70} y={760} f={f} at={STARTS[2] + Math.round(slam)} size={130} r={220} color={WH} />}
      <Caption x={P2.x + 40} y={110} f={f} at={SC.ponr + 6} w={900}>{TXT.p1}</Caption>
      <Caption x={P2.x + 40} y={310} f={f} at={SC.ponr + Math.round(slam) + 18} w={900} bg={WH}>{TXT.p2}</Caption>
      {/* 3 EXAMPLE */}
      <Panel {...PANELS[3]} bg={CY} dot={WH}>
        <svg width={1000} height={900} style={{position: 'absolute'}}><Guy x={760} y={720} s={0.8} f={f} face="ok" /></svg>
      </Panel>
      <Caption x={PANELS[3].x + 40} y={80} f={f} at={SC.ex + 2} bg={WH}>Օրինակ · առաջին 3 վայրկյանը</Caption>
      <Balloon x={PANELS[3].x + 60} y={230} f={f} at={SC.ex + 16} tail="right">{TXT.ex1}</Balloon>
      <Balloon x={PANELS[3].x + 60} y={520} f={f} at={SC.ex + 56} tail="right">{TXT.ex2}</Balloon>
      {/* 4 RULE */}
      <Panel {...PANELS[4]} bg={MG} dot={K}>
        <div style={{position: 'absolute', left: 60, right: 60, top: 220, transform: `scale(${pop(f, SC.rule + 6)}) rotate(-2deg)`, background: WH, border: `8px solid ${K}`, boxShadow: `12px 12px 0 ${K}`, padding: '30px 36px'}}>
          <span style={{fontFamily: SANS, fontWeight: 900, fontSize: 70, color: K, lineHeight: 1.1}}>{TXT.rule}</span></div>
      </Panel>
      <Caption x={PANELS[4].x + 40} y={1020} f={f} at={SC.rule + 2}>Կանոն</Caption>
      {/* 5 CTA */}
      <Panel {...PANELS[5]} bg={YL} dot={CY}>
        <svg width={1000} height={1840} style={{position: 'absolute'}}>{[...Array(36)].map((_, i) => { const a = (i / 36) * Math.PI * 2; return <line key={i} x1={500 + Math.cos(a) * 340} y1={920 + Math.sin(a) * 340} x2={500 + Math.cos(a) * 1200} y2={920 + Math.sin(a) * 1200} stroke={K} strokeWidth={6} />; })}</svg>
        <div style={{position: 'absolute', left: 60, right: 60, top: 1400, textAlign: 'center', transform: `scale(${pop(f, SC.cta + 30)})`}}><span style={{fontFamily: SANS, fontWeight: 900, fontSize: 64, color: K}}>↓ {TXT.cta3}</span></div>
      </Panel>
      <Caption x={PANELS[5].x + 60} y={160} f={f} at={SC.cta + 4} w={880} bg={WH} size={40}>{TXT.cta1}<br />մեկնաբանություններում</Caption>
      {f >= SC.cta + 12 && <Burst text="ԿՈԴ!" x={PANELS[5].x + 500} y={960} f={f} at={SC.cta + 12} size={240} r={380} color={MG} />}
    </div>
  );
};

export const AWolffStyle: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  let cur = 0; for (let i = 0; i < STARTS.length; i++) if (f >= STARTS[i]) cur = i;
  const tgt = (i: number) => { const p = PANELS[i]; const s = Math.min(1080 / (p.w + 80), 1920 / (p.h + 80)); return {x: p.x + p.w / 2, y: p.y + p.h / 2, s}; };
  const a = tgt(Math.max(0, cur - 1)), b = tgt(cur);
  const t = cur === 0 ? 1 : pr(f, STARTS[cur] - 4, STARTS[cur] + 10);
  const cx = a.x + (b.x - a.x) * t, cy = a.y + (b.y - a.y) * t;
  let s = a.s + (b.s - a.s) * t; s *= 1 - Math.sin(t * Math.PI) * 0.25; s *= 1 + (f - STARTS[cur]) * 0.0008;
  const shake = (f >= 22 && f < 30) ? boil(f * 3, 'sh', 30) : 0;
  return (
    <AbsoluteFill style={{background: PAPER, overflow: 'hidden'}}>
      <Audio src={staticFile('dr/st_awolff.wav')} />
      <div style={{position: 'absolute', left: 0, top: 0, transformOrigin: '0 0', transform: `translate(${540 + shake}px, ${960}px) scale(${s}) translate(${-cx}px, ${-cy}px)`}}><Page f={f} /></div>
      <div style={{position: 'absolute', right: 150, top: 150, fontFamily: SANS, fontWeight: 900, fontSize: 28, color: K, background: YL, border: `4px solid ${K}`, padding: '4px 14px'}}>01 / 12</div>
    </AbsoluteFill>
  );
};
