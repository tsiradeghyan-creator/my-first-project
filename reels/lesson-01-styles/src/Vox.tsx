import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, interpolate, random, Easing} from 'remotion';
import {G, G_TOTAL, VO, Amphitheatre, Column, Vase, Mask, Meander, Temple, useGreekFonts} from './Greece';
import {Defs, Scribble, Arrow, Stroke} from './Drama';

const PAPER = '#EFE6D4', KRAFT = '#C9A87C', INK = '#141110', RED = '#D90429', TEAL = '#1F5C63', CREAMW = '#FBF7EE';
const ARM = 'ArmSerif, DejaVu Serif', SANS = 'ArmSans, DejaVu Sans', GR = 'GrSerif, DejaVu Serif', CINZEL = 'Cinzel, serif';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = Easing.bezier(0.16, 1, 0.3, 1)) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});

// ---------- board: 3 columns x 4 rows of 1200x2100 cells, zig-zag ----------
const CW = 1200, CH = 2100;
const STARTS = [G.hook, G.etym, G.contest, G.masks, G.poet, G.temple, G.peri, G.cath, G.today, G.arch];
const CELL = [[0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [0, 1], [0, 2], [1, 2], [2, 2], [1, 3]];
const origin = (i: number) => ({x: CELL[i][0] * CW + 60, y: CELL[i][1] * CH + 90});
const BOARD_W = 3 * CW, BOARD_H = 4 * CH;

// ---------- collage primitives ----------
const torn = (seed: string, w: number, h: number, amp = 10) => {
  const pts: string[] = [];
  const step = 22;
  for (let x = 0; x <= w; x += step) pts.push(`${x}px ${random(`${seed}t${x}`) * amp}px`);
  for (let y = 0; y <= h; y += step) pts.push(`${w - random(`${seed}r${y}`) * amp}px ${y}px`);
  for (let x = w; x >= 0; x -= step) pts.push(`${x}px ${h - random(`${seed}b${x}`) * amp}px`);
  for (let y = h; y >= 0; y -= step) pts.push(`${random(`${seed}l${y}`) * amp}px ${y}px`);
  return `polygon(${pts.join(',')})`;
};
// "slap on" entrance: big + rotated -> settles with a little bounce
const useSlap = (lf: number, d: number) => {
  const p = interpolate(lf - d, [0, 8, 12], [0, 1.04, 1], clamp);
  return {p, style: {opacity: lf >= d ? 1 : 0, transform: `scale(${lf >= d ? (lf - d < 8 ? interpolate(lf - d, [0, 8], [1.35, 1.03]) : interpolate(lf - d, [8, 12], [1.03, 1], clamp)) : 1.35})`}};
};
const Scrap: React.FC<{lf: number; d: number; x: number; y: number; w: number; h: number; rot?: number; bg?: string; seed: string; children?: React.ReactNode; shadow?: boolean; amp?: number}> = ({lf, d, x, y, w, h, rot = 0, bg = CREAMW, seed, children, shadow = true, amp}) => {
  const s = useSlap(lf, d);
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, transform: `rotate(${rot}deg)`, filter: shadow ? 'drop-shadow(0 10px 14px rgba(40,25,10,0.35))' : undefined}}>
      <div style={{...s.style, width: w, height: h, transformOrigin: '50% 50%'}}>
        <div style={{position: 'absolute', inset: 0, background: bg, clipPath: torn(seed, w, h, amp), overflow: 'hidden'}}>{children}</div>
      </div>
    </div>
  );
};
const Tape: React.FC<{x: number; y: number; rot: number; w?: number; lf: number; d: number}> = ({x, y, rot, w = 150, lf, d}) =>
  <div style={{position: 'absolute', left: x, top: y, width: w, height: 46, background: 'rgba(236,224,190,0.78)', transform: `rotate(${rot}deg)`, opacity: lf >= d + 6 ? 1 : 0, boxShadow: '0 2px 4px rgba(0,0,0,0.12)', clipPath: torn(`tp${x}${y}`, w, 46, 5)}} />;
