import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, interpolate, random, Easing} from 'remotion';
import {useGreekFonts} from '../Greece';
import {SC, TXT} from './common';

// HIGH CONTRAST · ULTRA TEXTURED · MOODY · OPTICAL — frame-by-frame on twos, collage, op-art
const BLK = '#0A0A0A', PAP = '#E9E4D8', ACID = '#FF2A1A';
const SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const pr = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], clamp);
const jit = (f: number, k: string, a = 6) => (random(`${k}${Math.floor(f / 2)}`) - 0.5) * a;

const Big: React.FC<{children: React.ReactNode; size: number; color?: string; f: number; k: string; style?: React.CSSProperties}> = ({children, size, color = PAP, f, k, style}) =>
  <span style={{display: 'inline-block', fontFamily: SANS, fontWeight: 900, fontStretch: '62.5%', fontSize: size, lineHeight: 0.86, color, letterSpacing: -size * 0.03, textTransform: 'uppercase', transform: `translate(${jit(f, k + 'x')}px, ${jit(f, k + 'y')}px) rotate(${jit(f, k + 'r', 1.4)}deg)`, ...style}}>{children}</span>;

// textures
const Grain: React.FC<{f: number; o?: number}> = ({f, o = 0.35}) => (
  <AbsoluteFill style={{opacity: o, mixBlendMode: 'overlay', backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='360' height='360'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.95' numOctaves='2' seed='${Math.floor(f / 2) % 11}'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 2 -0.6'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`}} />
);
const Photocopy: React.FC<{f: number}> = ({f}) => (
  <AbsoluteFill style={{mixBlendMode: 'multiply', opacity: 0.28, backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1920'><filter id='p'><feTurbulence type='fractalNoise' baseFrequency='0.004 0.06' numOctaves='3' seed='${Math.floor(f / 2) % 7}'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -6 3.2'/></filter><rect width='100%' height='100%' filter='url(%23p)'/></svg>")`}} />
);
const Scan: React.FC = () => <AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.22) 0 2px, transparent 2px 5px)', mixBlendMode: 'multiply'}} />;
const Bust: React.FC<{src: string; x: number; y: number; w: number; f: number; k: string; flip?: boolean}> = ({src, x, y, w, f, k, flip}) =>
  <Img src={staticFile(`dr/img/${src}.png`)} style={{position: 'absolute', left: x + jit(f, k, 8), top: y + jit(f, k + 'y', 8), width: w, transform: `scaleX(${flip ? -1 : 1})`, filter: 'grayscale(1) contrast(3.2) brightness(1.1)'}} />;

// op-art: concentric rings / tunnel
const Rings: React.FC<{f: number; color?: string; speed?: number; cx?: number; cy?: number}> = ({f, color = PAP, speed = 6, cx = 540, cy = 960}) => {
  const ph = (Math.floor(f / 2) * speed) % 80;
  return <svg width={1080} height={1920} style={{position: 'absolute'}}>{[...Array(30)].map((_, i) => <circle key={i} cx={cx} cy={cy} r={i * 80 + ph} fill="none" stroke={color} strokeWidth={38} />)}</svg>;
};
const Tunnel: React.FC<{f: number; collapse: number; flashRed?: boolean}> = ({f, collapse, flashRed}) => {
  const ph = (Math.floor(f / 2) * 0.06) % 1;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute'}}>
      {[...Array(16)].map((_, i) => {
        const z = (i + ph) / 16; const s = Math.pow(z, 2.2);
        const w = 60 + s * 1500, h = 110 + s * 2700;
        const behind = s > 0.55 && collapse > 0;
        const drop = behind ? collapse * (s - 0.55) * 3000 : 0;
        return <rect key={i} x={540 - w / 2 + (behind ? jit(f, `t${i}`, 60) * collapse : 0)} y={980 - h / 2 + drop} width={w} height={h} fill="none" stroke={i % 5 === 0 && flashRed ? ACID : PAP} strokeWidth={8 + s * 40} opacity={behind ? 1 - collapse : 1} />;
      })}
    </svg>
  );
};
const TornStrip: React.FC<{children: React.ReactNode; x: number; y: number; rot?: number; bg?: string; f: number; k: string; show: boolean}> = ({children, x, y, rot = -2, bg = PAP, f, k, show}) => !show ? null : (
  <div style={{position: 'absolute', left: x + jit(f, k, 5), top: y + jit(f, k + 'y', 5), transform: `rotate(${rot + jit(f, k + 'r', 1)}deg)`, background: bg, padding: '18px 30px', clipPath: 'polygon(0 6%, 4% 0, 30% 5%, 60% 0, 96% 4%, 100% 40%, 98% 100%, 70% 95%, 40% 100%, 3% 96%)', filter: 'contrast(1.2)'}}>{children}</div>
);

