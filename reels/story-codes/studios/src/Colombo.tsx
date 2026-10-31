import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame, interpolate, random, Easing} from 'remotion';
import {useGreekFonts} from '../Greece';
import {SC, TXT, ST_TOTAL} from './common';

// flat 2D character animation: simple shapes, bold colour, bouncy follow-through, unexpected shape transitions
const YEL = '#FFD23F', BLU = '#3D5AFE', COR = '#FF5470', INK = '#1B1B3A', MINT = '#2EC4B6', CRM = '#FFF4E0', PUR = '#7B4DFF';
const SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = io) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});
const pop = (f: number, a: number, d = 14) => interpolate(f, [a, a + d], [0, 1], {...clamp, easing: Easing.out(Easing.back(2.2))});
const elastic = (f: number, a: number) => { const t = Math.max(0, f - a) / 30; return f < a ? 0 : 1 - Math.exp(-5 * t) * Math.cos(14 * t); };

const T: React.FC<{children: React.ReactNode; size: number; color?: string; w?: number; style?: React.CSSProperties}> = ({children, size, color = INK, w = 900, style}) =>
  <span style={{fontFamily: SANS, fontWeight: w, fontStretch: '80%', fontSize: size, color, lineHeight: 1.02, letterSpacing: -size * 0.02, ...style}}>{children}</span>;
const PopText: React.FC<{f: number; at: number; children: React.ReactNode; x?: number; y: number; center?: boolean; rot?: number}> = ({f, at, children, x = 90, y, center, rot = 0}) => {
  const p = pop(f, at);
  return <div style={{position: 'absolute', left: center ? 0 : x, right: center ? 0 : 140, top: y, textAlign: center ? 'center' : 'left', transform: `scale(${p}) rotate(${(1 - p) * rot}deg)`, transformOrigin: center ? '50% 50%' : '0% 50%', opacity: p > 0.01 ? 1 : 0}}>{children}</div>;
};

// the blogger character, built from shapes
const Hero: React.FC<{x: number; y: number; s?: number; walk?: number; look?: number; shock?: boolean; phone?: boolean; f: number}> = ({x, y, s = 1, walk = 0, look = 1, shock, phone, f}) => {
  const bob = Math.abs(Math.sin(walk)) * 10;
  const leg = Math.sin(walk) * 26;
  const arm = Math.sin(walk) * 30;
  const blink = (f % 90) < 4;
  return (
    <g transform={`translate(${x} ${y - bob}) scale(${s * look} ${s})`}>
      {/* legs */}
      <line x1={-24} y1={90} x2={-24 + Math.sin((leg * Math.PI) / 180) * 70} y2={90 + Math.cos((leg * Math.PI) / 180) * 70} stroke={INK} strokeWidth={22} strokeLinecap="round" />
      <line x1={24} y1={90} x2={24 - Math.sin((leg * Math.PI) / 180) * 70} y2={90 + Math.cos((leg * Math.PI) / 180) * 70} stroke={INK} strokeWidth={22} strokeLinecap="round" />
      {/* body */}
      <rect x={-62} y={-60} width={124} height={170} rx={56} fill={COR} />
      {/* arms */}
      {phone ? <>
        <path d="M -50 -10 Q -10 40 20 10" stroke={INK} strokeWidth={18} fill="none" strokeLinecap="round" />
        <rect x={10} y={-34} width={44} height={74} rx={10} fill={INK} transform="rotate(-12 32 3)" /><rect x={16} y={-28} width={32} height={58} rx={6} fill={MINT} transform="rotate(-12 32 3)" />
      </> : <>
        <line x1={-56} y1={-10} x2={-56 - Math.sin((arm * Math.PI) / 180) * 60} y2={-10 + Math.cos((arm * Math.PI) / 180) * 60} stroke={INK} strokeWidth={18} strokeLinecap="round" />
        <line x1={56} y1={-10} x2={56 + Math.sin((arm * Math.PI) / 180) * 60} y2={-10 + Math.cos((arm * Math.PI) / 180) * 60} stroke={INK} strokeWidth={18} strokeLinecap="round" />
      </>}
      {/* head */}
      <circle cx={0} cy={-120} r={66} fill={CRM} />
      <path d="M -66 -124 A 66 66 0 0 1 66 -124 Q 30 -150 -10 -140 Q -40 -134 -66 -124 Z" fill={INK} />
      <circle cx={58} cy={-150} r={22} fill={INK} />
      {/* face (looks to its right) */}
      {blink && !shock ? <><line x1={2} y1={-112} x2={22} y2={-112} stroke={INK} strokeWidth={6} /><line x1={36} y1={-112} x2={56} y2={-112} stroke={INK} strokeWidth={6} /></>
        : <><circle cx={14} cy={-112} r={shock ? 12 : 8} fill={INK} /><circle cx={46} cy={-112} r={shock ? 12 : 8} fill={INK} /></>}
      {shock ? <ellipse cx={30} cy={-80} rx={10} ry={14} fill={INK} /> : <path d="M 14 -86 Q 30 -74 46 -86" stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />}
      <circle cx={-4} cy={-92} r={10} fill={COR} opacity={0.5} />
    </g>
  );
};