// halftone print overlay + duotone
const Print: React.FC<{tint?: string; children: React.ReactNode; dot?: number}> = ({tint = TEAL, children, dot = 7}) => (
  <div style={{position: 'absolute', inset: 0, overflow: 'hidden'}}>
    <div style={{position: 'absolute', inset: 0, filter: 'contrast(1.18) saturate(1.15)'}}>{children}</div>
    <div style={{position: 'absolute', inset: 0, background: tint, mixBlendMode: 'soft-light', opacity: 0.35}} />
    <div style={{position: 'absolute', inset: 0, mixBlendMode: 'multiply', opacity: 0.22, backgroundImage: `radial-gradient(circle, #000 ${dot * 0.28}px, transparent ${dot * 0.32}px)`, backgroundSize: `${dot}px ${dot}px`}} />
  </div>
);
// ransom-note letters
const Ransom: React.FC<{text: string; x: number; y: number; size: number; lf: number; d: number; seed: string}> = ({text, x, y, size, lf, d, seed}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', flexWrap: 'wrap', gap: 6}}>
    {[...text].map((ch, i) => {
      if (ch === ' ') return <span key={i} style={{width: size * 0.3}} />;
      const r = random(`${seed}${i}`);
      const bgs = [CREAMW, INK, RED, KRAFT, '#fff'], fgs = [INK, CREAMW, '#fff', INK, RED];
      const k = Math.floor(r * bgs.length);
      const fonts = [ARM, SANS, ARM, SANS];
      const on = lf >= d + i * 1.5;
      const sc = on ? interpolate(lf - d - i * 1.5, [0, 5], [1.6, 1], clamp) : 1.6;
      return <span key={i} style={{display: 'inline-block', padding: `${size * 0.05}px ${size * 0.12}px`, background: bgs[k], color: fgs[k], fontFamily: fonts[Math.floor(random(`${seed}f${i}`) * 4)], fontWeight: random(`${seed}w${i}`) > 0.4 ? 900 : 500, fontStretch: '75%', fontSize: size * (0.85 + random(`${seed}s${i}`) * 0.3), lineHeight: 1, transform: `rotate(${(random(`${seed}r${i}`) - 0.5) * 12}deg) scale(${sc})`, opacity: on ? 1 : 0, boxShadow: '0 3px 6px rgba(0,0,0,0.25)'}}>{ch}</span>;
    })}
  </div>
);
const Label: React.FC<{text: string; x: number; y: number; lf: number; d: number; rot?: number; size?: number; bg?: string}> = ({text, x, y, lf, d, rot = -2, size = 34, bg = INK}) => {
  const s = useSlap(lf, d);
  return <div style={{position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg)`}}><div style={{...s.style, padding: `${size * 0.25}px ${size * 0.5}px`, background: bg, color: '#fff', fontFamily: SANS, fontWeight: 800, fontSize: size, letterSpacing: size * 0.12, borderRadius: 6, boxShadow: 'inset 0 -3px 0 rgba(255,255,255,0.15), 0 4px 8px rgba(0,0,0,0.3)'}}>{text}</div></div>;
};
const Headline: React.FC<{lines: string[]; x: number; y: number; lf: number; d: number; size?: number; hi?: number}> = ({lines, x, y, lf, d, size = 92, hi = -1}) => (
  <div style={{position: 'absolute', left: x, top: y}}>
    {lines.map((l, i) => {
      const p = pr(lf, d + i * 6, d + i * 6 + 10);
      return <div key={i} style={{display: 'inline-block', marginBottom: 10, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`}}>
        <span style={{display: 'inline-block', background: i === hi ? RED : CREAMW, color: i === hi ? '#fff' : INK, fontFamily: SANS, fontWeight: 900, fontStretch: '70%', fontSize: size, lineHeight: 1.05, padding: '6px 18px', transform: `rotate(${i % 2 ? 1 : -1.2}deg)`, boxShadow: '0 6px 10px rgba(0,0,0,0.2)'}}>{l}</span><br />
      </div>;
    })}
  </div>
);
const Bust: React.FC<{src: string; x: number; y: number; w: number; lf: number; d: number; rot?: number; flip?: number}> = ({src, x, y, w, lf, d, rot = 0, flip = 0}) => {
  const s = useSlap(lf, d);
  return <div style={{position: 'absolute', left: x, top: y, width: w, transform: `rotate(${rot}deg)`}}>
    <div style={{...s.style}}>
      <Img src={staticFile(`dr/img/${src}.png`)} style={{width: w, transform: `rotate(${flip}deg)`, filter: 'drop-shadow(0 0 0 #fff) drop-shadow(8px 0 0 #fff) drop-shadow(-8px 0 0 #fff) drop-shadow(0 8px 0 #fff) drop-shadow(0 -8px 0 #fff) drop-shadow(0 14px 16px rgba(0,0,0,0.35)) contrast(1.1)'}} />
    </div>
  </div>;
};