const Scene: React.FC<{f: number}> = ({f}) => {
  const strobe = (a: number, n = 3) => f >= a && f < a + n * 4 && Math.floor((f - a) / 2) % 2 === 0;
  // 1 HOOK
  if (f < SC.title) return (
    <AbsoluteFill style={{background: strobe(14) ? PAP : BLK}}>
      <Rings f={f} color={strobe(14) ? BLK : PAP} speed={f < 14 ? 14 : 2} />
      {f >= 14 && <Bust src="bust_front" x={190} y={520} w={700} f={f} k="b1" />}
      {f >= 16 && <div style={{position: 'absolute', left: 60, top: 220}}><Big f={f} k="h" size={340} color={ACID}>ՍՏՈՊ</Big></div>}
      {f >= 26 && <TornStrip f={f} k="hs" x={80} y={1480} show><Big f={f} k="hs2" size={64} color={BLK}>{TXT.hook}</Big></TornStrip>}
    </AbsoluteFill>
  );
  // 2 TITLE
  if (f < SC.ponr) {
    const l = f - SC.title;
    return (
      <AbsoluteFill style={{background: BLK}}>
        <svg width={1080} height={1920} style={{position: 'absolute'}}>
          <filter id="boil"><feTurbulence baseFrequency="0.03" numOctaves="2" seed={Math.floor(f / 2) % 9} /><feDisplacementMap in="SourceGraphic" scale="10" /></filter>
          <text x={540} y={1000} textAnchor="middle" fontFamily="ArmSans" fontWeight={900} fontSize={760} fill="none" stroke={PAP} strokeWidth={10} filter="url(#boil)" style={{fontStretch: '62.5%'}}>01</text>
        </svg>
        <TornStrip f={f} k="k" x={80} y={330} rot={-3} bg={ACID} show={l > 6}><Big f={f} k="k2" size={52} color={BLK}>{TXT.kicker}</Big></TornStrip>
        <div style={{position: 'absolute', left: 80, right: 140, top: 1200}}>{l > 12 && <Big f={f} k="t1" size={150}>Անվերադարձ</Big>}<br />{l > 18 && <Big f={f} k="t2" size={190} color={ACID}>կետ</Big>}</div>
      </AbsoluteFill>
    );
  }
  // 3 POINT OF NO RETURN — the tunnel, then everything behind collapses
  if (f < SC.ex) {
    const l = f - SC.ponr;
    const breakAt = 110;
    const collapse = pr(l, breakAt, breakAt + 50);
    const fig = interpolate(l, [0, breakAt], [1.3, 0.35], clamp);
    return (
      <AbsoluteFill style={{background: strobe(SC.ponr + breakAt, 3) ? ACID : BLK}}>
        <Tunnel f={f} collapse={collapse} flashRed={l > breakAt} />
        <div style={{position: 'absolute', left: 540 - 200 * fig, top: 980 - 330 * fig, width: 400 * fig}}><Bust src="bust_profile" x={0} y={0} w={400 * fig} f={f} k="fig" /></div>
        <div style={{position: 'absolute', left: 50, right: 120, top: 190, background: BLK, padding: '14px 20px'}}><Big f={f} k="p1" size={110}>{TXT.p1}</Big></div>
        {l > 40 && <div style={{position: 'absolute', left: 50, right: 120, top: 1400, background: BLK, padding: '14px 20px'}}><Big f={f} k="p2" size={110} color={l > breakAt ? ACID : PAP}>{TXT.p2}</Big></div>}
      </AbsoluteFill>
    );
  }
  // 4 EXAMPLE — photocopied notes, stop-motion
  if (f < SC.rule) {
    const l = f - SC.ex;
    return (
      <AbsoluteFill style={{background: PAP}}>
        <Bust src="bust_34" x={420} y={760} w={700} f={f} k="e" />
        <TornStrip f={f} k="lab" x={70} y={220} rot={-1} bg={BLK} show><Big f={f} k="lab2" size={44} color={PAP}>ՕՐԻՆԱԿ · ԱՌԱՋԻՆ 3 ՎԱՅՐԿՅԱՆԸ</Big></TornStrip>
        <TornStrip f={f} k="n1" x={70} y={420} rot={2} bg="#fff" show={l > 14}><Big f={f} k="n1t" size={86} color={BLK}>«{TXT.ex1}»</Big></TornStrip>
        <TornStrip f={f} k="n2" x={90} y={720} rot={-3} bg={ACID} show={l > 54}><Big f={f} k="n2t" size={86} color={BLK}>«{TXT.ex2}»</Big></TornStrip>
      </AbsoluteFill>
    );
  }
  // 5 RULE — op-art stripes warping behind stacked type
  if (f < SC.cta) {
    const l = f - SC.rule;
    return (
      <AbsoluteFill style={{background: BLK}}>
        <svg width={1080} height={1920} style={{position: 'absolute'}}>
          {[...Array(40)].map((_, i) => { const y = i * 50; let d = `M 0 ${y}`; for (let x = 0; x <= 1080; x += 40) d += ` L ${x} ${y + Math.sin(x / 120 + Math.floor(f / 2) * 0.5 + i * 0.3) * 30}`; return <path key={i} d={d} stroke={PAP} strokeWidth={14} fill="none" opacity={0.55} />; })}
        </svg>
        <TornStrip f={f} k="r" x={70} y={220} rot={-2} bg={ACID} show><Big f={f} k="r2" size={48} color={BLK}>ԿԱՆՈՆ</Big></TornStrip>
        <div style={{position: 'absolute', left: 70, right: 140, top: 520, background: BLK, padding: 20}}>{l > 6 && <Big f={f} k="rt" size={120}>{TXT.rule}</Big>}</div>
      </AbsoluteFill>
    );
  }
  // 6 CTA
  const l = f - SC.cta;
  return (
    <AbsoluteFill style={{background: strobe(SC.cta + 10, 2) ? ACID : BLK}}>
      <Rings f={f} color="#1d1d1d" speed={3} cy={1050} />
      <div style={{position: 'absolute', left: 70, right: 140, top: 260}}><Big f={f} k="c1" size={78}>{TXT.cta1} մեկնաբանություններում</Big></div>
      {l > 10 && <div style={{position: 'absolute', left: 0, right: 0, top: 820, textAlign: 'center'}}><Big f={f} k="c2" size={420} color={ACID}>ԿՈԴ</Big></div>}
      {l > 24 && <TornStrip f={f} k="c3" x={110} y={1460} rot={-2} show><Big f={f} k="c3t" size={60} color={BLK}>{TXT.cta3}</Big></TornStrip>}
    </AbsoluteFill>
  );
};

export const OcularStyle: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: BLK}}>
      <Audio src={staticFile('dr/st_ocular.wav')} />
      <Scene f={f} />
      <Photocopy f={f} />
      <Grain f={f} />
      <Scan />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.7) 100%)'}} />
      <div style={{position: 'absolute', left: 80, top: 150, fontFamily: SANS, fontWeight: 900, fontStretch: '62.5%', fontSize: 30, color: ACID, letterSpacing: 4}}>01/12</div>
    </AbsoluteFill>
  );
};