const Scene: React.FC<{f: number}> = ({f}) => {
  // ---------- 1 hook: endless feed, then STOP ----------
  if (f < SC.title) {
    const stop = 22;
    const scroll = f < stop ? f * 70 : stop * 70 + Math.sin((f - stop) * 0.9) * 40 * Math.exp(-(f - stop) / 6);
    const sq = f >= stop && f < stop + 12 ? 1 + Math.sin(((f - stop) / 12) * Math.PI) * 0.08 : 1;
    const zoom = pr(f, 48, 60, Easing.in(Easing.cubic));
    const cards = [COR, MINT, PUR, BLU, COR, MINT, PUR];
    return (
      <AbsoluteFill style={{background: YEL}}>
        <div style={{position: 'absolute', left: 290 - zoom * 290, top: 520 - zoom * 520, width: 500 + zoom * 580, height: 900 + zoom * 1020, borderRadius: 70 * (1 - zoom), background: INK, transform: `scale(${1 / sq}, ${sq})`, overflow: 'hidden'}}>
          <div style={{position: 'absolute', left: 24, right: 24, top: 24, bottom: 24, borderRadius: 50 * (1 - zoom), background: zoom > 0.6 ? BLU : CRM, overflow: 'hidden'}}>
            {zoom < 0.6 && cards.map((c, i) => <div key={i} style={{position: 'absolute', left: 30, right: 30, top: ((i * 300 - scroll) % 2100 + 2100) % 2100 - 300, height: 260, borderRadius: 30, background: c}}>
              <div style={{position: 'absolute', left: 30, top: 30, width: 80, height: 80, borderRadius: 40, background: CRM, opacity: 0.6}} /><div style={{position: 'absolute', left: 130, top: 44, width: 220, height: 20, borderRadius: 10, background: CRM, opacity: 0.6}} />
            </div>)}
          </div>
        </div>
        {/* the thumb */}
        {f < stop + 6 && <div style={{position: 'absolute', left: 560, top: 1150 - (f % 8) * 40, width: 120, height: 170, borderRadius: 60, background: CRM, border: `10px solid ${INK}`, opacity: zoom > 0 ? 0 : 1}} />}
        <PopText f={f} at={stop} y={240} center rot={-10}><T size={150} color={INK}>ՍՏՈՊ։</T></PopText>
        <PopText f={f} at={stop + 8} y={1500} center><T size={62} color={INK} w={800}>{TXT.hook}</T></PopText>
      </AbsoluteFill>
    );
  }
  // ---------- 2 title ----------
  if (f < SC.ponr) {
    const l = f - SC.title;
    const drop0 = elastic(f, SC.title + 4), drop1 = elastic(f, SC.title + 10);
    const out = pr(f, SC.ponr - 10, SC.ponr, Easing.in(Easing.cubic));
    return (
      <AbsoluteFill style={{background: BLU}}>
        <svg width={1080} height={1920} style={{position: 'absolute'}}>
          <circle cx={430 + out * 400} cy={760 - (1 - drop0) * 900} r={150 * (1 - out * 0.6)} fill="none" stroke={YEL} strokeWidth={70} />
          <rect x={640} y={610 - (1 - drop1) * 900} width={80} height={300} rx={40} fill={COR} opacity={1 - out} />
          {[...Array(10)].map((_, i) => { const a = (i / 10) * Math.PI * 2 + l * 0.05; const r = 300 + Math.sin(l / 6 + i) * 20; return <circle key={i} cx={540 + Math.cos(a) * r} cy={760 + Math.sin(a) * r} r={10 + (i % 3) * 6} fill={[YEL, MINT, COR][i % 3]} opacity={pop(f, SC.title + 14 + i)} />; })}
        </svg>
        <PopText f={f} at={SC.title + 16} y={1180} center><T size={44} color={CRM} w={700} style={{letterSpacing: 6}}>{TXT.kicker.toUpperCase()}</T></PopText>
        <PopText f={f} at={SC.title + 22} y={1250} center rot={6}><T size={128} color="#fff">{TXT.title}</T></PopText>
      </AbsoluteFill>
    );
  }
  // ---------- 3 point of no return ----------
  if (f < SC.ex) {
    const l = f - SC.ponr;
    const walkX = interpolate(l, [10, 150], [140, 840], clamp);
    const walking = l > 10 && l < 150;
    const gateX = 520;
    const passedAt = SC.ponr + 10 + ((gateX + 40 - 140) / 700) * 140;
    const shock = f > passedAt + 28 && f < passedAt + 120;
    const look = shock ? -1 : 1;
    const tiles = [...Array(10)].map((_, i) => 60 + i * 100);
    return (
      <AbsoluteFill style={{background: CRM}}>
        <svg width={1080} height={1920} style={{position: 'absolute'}}>
          {/* abyss */}
          <rect x={0} y={1210} width={1080} height={710} fill={INK} />
          {tiles.map((x, i) => {
            const behind = x + 90 < gateX && f > passedAt + 6;
            const t = behind ? Math.max(0, f - (passedAt + 6 + (4 - i) * 4)) : 0;
            return <rect key={i} x={x} y={1150 + 0.5 * 1.6 * t * t} width={92} height={60} rx={14} fill={i % 2 ? MINT : YEL} transform={`rotate(${t * 4 * (i % 2 ? 1 : -1)} ${x + 46} ${1180 + 0.8 * t * t})`} />;
          })}
          {/* the gate */}
          <path d={`M ${gateX - 10} 1150 L ${gateX - 10} 900 Q ${gateX + 50} 830 ${gateX + 110} 900 L ${gateX + 110} 1150`} stroke={COR} strokeWidth={26} fill="none" strokeLinecap="round" transform={`scale(1 ${pop(f, SC.ponr + 2)})`} style={{transformOrigin: `${gateX}px 1150px`}} />
          <Hero x={walkX} y={1000} s={0.8} walk={walking ? l * 0.35 : 0} look={look} shock={shock} f={f} />
          {shock && <g transform={`translate(${walkX - 10} ${780}) scale(${pop(f, passedAt + 28)})`}><circle r={44} fill={COR} /><rect x={-7} y={-28} width={14} height={34} rx={7} fill="#fff" /><circle cy={20} r={8} fill="#fff" /></g>}
        </svg>
        <PopText f={f} at={SC.ponr + 8} y={240}><T size={86}>{TXT.p1}</T></PopText>
        <PopText f={f} at={Math.round(passedAt + 20)} y={440}><T size={86} color={COR}>{TXT.p2}</T></PopText>
      </AbsoluteFill>
    );
  }
  // ---------- 4 example: chat bubbles out of the phone ----------
  if (f < SC.rule) {
    const b = (at: number, text: string, y: number, c: string, tc: string, right: boolean) => { const p = pop(f, at, 12);
      return <div style={{position: 'absolute', [right ? 'right' : 'left']: right ? 150 : 90, top: y, maxWidth: 760, padding: '28px 38px', borderRadius: 44, background: c, transform: `scale(${p})`, transformOrigin: right ? '100% 100%' : '0% 100%'}}><T size={50} color={tc} w={700}>{text}</T></div>; };
    return (
      <AbsoluteFill style={{background: MINT}}>
        <svg width={1080} height={1920} style={{position: 'absolute'}}><Hero x={300} y={1320} s={1.1} phone f={f} walk={0} /></svg>
        <PopText f={f} at={SC.ex + 2} y={230}><T size={40} color={INK} w={800} style={{letterSpacing: 4}}>ՕՐԻՆԱԿ · ԱՌԱՋԻՆ 3 ՎԱՅՐԿՅԱՆԸ</T></PopText>
        {b(SC.ex + 16, TXT.ex1, 420, '#fff', INK, true)}
        {b(SC.ex + 56, TXT.ex2, 600, COR, '#fff', true)}
        {b(SC.ex + 96, '😳 լավ, պատմիր', 780, INK, '#fff', false)}
      </AbsoluteFill>
    );
  }
  // ---------- 5 rule ----------
  if (f < SC.cta) {
    const l = f - SC.rule;
    return (
      <AbsoluteFill style={{background: PUR}}>
        <svg width={1080} height={1920} style={{position: 'absolute'}}>
          <circle cx={200 + Math.sin(l / 8) * 30} cy={1350} r={90 * pop(f, SC.rule + 4)} fill={YEL} />
          <rect x={720} y={1250 + Math.sin(l / 7) * 30} width={170} height={170} rx={30} fill={COR} transform={`rotate(${l * 3} 805 1335)`} opacity={pop(f, SC.rule + 8)} />
          <path d={`M 520 ${1500 + Math.cos(l / 9) * 20} l 90 160 l -180 0 Z`} fill={MINT} opacity={pop(f, SC.rule + 12)} />
        </svg>
        <PopText f={f} at={SC.rule + 2} y={230}><T size={44} color={YEL} w={800} style={{letterSpacing: 6}}>ԿԱՆՈՆ</T></PopText>
        <PopText f={f} at={SC.rule + 8} y={420}><T size={96} color="#fff">{TXT.rule}</T></PopText>
      </AbsoluteFill>
    );
  }
  // ---------- 6 CTA ----------
  const l = f - SC.cta;
  const press = l > 30 && l < 38 ? 0.88 : 1;
  return (
    <AbsoluteFill style={{background: YEL}}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {l > 34 && [...Array(26)].map((_, i) => { const a = random(`a${i}`) * Math.PI * 2, v = 10 + random(`v${i}`) * 18, t = l - 34; return <rect key={i} x={540 + Math.cos(a) * v * t} y={1000 + Math.sin(a) * v * t + 0.6 * t * t} width={22} height={22} rx={i % 2 ? 11 : 4} fill={[COR, BLU, MINT, PUR][i % 4]} transform={`rotate(${t * 12} ${540 + Math.cos(a) * v * t} ${1000 + Math.sin(a) * v * t})`} />; })}
        <circle cx={740 - pr(f, SC.cta + 18, SC.cta + 30) * 140} cy={1240 - pr(f, SC.cta + 18, SC.cta + 30) * 140} r={60} fill={CRM} stroke={INK} strokeWidth={10} />
      </svg>
      <PopText f={f} at={SC.cta + 2} y={300} center><T size={80}>{TXT.cta1} մեկնաբանություններում</T></PopText>
      <div style={{position: 'absolute', left: 240, top: 880, width: 600, height: 240, borderRadius: 120, background: COR, transform: `scale(${pop(f, SC.cta + 8) * press})`, boxShadow: `0 ${press < 1 ? 6 : 22}px 0 ${INK}`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><T size={140} color="#fff">{TXT.cta2}</T></div>
      <PopText f={f} at={SC.cta + 40} y={1420} center><T size={54} w={800}>{TXT.cta3}</T></PopText>
    </AbsoluteFill>
  );
};

export const ColomboStyle: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Audio src={staticFile('dr/st_colombo.wav')} />
      <Scene f={f} />
      <div style={{position: 'absolute', left: 90, top: 150, fontFamily: SANS, fontWeight: 800, fontSize: 26, color: INK, opacity: 0.5, letterSpacing: 4}}>01 / 12</div>
    </AbsoluteFill>
  );
};