// ---------- clusters (cell-local coordinates, lf = frames since the cluster started) ----------
const C1: React.FC<{lf: number}> = ({lf}) => (
  <>
    <Scrap lf={lf} d={0} x={20} y={500} w={1040} h={1080} rot={-2} seed="amp" bg="#222">
      <div style={{position: 'absolute', left: -20, top: -560, width: 1080, height: 1920, transform: 'scale(1.05)'}}><Print tint="#C8552B"><Amphitheatre f={Math.min(lf, 150)} /></Print></div>
    </Scrap>
    <Tape x={60} y={480} rot={-24} lf={lf} d={0} /><Tape x={880} y={1540} rot={-18} lf={lf} d={0} />
    <Ransom text="2500" x={60} y={140} size={170} lf={lf} d={6} seed="n" />
    <Headline lines={['տարի առաջ', 'Աթենք']} x={60} y={350} lf={lf} d={18} size={64} hi={1} />
    <Label text="17 000 ՀԱՆԴԻՍԱՏԵՍ" x={540} y={1280} lf={lf} d={60} rot={3} size={36} bg={RED} />
    <div style={{position: 'absolute', left: 0, top: 0}}><Scribble cx={540} cy={1320} rx={330} ry={150} p={pr(lf, 70, 96)} /></div>
  </>
);
const C2: React.FC<{lf: number}> = ({lf}) => (
  <>
    <Headline lines={['Այնտեղ ծնվեց', 'դրամատուրգիան']} x={40} y={120} lf={lf} d={4} size={84} hi={1} />
    <Bust src="bust_front" x={560} y={420} w={520} lf={lf} d={12} rot={4} />
    <Scrap lf={lf} d={30} x={40} y={560} w={480} h={200} rot={-4} seed="dr" bg={CREAMW}>
      <div style={{padding: '30px 40px', fontFamily: GR, fontWeight: 700, fontSize: 96, color: '#B5452A'}}>δρᾶμα</div>
    </Scrap>
    <Label text="ԳՈՐԾՈՂՈՒԹՅՈՒՆ" x={60} y={780} lf={lf} d={40} size={30} />
    <Scrap lf={lf} d={60} x={60} y={900} w={480} h={200} rot={3} seed="er" bg={CREAMW}>
      <div style={{padding: '30px 40px', fontFamily: GR, fontWeight: 700, fontSize: 96, color: '#B5452A'}}>ἔργον</div>
    </Scrap>
    <Label text="ԱՇԽԱՏԱՆՔ" x={80} y={1120} lf={lf} d={70} size={30} rot={2} />
    <Scrap lf={lf} d={130} x={60} y={1250} w={960} h={240} rot={-1.5} seed="def" bg={INK}>
      <div style={{padding: '34px 40px', fontFamily: ARM, fontWeight: 700, fontSize: 58, color: CREAMW, lineHeight: 1.2}}>գործողությունը<br /><span style={{color: RED}}>կառուցելու արվեստ</span></div>
    </Scrap>
    <div style={{position: 'absolute', left: 0, top: 0}}><Arrow x1={520} y1={1000} x2={620} y2={1260} p={pr(lf, 110, 128)} color={RED} bend={-60} /></div>
  </>
);
const C3: React.FC<{lf: number}> = ({lf}) => (
  <>
    <Scrap lf={lf} d={0} x={0} y={380} w={1080} h={1100} rot={1} seed="red" bg="#C8552B" amp={16}>
      <Meander x={0} y={30} w={1080} h={40} />
      <Meander x={0} y={1010} w={1080} h={40} />
    </Scrap>
    <Headline lines={['Թատրոնը մրցույթ էր', 'Դիոնիսոսի տոներին']} x={40} y={110} lf={lf} d={4} size={70} hi={0} />
    <Vase x={30} y={520} s={0.85} p={pr(lf, 30, 50)} name="" dates="" />
    <Vase x={380} y={480} s={0.85} p={pr(lf, 46, 66)} name="" dates="" />
    <Vase x={730} y={520} s={0.85} p={pr(lf, 62, 82)} name="" dates="" />
    <Label text="ԷՍՔԻԼԵՍ" x={60} y={1040} lf={lf} d={50} size={32} rot={-3} />
    <Label text="ՍՈՖՈԿԼԵՍ" x={400} y={1000} lf={lf} d={66} size={32} rot={2} />
    <Label text="ԵՎՐԻՊԻԴԵՍ" x={740} y={1040} lf={lf} d={82} size={32} rot={-2} />
    <div style={{position: 'absolute', left: 430, top: 1250, opacity: lf > 110 ? 1 : 0, transform: `rotate(-12deg) scale(${lf > 110 ? interpolate(lf - 110, [0, 6], [2, 1], clamp) : 2})`, border: `8px solid ${RED}`, color: RED, fontFamily: SANS, fontWeight: 900, fontSize: 70, padding: '6px 26px', letterSpacing: 6, background: 'rgba(255,255,255,0.75)'}}>VS</div>
  </>
);
const C4: React.FC<{lf: number}> = ({lf}) => (
  <>
    <Scrap lf={lf} d={0} x={40} y={420} w={1000} h={1050} rot={-1} seed="nt" bg="#1E1838">
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at 50% 50%, rgba(255,210,140,0.35), rgba(0,0,0,0) 65%)'}} />
    </Scrap>
    <Mask x={60} y={600} sad p={pr(lf, 8, 26)} rot={-14 + Math.sin(lf / 10) * 4} />
    <Mask x={600} y={560} p={pr(lf, 16, 34)} rot={12 - Math.sin(lf / 10) * 4} />
    <Headline lines={['Դերասանները', 'խաղում էին դիմակներով']} x={40} y={130} lf={lf} d={2} size={70} hi={1} />
    <Label text="ՈՂԲԵՐԳՈՒԹՅՈՒՆ" x={90} y={1200} lf={lf} d={40} size={28} rot={-3} bg={RED} />
    <Label text="ԿԱՏԱԿԵՐԳՈՒԹՅՈՒՆ" x={590} y={1160} lf={lf} d={50} size={28} rot={3} />
  </>
);
const C5: React.FC<{lf: number}> = ({lf}) => (
  <>
    <Ransom text="335" x={60} y={120} size={150} lf={lf} d={2} seed="335" />
    <Label text="Մ.Թ.Ա." x={420} y={170} lf={lf} d={14} size={40} bg={RED} />
    <Scrap lf={lf} d={20} x={60} y={420} w={700} h={980} rot={-3} seed="pap" bg="#EBD7A6" amp={18}>
      <div style={{padding: '70px 50px', textAlign: 'center'}}>
        <div style={{fontFamily: GR, fontWeight: 700, fontSize: 60, color: INK, letterSpacing: 3}}>ΠΕΡΙ ΠΟΙΗΤΙΚΗΣ</div>
        <div style={{width: 240, height: 4, background: '#B5452A', margin: '26px auto'}} />
        <div style={{fontFamily: ARM, fontWeight: 800, fontSize: 82, color: '#B5452A'}}>«Պոետիկա»</div>
        <div style={{fontFamily: ARM, fontWeight: 600, fontSize: 52, color: INK, marginTop: 30}}>Արիստոտել</div>
        {[...Array(9)].map((_, i) => <div key={i} style={{height: 7, margin: '22px 20px 0', background: 'rgba(60,40,20,0.18)', width: `${55 + random(`pl${i}`) * 40}%`}} />)}
      </div>
    </Scrap>
    <Tape x={300} y={400} rot={4} lf={lf} d={20} />
    <Bust src="bust_34" x={560} y={760} w={480} lf={lf} d={40} rot={-3} />
    <Label text="ԴՐԱՄԱՅԻ ԱՌԱՋԻՆ ՏԵՍՈՒԹՅՈՒՆԸ" x={80} y={1430} lf={lf} d={70} size={30} rot={-1} bg={RED} />
  </>
);
const C6: React.FC<{lf: number}> = ({lf}) => (
  <>
    <Headline lines={['սկիզբ · միջնամաս · վերջ']} x={40} y={150} lf={lf} d={2} size={66} hi={0} />
    <Scrap lf={lf} d={0} x={0} y={380} w={1080} h={1100} rot={1.5} seed="tmp" bg="#E9A86A">
      <div style={{position: 'absolute', left: 0, top: -420, width: 1080, height: 1920}}><Print tint="#E07A4F" dot={8}><div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, #F7C98B, #E07A4F)'}} /><Temple f={Math.min(lf + 10, 120)} labels={false} /></Print></div>
    </Scrap>
    <Label text="ՍԿԻԶԲ" x={150} y={1100} lf={lf} d={30} size={34} rot={-4} />
    <Label text="ՄԻՋՆԱՄԱՍ" x={390} y={1150} lf={lf} d={42} size={34} rot={3} />
    <Label text="ՎԵՐՋ" x={760} y={1100} lf={lf} d={54} size={34} rot={-2} bg={RED} />
  </>
);
const C7: React.FC<{lf: number}> = ({lf}) => {
  const flip = pr(lf, 70, 100, io) * 180;
  return (
    <>
      <Headline lines={['Սյուժեն', 'ողբերգության հոգին է']} x={40} y={120} lf={lf} d={2} size={74} hi={0} />
      <Scrap lf={lf} d={10} x={140} y={480} w={800} h={820} rot={-2} seed="per" bg={TEAL}><div style={{position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.15) 2px, transparent 2.4px)', backgroundSize: '12px 12px'}} /></Scrap>
      <Bust src="bust_up" x={260} y={560} w={560} lf={lf} d={20} flip={flip} />
      <div style={{position: 'absolute', left: 0, top: 0}}><Arrow x1={960} y1={700} x2={940} y2={1200} p={pr(lf, 60, 84)} color={RED} bend={140} /></div>
      <Ransom text="περιπέτεια" x={70} y={1360} size={78} lf={lf} d={96} seed="per" />
      <Label text="ՊԵՐԻՊԵՏԻԱ՝ ՇՐՋԱԴԱՐՁ" x={120} y={1500} lf={lf} d={110} size={34} bg={RED} rot={-2} />
    </>
  );
};
const C8: React.FC<{lf: number}> = ({lf}) => {
  const glow = pr(lf, 40, 90);
  return (
    <>
      <Scrap lf={lf} d={0} x={20} y={360} w={1040} h={1150} rot={-1} seed="cat" bg="#F4C35A">
        <div style={{position: 'absolute', inset: 0, background: `repeating-conic-gradient(from ${lf * 0.5}deg at 50% 55%, #F9E3A5 0deg 8deg, #F4C35A 8deg 16deg)`, opacity: 0.4 + glow * 0.6}} />
      </Scrap>
      <Bust src="bust_34r" x={280} y={600} w={520} lf={lf} d={14} />
      <Headline lines={['վախ + կարեկցանք']} x={40} y={130} lf={lf} d={2} size={70} />
      <Ransom text="կաթարսիս" x={80} y={250} size={110} lf={lf} d={40} seed="kat" />
      <Label text="ՄԱՔՐՈՒՄ" x={640} y={1300} lf={lf} d={70} size={40} bg={RED} rot={4} />
    </>
  );
};
const C9: React.FC<{lf: number}> = ({lf}) => (
  <>
    <Ransom text="2500" x={60} y={110} size={140} lf={lf} d={2} seed="25b" />
    <Headline lines={['տարի անց']} x={60} y={300} lf={lf} d={12} size={70} hi={0} />
    {[0, 1, 2].map((i) => (
      <Scrap key={i} lf={lf} d={26 + i * 12} x={40 + i * 340} y={520 + (i % 2) * 60} w={320} h={560} rot={[-4, 2, -1][i]} seed={`fs${i}`} bg="#111">
        {[...Array(8)].map((_, k) => <React.Fragment key={k}><div style={{position: 'absolute', left: 10, top: 14 + k * 68, width: 22, height: 34, background: CREAMW, borderRadius: 4}} /><div style={{position: 'absolute', right: 10, top: 14 + k * 68, width: 22, height: 34, background: CREAMW, borderRadius: 4}} /></React.Fragment>)}
        <div style={{position: 'absolute', left: 44, right: 44, top: 40, bottom: 40, overflow: 'hidden', background: ['#C8552B', '#1F5C63', '#E9A86A'][i]}}>
          <div style={{position: 'absolute', left: -380, top: -620, width: 1080, height: 1920, transform: 'scale(0.42)'}}><Temple f={200} labels={false} /></div>
        </div>
      </Scrap>
    ))}
    <Headline lines={['գրեթե ամեն ֆիլմ ու սերիա', 'նույն սկզբունքներով']} x={40} y={1180} lf={lf} d={70} size={58} hi={1} />
  </>
);
const C10: React.FC<{lf: number}> = ({lf}) => {
  const morph = pr(lf, 40, 70, io);
  return (
    <>
      <Headline lines={['Սյուները փոխվել են։', 'Կառույցը՝ ոչ։']} x={40} y={110} lf={lf} d={2} size={76} hi={1} />
      <Scrap lf={lf} d={0} x={20} y={420} w={1040} h={1100} rot={-0.5} seed="arc" bg="#2A1B3D" />
      {[0, 1, 2].map((i) => (
        <React.Fragment key={i}>
          <div style={{opacity: 1 - morph}}><Column x={170 + i * 290} y={760} h={540} w={130} p={1} /></div>
          <div style={{position: 'absolute', left: 185 + i * 290, top: 780, width: 130, height: 520, opacity: morph, background: i === 1 ? RED : '#111', border: '4px solid #F6D9A8', borderRadius: 8}}>
            {[...Array(8)].map((_, k) => <div key={k} style={{position: 'absolute', left: 10, top: 14 + k * 64, width: 22, height: 32, background: '#F6D9A8', borderRadius: 4}} />)}
          </div>
        </React.Fragment>
      ))}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d="M 100 740 L 520 570 L 940 740 Z" fill="#F6D9A8" /><rect x={100} y={740} width={840} height={28} fill="#F6D9A8" />
        <text x={520} y={705} textAnchor="middle" fontFamily="ArmSans" fontWeight={900} fontSize={48} fill={RED}>ԴՐԱՄԱՏՈՒՐԳԻԱ</text>
      </svg>
      <Label text="ՊԱՏՄՈՒԹՅԱՆ ՃԱՐՏԱՐԱՊԵՏՈՒԹՅՈՒՆԸ" x={60} y={1360} lf={lf} d={90} size={32} bg={RED} rot={-1.5} />
    </>
  );
};
const CLUSTERS = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10];

// paper board background with doodles
const Board: React.FC<{f: number; cur: number; all: boolean}> = ({f, cur, all}) => (
  <div style={{position: 'absolute', left: 0, top: 0, width: BOARD_W, height: BOARD_H, background: PAPER}}>
    <div style={{position: 'absolute', inset: 0, opacity: 0.5, backgroundImage: 'linear-gradient(rgba(120,90,60,0.08) 2px, transparent 2px), linear-gradient(90deg, rgba(120,90,60,0.08) 2px, transparent 2px)', backgroundSize: '120px 120px'}} />
    {/* red thread connecting the clusters, in story order */}
    <svg width={BOARD_W} height={BOARD_H} style={{position: 'absolute', left: 0, top: 0}}>
      <path d={CELL.map(([c, r], i) => `${i ? 'L' : 'M'} ${c * CW + 600} ${r * CH + 1100}`).join(' ')} stroke={RED} strokeWidth={6} fill="none" strokeDasharray="2 18" strokeLinecap="round" opacity={0.6} />
      {CELL.map(([c, r], i) => <circle key={i} cx={c * CW + 600} cy={r * CH + 1100} r={14} fill={RED} />)}
    </svg>
    {CLUSTERS.map((C, i) => {
      if (!all && Math.abs(i - cur) > 1) return null;
      const lf = all ? 400 : f - STARTS[i];
      const o = origin(i);
      return <div key={i} style={{position: 'absolute', left: o.x, top: o.y, width: 1080, height: 1920}}>
        {lf >= -20 && <C lf={Math.max(-1, lf)} />}
        <div style={{position: 'absolute', left: 20, top: 20, fontFamily: CINZEL, fontWeight: 700, fontSize: 40, color: 'rgba(20,17,16,0.35)'}}>{String(i + 1).padStart(2, '0')}</div>
      </div>;
    })}
  </div>
);

// caption as a typed paper strip
const Caption: React.FC = () => {
  const f = useCurrentFrame();
  let cur = VO[0];
  for (const v of VO) if (f >= v.at) cur = v;
  const next = VO[VO.indexOf(cur) + 1];
  const end = next ? next.at : G_TOTAL;
  const words = cur.t.split(' ');
  const span = (end - cur.at - 12) / words.length;
  const o = pr(f, cur.at + 4, cur.at + 10) * (1 - pr(f, end - 6, end));
  return (
    <div style={{position: 'absolute', left: 60, right: 150, top: 1500, opacity: o}}>
      <div style={{background: CREAMW, padding: '20px 26px', transform: 'rotate(-0.8deg)', boxShadow: '0 8px 16px rgba(0,0,0,0.25)', clipPath: torn('cap', 870, 400, 6), display: 'flex', flexWrap: 'wrap', gap: '2px 12px'}}>
        {words.map((w, i) => <span key={i} style={{fontFamily: SANS, fontWeight: 600, fontSize: 38, lineHeight: 1.3, color: f >= cur.at + i * span ? INK : 'rgba(20,17,16,0.3)', background: f >= cur.at + i * span && i === Math.floor((f - cur.at) / span) ? '#F4E06A' : 'transparent'}}>{w}</span>)}
      </div>
    </div>
  );
};

export const Vox: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  let cur = 0;
  for (let i = 0; i < STARTS.length; i++) if (f >= STARTS[i]) cur = i;
  // camera: travel 16 frames into each cluster, slight drift while there
  const tgt = (i: number) => ({x: origin(i).x + 540, y: origin(i).y + 960});
  const prev = tgt(Math.max(0, cur - 1)), now = tgt(cur);
  const t = cur === 0 ? 1 : pr(f, STARTS[cur] - 8, STARTS[cur] + 10, io);
  let cx = prev.x + (now.x - prev.x) * t, cy = prev.y + (now.y - prev.y) * t;
  let s = 1 - Math.sin(t * Math.PI) * 0.35;
  const drift = f - STARTS[cur];
  s *= 1 + drift * 0.0006; cy += drift * 0.15;
  // final reveal of the whole board
  const out = pr(f, G.logo - 10, G.logo + 30, io);
  const sAll = Math.min(1080 / BOARD_W, 1920 / BOARD_H);
  cx = cx + (BOARD_W / 2 - cx) * out; cy = cy + (BOARD_H / 2 - cy) * out; s = s + (sAll - s) * out;
  const rot = Math.sin(f / 60) * 0.6 * (1 - out);
  const logoP = pr(f, G.logo + 26, G.logo + 40);
  return (
    <AbsoluteFill style={{background: '#2b2219', overflow: 'hidden'}}>
      <Defs />
      <Audio src={staticFile('dr/vox_mix.wav')} />
      <div style={{position: 'absolute', left: 0, top: 0, transformOrigin: '0 0', transform: `translate(${540}px, ${960}px) rotate(${rot}deg) scale(${s}) translate(${-cx}px, ${-cy}px)`}}>
        <Board f={f} cur={cur} all={out > 0} />
      </div>
      {/* vignette + grain for print feel */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(40,25,10,0.45) 100%)'}} />
      <AbsoluteFill style={{opacity: 0.18, mixBlendMode: 'multiply', backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' seed='${f % 5}'/><feColorMatrix values='0 0 0 0 0.4  0 0 0 0 0.3  0 0 0 0 0.2  0 0 0 1.2 -0.3'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`}} />
      {out < 0.5 && <Caption />}
      {/* logo slapped on top of the board */}
      <div style={{position: 'absolute', left: 140, top: 620, width: 800, height: 520, opacity: f >= G.logo + 26 ? 1 : 0, transform: `rotate(-2deg) scale(${interpolate(logoP, [0, 1], [1.4, 1])})`, filter: 'drop-shadow(0 20px 30px rgba(0,0,0,0.45))'}}>
        <div style={{position: 'absolute', inset: 0, background: CREAMW, clipPath: torn('logo', 800, 520, 12)}} />
        <Img src={staticFile('dr/logo.svg')} style={{position: 'absolute', left: 60, top: -120, width: 680, height: 680}} />
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 40, textAlign: 'center', fontFamily: SANS, fontWeight: 800, fontSize: 30, letterSpacing: 6, color: INK}}>ՍՑԵՆԱՐԻ ԴԱՍ · 01</div>
      </div>
    </AbsoluteFill>
  );
};
