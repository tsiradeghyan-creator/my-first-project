import React, {useEffect, useState} from 'react';
import {AbsoluteFill, Audio, Img, Sequence, continueRender, delayRender, interpolate, random, staticFile, useCurrentFrame, Easing} from 'remotion';

// ---------- palette: Attic sunset, marble, gold, red-figure pottery ----------
const GOLD = '#E8B455', GOLD2 = '#B9822F', MARBLE = '#EFE8DC', TERRA = '#C8552B', BLACKFIG = '#1B1210', AEGEAN = '#0E3B5C', NIGHT = '#120C24', RED = '#D90429', CREAM = '#F6EBD6';
const ARM = 'ArmSerif, DejaVu Serif', GR = 'GrSerif, DejaVu Serif', CINZEL = 'Cinzel, serif', SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const outx = Easing.bezier(0.16, 1, 0.3, 1);
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = outx) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});

// ---------- timeline ----------
export const G = {hook: 0, etym: 195, contest: 405, masks: 570, poet: 675, temple: 840, peri: 945, cath: 1110, today: 1245, arch: 1410, logo: 1575};
export const G_TOTAL = 1665;

export const VO = [
  {at: G.hook, t: 'Մոտ 2500 տարի առաջ Աթենքում մինչև 17 000 մարդ նստում էր քարե աստիճաններին՝ պատմություն լսելու։'},
  {at: G.etym, t: 'Այնտեղ ծնվեց դրամատուրգիան։ Հունարեն «դրամա»՝ գործողություն, «էրգոն»՝ աշխատանք։ Գործողությունը կառուցելու արվեստ։'},
  {at: G.contest, t: 'Թատրոնը մրցույթ էր՝ Դիոնիսոսի տոներին։ Մրցում էին Էսքիլեսը, Սոֆոկլեսը, Եվրիպիդեսը։'},
  {at: G.masks, t: 'Դերասանները խաղում էին դիմակներով։'},
  {at: G.poet, t: 'Մ.թ.ա. մոտ 335 թվականին Արիստոտելը գրեց «Պոետիկան»՝ դրամայի առաջին հայտնի տեսությունը։'},
  {at: G.temple, t: 'Պատմությունն ունի սկիզբ, միջնամաս և վերջ։'},
  {at: G.peri, t: 'Սյուժեն ողբերգության հոգին է։ Հերոսի ճակատագիրը պետք է շրջվի՝ պերիպետիա։'},
  {at: G.cath, t: 'Իսկ հանդիսատեսը վախի ու կարեկցանքի միջով ապրում է կաթարսիս՝ մաքրում։'},
  {at: G.today, t: '2500 տարի անց գրեթե ամեն ֆիլմ ու սերիա կառուցված է նույն սկզբունքներով։'},
  {at: G.arch, t: 'Սյուները փոխվել են։ Կառույցը՝ ոչ։ Սա է դրամատուրգիան՝ պատմության ճարտարապետությունը։'},
  {at: G.logo, t: 'Maghakian Scripts։ Սցենարի դաս առաջին։'},
];

const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const fs = [
      new FontFace('ArmSerif', `url(${staticFile('dr/NotoSerifArm.ttf')})`, {weight: '100 900', stretch: '62.5% 100%'}),
      new FontFace('ArmSans', `url(${staticFile('dr/NotoArm.ttf')})`, {weight: '100 900', stretch: '62.5% 100%'}),
      new FontFace('GrSerif', `url(${staticFile('dr/NotoSerifGr.ttf')})`, {weight: '100 900', stretch: '62.5% 100%'}),
      new FontFace('Cinzel', `url(${staticFile('dr/Cinzel.ttf')})`, {weight: '400 900'}),
    ];
    Promise.all(fs.map((x) => x.load())).then((l) => { l.forEach((x) => (document as any).fonts.add(x)); continueRender(h); });
  }, [h]);
};

// ---------- text ----------
const goldText = (size: number, w = 800): React.CSSProperties => ({fontFamily: ARM, fontWeight: w, fontSize: size, lineHeight: 1.08,
  background: 'linear-gradient(180deg, #FFF1C9 0%, #E8B455 45%, #A8701F 100%)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent',
  filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.55))'});
const plain = (size: number, color: string, w = 600, font = ARM): React.CSSProperties => ({fontFamily: font, fontWeight: w, fontSize: size, color, lineHeight: 1.12});
const Words: React.FC<{text: string; style: React.CSSProperties; d?: number; rate?: number; hi?: string[]; hiStyle?: React.CSSProperties; center?: boolean}> = ({text, style, d = 0, rate = 3, hi = [], hiStyle, center}) => {
  const f = useCurrentFrame();
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', gap: `0 ${(style.fontSize as number) * 0.25}px`, justifyContent: center ? 'center' : 'flex-start'}}>
      {text.split(' ').map((w, i) => {
        const p = pr(f, d + i * rate, d + i * rate + 14);
        const isHi = hi.some((h) => w.includes(h));
        return <span key={i} style={{...style, ...(isHi ? hiStyle : {}), display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 34}px)`, filter: `${style.filter ?? ''} blur(${(1 - p) * 8}px)`}}>{w}</span>;
      })}
    </div>
  );
};
// caption bar (the narration, readable muted)
const Caption: React.FC = () => {
  const f = useCurrentFrame();
  let cur = VO[0];
  for (const v of VO) if (f >= v.at) cur = v;
  const next = VO[VO.indexOf(cur) + 1];
  const end = next ? next.at : G_TOTAL;
  const o = pr(f, cur.at + 2, cur.at + 10) * (1 - pr(f, end - 6, end));
  const words = cur.t.split(' ');
  const span = (end - cur.at - 12) / words.length;
  return (
    <div style={{position: 'absolute', left: 70, right: 150, top: 1470, opacity: o}}>
      <div style={{display: 'flex', flexWrap: 'wrap', gap: '4px 12px', padding: '22px 28px', background: 'rgba(12,8,20,0.55)', borderRadius: 18, backdropFilter: 'blur(6px)'}}>
        {words.map((w, i) => {
          const lit = f >= cur.at + i * span;
          return <span key={i} style={{...plain(40, lit ? '#fff' : 'rgba(255,255,255,0.45)', 500, SANS)}}>{w}</span>;
        })}
      </div>
    </div>
  );
};

// ---------- atmosphere ----------
const Motes: React.FC<{n?: number; color?: string}> = ({n = 40, color = '#FFE2A0'}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {[...Array(n)].map((_, i) => {
        const x = (random(`mx${i}`) * 1080 + f * (0.3 + random(`ms${i}`) * 0.8)) % 1080;
        const y = (random(`my${i}`) * 1920 - f * (0.4 + random(`mv${i}`))) % 1920;
        const r = 2 + random(`mr${i}`) * 4;
        return <div key={i} style={{position: 'absolute', left: x, top: (y + 1920) % 1920, width: r, height: r, borderRadius: '50%', background: color, opacity: 0.25 + 0.5 * Math.abs(Math.sin(f / 20 + i)), boxShadow: `0 0 ${r * 3}px ${color}`}} />;
      })}
    </AbsoluteFill>
  );
};
const Grain: React.FC<{o?: number}> = ({o = 0.12}) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{opacity: o, mixBlendMode: 'overlay', backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.8' seed='${f % 7}'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`}} />;
};
const Vignette: React.FC = () => <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.55) 100%)'}} />;

// Greek key (meander) band
const Meander: React.FC<{x: number; y: number; w: number; h?: number; color?: string; p?: number}> = ({x, y, w, h = 40, color = BLACKFIG, p = 1}) => {
  const id = `mk${x}${y}${w}`;
  return (
    <svg width={w} height={h + 12} style={{position: 'absolute', left: x, top: y, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`}}>
      <defs><pattern id={id} width={h} height={h} patternUnits="userSpaceOnUse">
        <path d={`M 2 ${h - 2} V 2 H ${h - 2} V ${h * 0.75} H ${h * 0.25} V ${h * 0.25} H ${h * 0.75} V ${h * 0.5} H ${h * 0.5}`} fill="none" stroke={color} strokeWidth={h * 0.11} strokeLinecap="square" />
      </pattern></defs>
      <rect x={0} y={6} width={w} height={h} fill={`url(#${id})`} />
      <line x1={0} y1={2} x2={w} y2={2} stroke={color} strokeWidth={4} /><line x1={0} y1={h + 10} x2={w} y2={h + 10} stroke={color} strokeWidth={4} />
    </svg>
  );
};

// ---------- marble column ----------
const Column: React.FC<{x: number; y: number; h: number; w?: number; p?: number; tint?: string}> = ({x, y, h, w = 120, p = 1, tint = MARBLE}) => {
  const rise = (1 - p) * (h + 200);
  return (
    <div style={{position: 'absolute', left: x, top: y + rise, width: w, height: h, opacity: Math.min(1, p * 3)}}>
      <svg width={w + 40} height={h} style={{position: 'absolute', left: -20, overflow: 'visible'}}>
        <defs>
          <linearGradient id={`shaft${x}`} x1="0" x2="1">
            <stop offset="0" stopColor="#8f8676" /><stop offset="0.25" stopColor={tint} /><stop offset="0.55" stopColor="#fffaf0" /><stop offset="1" stopColor="#7d7466" />
          </linearGradient>
        </defs>
        {/* abacus + echinus */}
        <rect x={0} y={0} width={w + 40} height={22} fill={`url(#shaft${x})`} />
        <path d={`M 6 22 Q ${(w + 40) / 2} 58 ${w + 34} 22 Z`} fill={`url(#shaft${x})`} />
        {/* shaft with flutes */}
        <path d={`M 26 48 L ${w + 14} 48 L ${w + 20} ${h - 28} L 20 ${h - 28} Z`} fill={`url(#shaft${x})`} />
        {[...Array(7)].map((_, i) => <line key={i} x1={34 + i * ((w - 20) / 7)} y1={52} x2={30 + i * ((w - 8) / 7)} y2={h - 30} stroke="rgba(60,50,40,0.22)" strokeWidth={3} />)}
        {/* base */}
        <rect x={6} y={h - 28} width={w + 28} height={28} fill={`url(#shaft${x})`} />
      </svg>
    </div>
  );
};

// ---------- S1: amphitheatre at sunset ----------
const Amphitheatre: React.FC<{f: number}> = ({f}) => {
  const cx = 540, cy = 1130;
  const tiers = 20;
  const rx = (i: number) => 210 + i * 62, ry = (i: number) => 60 + i * 46;
  const crowd = pr(f, 20, 150);
  const colors = ['#F6EBD6', '#C8552B', '#E8B455', '#2E6C93', '#8A2B1E', '#EDE0C8'];
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#1C1440" /><stop offset="0.35" stopColor="#6B2D5C" /><stop offset="0.62" stopColor="#E0663A" /><stop offset="0.8" stopColor="#F7B25A" />
        </linearGradient>
        <radialGradient id="sun"><stop offset="0" stopColor="#FFF4CF" /><stop offset="0.35" stopColor="#FFD27A" /><stop offset="1" stopColor="#FFD27A" stopOpacity="0" /></radialGradient>
        <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#F2A15A" /><stop offset="1" stopColor="#2B3F6B" /></linearGradient>
      </defs>
      <rect x={0} y={0} width={1080} height={1000} fill="url(#sky)" />
      <circle cx={540} cy={820 - f * 0.25} r={260} fill="url(#sun)" />
      <circle cx={540} cy={820 - f * 0.25} r={80} fill="#FFF0C0" />
      {[0, 1, 2].map((i) => <ellipse key={i} cx={(200 + i * 350 + f * (0.4 + i * 0.2)) % 1300 - 100} cy={300 + i * 120} rx={180} ry={26} fill="#F6C6A0" opacity={0.25} />)}
      {[0, 1, 2, 3].map((i) => { const bx = (900 - f * (1.2 + i * 0.3) + i * 80) % 1200; return <path key={i} d={`M ${bx} ${420 + i * 30} q 14 -12 28 0 q 14 -12 28 0`} stroke="#2a1530" strokeWidth={4} fill="none" />; })}
      <rect x={0} y={900} width={1080} height={140} fill="url(#sea)" />
      <path d="M 0 930 C 150 860, 300 900, 420 870 C 560 830, 700 900, 820 860 C 920 830, 1000 870, 1080 850 L 1080 1040 L 0 1040 Z" fill="#3B2346" opacity={0.85} />
      {/* skene with columns */}
      <rect x={330} y={985} width={420} height={110} fill="#D9C3A0" />
      <rect x={320} y={975} width={440} height={16} fill="#EBD8B8" />
      {[...Array(8)].map((_, i) => <rect key={i} x={346 + i * 52} y={995} width={16} height={100} fill="#F3E6CC" stroke="#9b8466" strokeWidth={2} />)}
      {/* orchestra */}
      <ellipse cx={cx} cy={cy} rx={rx(0)} ry={ry(0)} fill="#E7D2AE" stroke="#b39a74" strokeWidth={4} />
      <circle cx={cx} cy={cy} r={10} fill={RED} />
      {/* tiers */}
      {[...Array(tiers)].map((_, i) => {
        const a = rx(i), b = ry(i), A = rx(i + 1), B = ry(i + 1);
        const d = `M ${cx - a} ${cy} A ${a} ${b} 0 0 0 ${cx + a} ${cy} L ${cx + A} ${cy} A ${A} ${B} 0 0 1 ${cx - A} ${cy} Z`;
        return <path key={i} d={d} fill={i % 2 ? '#C9B08A' : '#DCC6A0'} stroke="#8d7556" strokeWidth={2} />;
      })}
      {/* aisles */}
      {[0.18, 0.36, 0.5, 0.64, 0.82].map((t, k) => { const th = Math.PI * t; return <line key={k} x1={cx + rx(0) * Math.cos(th)} y1={cy + ry(0) * Math.sin(th)} x2={cx + rx(tiers) * Math.cos(th)} y2={cy + ry(tiers) * Math.sin(th)} stroke="#7a6346" strokeWidth={10} opacity={0.6} />; })}
      {/* crowd */}
      {[...Array(tiers - 1)].map((_, i) => {
        const a = (rx(i) + rx(i + 1)) / 2, b = (ry(i) + ry(i + 1)) / 2;
        const n = 10 + i * 3;
        return [...Array(n)].map((__, k) => {
          const th = Math.PI * (0.03 + 0.94 * (k + random(`c${i}-${k}`) * 0.6) / n);
          if (random(`v${i}-${k}`) > crowd * 1.15 - (i / tiers) * 0.15) return null;
          const x = cx + a * Math.cos(th), y = cy + b * Math.sin(th) - 6;
          const s = 3 + i * 0.55;
          return <g key={`${i}-${k}`}><circle cx={x} cy={y - s * 1.4} r={s * 0.7} fill="#6b4630" /><rect x={x - s} y={y - s * 0.8} width={s * 2} height={s * 1.6} rx={s * 0.5} fill={colors[Math.floor(random(`col${i}-${k}`) * colors.length)]} /></g>;
        });
      })}
    </svg>
  );
};
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const z = interpolate(f, [0, 195], [1.18, 1.0], {easing: Easing.out(Easing.quad)});
  const count = Math.round(interpolate(f, [40, 150], [0, 17000], {...clamp, easing: Easing.out(Easing.cubic)}));
  return (
    <AbsoluteFill style={{background: '#1C1440'}}>
      <AbsoluteFill style={{transform: `scale(${z})`, transformOrigin: '50% 60%'}}><Amphitheatre f={f} /></AbsoluteFill>
      <Motes n={30} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(12,8,30,0.75) 0%, rgba(12,8,30,0) 30%)'}} />
      <div style={{position: 'absolute', left: 80, top: 170}}>
        <div style={{...plain(30, '#F6D9A8', 600, CINZEL), letterSpacing: 10, opacity: pr(f, 4, 16)}}>ԱԹԵՆՔ · Մ.Թ.Ա. V ԴԱՐ</div>
        <Words text="2500 տարի առաջ" style={goldText(116)} d={8} rate={4} />
      </div>
      <div style={{position: 'absolute', right: 150, top: 470, textAlign: 'right', opacity: pr(f, 40, 52)}}>
        <div style={{...plain(110, '#fff', 800, CINZEL), textShadow: '0 6px 30px rgba(0,0,0,0.6)'}}>{count.toLocaleString('en-US').replace(',', ' ')}</div>
        <div style={{...plain(30, '#F6D9A8', 600, SANS), letterSpacing: 6}}>ՀԱՆԴԻՍԱՏԵՍ</div>
      </div>
      <Grain />
    </AbsoluteFill>
  );
};

// ---------- S2: etymology on marble ----------
const MarbleBG: React.FC = () => (
  <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 35%, #FBF6EC 0%, #E6DDCC 60%, #CFC3AE 100%)'}}>
    <svg width={1080} height={1920} style={{position: 'absolute', opacity: 0.35}}>
      <filter id="veins"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.012" numOctaves="4" seed="11" /><feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.42  0 0 0 0 0.38  0 0 0 -9 4.2" /></filter>
      <rect width={1080} height={1920} filter="url(#veins)" />
    </svg>
  </AbsoluteFill>
);
const Etym: React.FC = () => {
  const f = useCurrentFrame();
  const merge = pr(f, 110, 140, io);
  return (
    <AbsoluteFill>
      <MarbleBG />
      <Column x={-80} y={300} h={1500} w={140} p={pr(f, 0, 30)} />
      <Column x={980} y={300} h={1500} w={140} p={pr(f, 6, 36)} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 220, textAlign: 'center'}}>
        <Words text="Այնտեղ ծնվեց" style={plain(64, '#5a4a36', 500)} d={10} center />
        <Words text="դրամատուրգիան" style={{...goldText(92), filter: 'drop-shadow(0 4px 8px rgba(80,50,10,0.35))'}} d={18} center />
      </div>
      {/* two greek roots */}
      <div style={{position: 'absolute', left: 150 + merge * 120, top: 680, opacity: pr(f, 40, 56) * (1 - merge), transform: `translateY(${(1 - pr(f, 40, 56)) * 40}px)`}}>
        <div style={{...plain(110, TERRA, 700, GR)}}>δρᾶμα</div>
        <div style={{...plain(40, '#5a4a36', 500), marginTop: 8, opacity: 1 - merge}}>գործողություն</div>
      </div>
      <div style={{position: 'absolute', left: 525, top: 690, ...plain(90, GOLD2, 400, GR), opacity: pr(f, 58, 66) * (1 - merge)}}>+</div>
      <div style={{position: 'absolute', left: 610 - merge * 160, top: 680, opacity: pr(f, 66, 82) * (1 - merge), transform: `translateY(${(1 - pr(f, 66, 82)) * 40}px)`}}>
        <div style={{...plain(110, TERRA, 700, GR)}}>ἔργον</div>
        <div style={{...plain(40, '#5a4a36', 500), marginTop: 8, opacity: 1 - merge}}>աշխատանք</div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 900, textAlign: 'center', opacity: pr(f, 140, 156)}}>
        <div style={{...plain(92, BLACKFIG, 700, GR)}}>δραματουργία</div>
        <div style={{width: 520 * pr(f, 150, 170), height: 4, background: GOLD2, margin: '24px auto'}} />
        <Words text="գործողությունը կառուցելու արվեստ" style={plain(58, '#3d2f20', 600)} d={156} rate={4} center hi={['արվեստ']} hiStyle={{color: RED}} />
      </div>
      <Meander x={150} y={1330} w={780} h={36} color={GOLD2} p={pr(f, 20, 70)} />
      <Grain o={0.08} />
    </AbsoluteFill>
  );
};

// ---------- S3: red-figure pottery: the contest ----------
const Vase: React.FC<{x: number; y: number; s: number; p: number; name: string; dates: string}> = ({x, y, s, p, name, dates}) => {
  const half = 'M 0 0 L 60 0 C 62 20, 50 30, 46 50 C 120 80, 170 160, 160 260 C 150 350, 90 400, 70 430 L 90 460 L 0 460';
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 340 * s, height: 480 * s, transform: `translateY(${(1 - p) * 300}px) rotate(${(1 - p) * -12}deg)`, opacity: Math.min(1, p * 2)}}>
      <svg width={340 * s} height={480 * s} viewBox="-170 -10 340 480">
        <path d={half} fill={BLACKFIG} /><path d={half} fill={BLACKFIG} transform="scale(-1 1)" />
        {/* handles */}
        <path d="M 52 40 C 140 20, 160 90, 120 120" stroke={BLACKFIG} strokeWidth={16} fill="none" /><path d="M -52 40 C -140 20, -160 90, -120 120" stroke={BLACKFIG} strokeWidth={16} fill="none" />
        {/* terracotta bands */}
        <rect x={-150} y={140} width={300} height={10} fill={TERRA} /><rect x={-150} y={330} width={300} height={8} fill={TERRA} />
        {[...Array(10)].map((_, i) => <path key={i} d={`M ${-130 + i * 28} 365 l 10 -14 l 10 14`} stroke={TERRA} strokeWidth={4} fill="none" />)}
        {/* a red-figure actor silhouette */}
        <g fill={TERRA} transform="translate(0 170)">
          <circle cx={0} cy={14} r={16} /><path d="M -14 34 L 14 34 L 30 140 L -30 140 Z" /><path d="M 12 44 L 52 20 L 58 28 L 18 56 Z" /><path d="M -12 44 L -40 90 L -32 94 L -6 58 Z" />
        </g>
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 480 * s + 10, textAlign: 'center'}}>
        <div style={{...plain(52 * s / 0.9, CREAM, 800)}}>{name}</div>
        <div style={{...plain(26, '#F6D9A8', 500, CINZEL), letterSpacing: 4}}>{dates}</div>
      </div>
    </div>
  );
};
const Contest: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, #D9673A 0%, ${TERRA} 50%, #8E3519 100%)`}}>
      <Meander x={0} y={120} w={1080} h={44} p={pr(f, 0, 30)} />
      <Meander x={0} y={1370} w={1080} h={44} p={pr(f, 10, 40)} />
      <div style={{position: 'absolute', left: 80, right: 150, top: 220}}>
        <Words text="Թատրոնը մրցույթ էր" style={plain(84, BLACKFIG, 800)} d={4} />
        <Words text="Դիոնիսոսի տոներին" style={plain(58, CREAM, 500)} d={18} />
      </div>
      <Vase x={20} y={560} s={0.9} p={pr(f, 50, 74)} name="Էսքիլես" dates="525–456" />
      <Vase x={370} y={520} s={0.9} p={pr(f, 66, 90)} name="Սոֆոկլես" dates="497–406" />
      <Vase x={720} y={560} s={0.9} p={pr(f, 82, 106)} name="Եվրիպիդես" dates="480–406" />
      {/* laurel for the winner */}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, opacity: pr(f, 120, 140)}}>
        {[...Array(9)].map((_, i) => { const a = Math.PI * (1.1 + i * 0.1); return <ellipse key={i} cx={523 + Math.cos(a) * 90} cy={520 + Math.sin(a) * 50} rx={22} ry={9} fill={GOLD} transform={`rotate(${(a * 180) / Math.PI + 90} ${523 + Math.cos(a) * 90} ${520 + Math.sin(a) * 50})`} />; })}
        {[...Array(9)].map((_, i) => { const a = Math.PI * (1.9 - i * 0.1); return <ellipse key={i} cx={523 + Math.cos(a) * 90} cy={520 + Math.sin(a) * 50} rx={22} ry={9} fill={GOLD} transform={`rotate(${(a * 180) / Math.PI + 90} ${523 + Math.cos(a) * 90} ${520 + Math.sin(a) * 50})`} />; })}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1250, textAlign: 'center', ...plain(26, BLACKFIG, 700, CINZEL), letterSpacing: 6, opacity: pr(f, 110, 120)}}>Մ.Թ.Ա. ԿՅԱՆՔԻ ՏԱՐԻՆԵՐ</div>
      <Grain o={0.14} />
    </AbsoluteFill>
  );
};

// ---------- S4: golden masks ----------
const Mask: React.FC<{x: number; y: number; sad?: boolean; p: number; rot: number}> = ({x, y, sad, p, rot}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg) scale(${0.6 + p * 0.4})`, opacity: p}}>
    <svg width={360} height={460} viewBox="-180 -230 360 460">
      <defs><linearGradient id={`g${sad ? 's' : 'h'}`} x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFF0B8" /><stop offset="0.45" stopColor={GOLD} /><stop offset="1" stopColor="#7A4E14" /></linearGradient></defs>
      <path d="M 0 -210 C 130 -210, 160 -100, 150 0 C 140 120, 80 210, 0 220 C -80 210, -140 120, -150 0 C -160 -100, -130 -210, 0 -210 Z" fill={`url(#g${sad ? 's' : 'h'})`} stroke="#5a3a10" strokeWidth={4} />
      {/* brows */}
      <path d={sad ? 'M -110 -90 Q -60 -130 -20 -70' : 'M -110 -70 Q -60 -120 -20 -80'} stroke="#5a3a10" strokeWidth={10} fill="none" strokeLinecap="round" />
      <path d={sad ? 'M 110 -90 Q 60 -130 20 -70' : 'M 110 -70 Q 60 -120 20 -80'} stroke="#5a3a10" strokeWidth={10} fill="none" strokeLinecap="round" />
      {/* eyes */}
      <path d={sad ? 'M -105 -30 Q -65 -60 -25 -25 Q -65 -10 -105 -30 Z' : 'M -105 -35 Q -65 -10 -25 -35 Q -65 -60 -105 -35 Z'} fill={NIGHT} />
      <path d={sad ? 'M 105 -30 Q 65 -60 25 -25 Q 65 -10 105 -30 Z' : 'M 105 -35 Q 65 -10 25 -35 Q 65 -60 105 -35 Z'} fill={NIGHT} />
      {/* nose */}
      <path d="M 0 -40 L -14 50 Q 0 60 14 50 Z" fill="rgba(90,58,16,0.35)" />
      {/* mouth */}
      <path d={sad ? 'M -80 140 Q 0 60 80 140 Q 0 100 -80 140 Z' : 'M -90 90 Q 0 190 90 90 Q 0 130 -90 90 Z'} fill={NIGHT} />
    </svg>
  </div>
);
const Masks: React.FC = () => {
  const f = useCurrentFrame();
  const sw = Math.sin(f / 12) * 6;
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 55%, #2A1F5C 0%, ${NIGHT} 70%)`}}>
      <div style={{position: 'absolute', left: 290, top: 520, width: 500, height: 900, background: 'radial-gradient(ellipse, rgba(255,214,140,0.35), rgba(0,0,0,0) 65%)'}} />
      <Mask x={90} y={640} sad p={pr(f, 4, 26)} rot={-14 + sw} />
      <Mask x={630} y={600} p={pr(f, 14, 36)} rot={12 - sw} />
      <div style={{position: 'absolute', left: 80, right: 150, top: 220}}>
        <Words text="Դերասանները խաղում էին" style={plain(60, '#E7DCF5', 500)} d={2} />
        <Words text="դիմակներով" style={goldText(120)} d={14} />
      </div>
      <div style={{position: 'absolute', left: 120, top: 1150, ...plain(40, '#E7DCF5', 600), opacity: pr(f, 40, 52)}}>ողբերգություն</div>
      <div style={{position: 'absolute', left: 650, top: 1110, ...plain(40, '#E7DCF5', 600), opacity: pr(f, 48, 60)}}>կատակերգություն</div>
      <Motes n={24} />
      <Grain />
    </AbsoluteFill>
  );
};

// ---------- S5a: Aristotle's Poetics scroll ----------
const Scroll: React.FC<{p: number; children?: React.ReactNode}> = ({p, children}) => {
  const w = 120 + p * 780;
  return (
    <div style={{position: 'absolute', left: 540 - w / 2, top: 560, width: w, height: 820}}>
      <div style={{position: 'absolute', inset: '30px 0', background: 'linear-gradient(90deg, #d8c08f, #F3E2B8 20%, #F7EACB 50%, #F3E2B8 80%, #d8c08f)', boxShadow: '0 30px 80px rgba(0,0,0,0.5)', overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: (w - 780) / 2, top: 0, width: 780, height: 760}}>{children}</div>
      </div>
      {[0, 1].map((k) => <div key={k} style={{position: 'absolute', [k ? 'right' : 'left']: -30, top: 0, width: 60, height: 820, borderRadius: 30, background: 'linear-gradient(90deg, #6b4a22, #C9A066 40%, #8a6532)'}} />)}
    </div>
  );
};
const Poetics: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #3B2A1A 0%, #140C08 80%)`}}>
      <div style={{position: 'absolute', left: 80, right: 150, top: 200}}>
        <div style={{...plain(30, '#F6D9A8', 600, CINZEL), letterSpacing: 8, opacity: pr(f, 2, 12)}}>Մ.Թ.Ա. ~335</div>
        <Words text="Արիստոտել" style={goldText(120)} d={6} />
      </div>
      <Scroll p={pr(f, 20, 60, io)}>
        <div style={{textAlign: 'center', paddingTop: 70, opacity: pr(f, 50, 66)}}>
          <div style={{...plain(66, BLACKFIG, 700, GR), letterSpacing: 4}}>ΠΕΡΙ ΠΟΙΗΤΙΚΗΣ</div>
          <div style={{width: 300, height: 3, background: TERRA, margin: '24px auto'}} />
          <div style={{...plain(84, TERRA, 800)}}>«Պոետիկա»</div>
          <div style={{...plain(36, '#5a4426', 500), marginTop: 30, padding: '0 60px', lineHeight: 1.4}}>դրամայի առաջին հայտնի տեսությունը</div>
          {[...Array(6)].map((_, i) => <div key={i} style={{height: 6, margin: '26px 90px 0', background: 'rgba(60,40,20,0.15)', width: `${60 + random(`l${i}`) * 30}%`}} />)}
        </div>
      </Scroll>
      <Motes n={20} />
      <Grain />
    </AbsoluteFill>
  );
};

// ---------- S5b: the temple of story: beginning, middle, end ----------
const Temple: React.FC<{f: number; labels?: boolean; scale?: number}> = ({f, labels = true}) => {
  const ped = pr(f, 50, 74, io);
  const names = ['ՍԿԻԶԲ', 'ՄԻՋՆԱՄԱՍ', 'ՎԵՐՋ'];
  return (
    <>
      <div style={{position: 'absolute', left: 120, top: 1300, width: 840, height: 40, background: 'linear-gradient(180deg, #F3EADB, #b9ad98)', opacity: pr(f, 0, 10)}} />
      <div style={{position: 'absolute', left: 90, top: 1336, width: 900, height: 40, background: 'linear-gradient(180deg, #E9DFCF, #a99d88)', opacity: pr(f, 0, 10)}} />
      {[0, 1, 2].map((i) => <Column key={i} x={190 + i * 290} y={760} h={540} w={130} p={pr(f, 6 + i * 10, 34 + i * 10)} />)}
      {labels && [0, 1, 2].map((i) => <div key={i} style={{position: 'absolute', left: 140 + i * 290, width: 230, top: 1000, textAlign: 'center', opacity: pr(f, 30 + i * 10, 42 + i * 10)}}>
        <div style={{display: 'inline-block', padding: '8px 14px', background: i === 2 ? RED : BLACKFIG, ...plain(28, '#fff', 700, SANS), letterSpacing: 2}}>{names[i]}</div>
      </div>)}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, transform: `translateY(${(1 - ped) * -500}px)`, opacity: ped}}>
        <defs><linearGradient id="ped" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#FBF5EA" /><stop offset="1" stopColor="#BFB29C" /></linearGradient></defs>
        <path d="M 110 740 L 540 560 L 970 740 Z" fill="url(#ped)" stroke="#8d806b" strokeWidth={4} />
        <rect x={110} y={740} width={860} height={30} fill="url(#ped)" stroke="#8d806b" strokeWidth={3} />
        <text x={540} y={705} textAnchor="middle" fontFamily="ArmSerif" fontWeight={800} fontSize={54} fill={TERRA}>ՊԱՏՄՈՒԹՅՈՒՆ</text>
      </svg>
    </>
  );
};
const TempleScene: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #F7C98B 0%, #F3A86A 40%, #E07A4F 100%)'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 170, textAlign: 'center'}}>
        <Words text="սկիզբ · միջնամաս · վերջ" style={plain(66, BLACKFIG, 800)} d={2} center />
      </div>
      <Temple f={f} />
      <Motes n={20} />
      <Grain o={0.1} />
    </AbsoluteFill>
  );
};

// ---------- S5c: plot is the soul; peripeteia (the turn) ----------
const Peri: React.FC = () => {
  const f = useCurrentFrame();
  const flip = pr(f, 80, 110, io);
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${AEGEAN} 0%, #0A2236 100%)`}}>
      <div style={{position: 'absolute', left: 80, right: 150, top: 200}}>
        <Words text="Սյուժեն" style={goldText(120)} d={2} />
        <Words text="ողբերգության հոգին է" style={plain(64, '#D6E6F2', 500)} d={14} />
      </div>
      {/* fortune wheel / turning arrow */}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <g transform={`translate(540 860) rotate(${flip * 180})`}>
          <circle r={260} fill="none" stroke={GOLD} strokeWidth={6} strokeDasharray="4 18" />
          <circle r={200} fill="rgba(232,180,85,0.08)" stroke={GOLD} strokeWidth={3} />
          <path d="M -150 60 C -80 -120, 80 -120, 150 -20" fill="none" stroke={GOLD} strokeWidth={22} strokeLinecap="round" />
          <path d="M 150 -20 L 104 -40 M 150 -20 L 150 30" stroke={GOLD} strokeWidth={22} strokeLinecap="round" />
          <circle cx={-150} cy={60} r={20} fill={CREAM} />
        </g>
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1150, textAlign: 'center', opacity: pr(f, 96, 110)}}>
        <div style={{...plain(96, CREAM, 800, GR)}}>περιπέτεια</div>
        <div style={{...plain(54, RED, 800), marginTop: 6, textShadow: '0 0 30px rgba(217,4,41,0.5)'}}>պերիպետիա՝ շրջադարձ</div>
      </div>
      <Motes n={20} color="#BFE3FF" />
      <Grain />
    </AbsoluteFill>
  );
};

// ---------- S5d: catharsis ----------
const Cath: React.FC = () => {
  const f = useCurrentFrame();
  const glow = pr(f, 50, 100);
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 55%, rgba(255,236,190,${glow}) 0%, rgba(232,180,85,${glow * 0.6}) 25%, #2A1530 70%, #120C24 100%)`}}>
      <div style={{position: 'absolute', left: 80, right: 150, top: 200}}>
        <Words text="վախ + կարեկցանք" style={plain(70, '#E7DCF5', 600)} d={2} rate={5} />
        <div style={{height: 20}} />
        <Words text="կաթարսիս" style={goldText(150)} d={40} />
        <Words text="κάθαρσις · մաքրում" style={plain(52, '#F6D9A8', 500, GR)} d={56} />
      </div>
      {[...Array(14)].map((_, i) => {
        const a = (i / 14) * Math.PI * 2 + f / 90;
        const r = 120 + glow * 380;
        return <div key={i} style={{position: 'absolute', left: 540 + Math.cos(a) * r - 4, top: 1050 + Math.sin(a) * r * 0.9 - 70, width: 8, height: 140, background: 'linear-gradient(180deg, rgba(255,240,200,0), rgba(255,240,200,0.8), rgba(255,240,200,0))', transform: `rotate(${(a * 180) / Math.PI + 90}deg)`, opacity: glow}} />;
      })}
      <Motes n={50} />
      <Grain />
    </AbsoluteFill>
  );
};

// ---------- S6: 2500 years later: the screen ----------
const Today: React.FC = () => {
  const f = useCurrentFrame();
  const scroll = (f * 6) % 240;
  return (
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #0B0B12 0%, #1A0F1F 100%)'}}>
      <div style={{position: 'absolute', left: 80, right: 150, top: 200}}>
        <Words text="2500 տարի անց" style={goldText(108)} d={2} />
        <Words text="գրեթե ամեն ֆիլմ ու սերիա" style={plain(58, '#fff', 600)} d={16} />
      </div>
      {/* film strip carrying the temple */}
      <div style={{position: 'absolute', left: 140, top: 640, width: 800, height: 760, background: '#050505', overflow: 'hidden', borderRadius: 10, transform: `perspective(1600px) rotateY(${interpolate(pr(f, 0, 30), [0, 1], [-30, -8])}deg)`, boxShadow: '0 40px 120px rgba(217,4,41,0.25)'}}>
        {[...Array(9)].map((_, i) => <React.Fragment key={i}>
          <div style={{position: 'absolute', left: 16, top: i * 90 - scroll % 90, width: 30, height: 44, background: '#E8E1D4', borderRadius: 6}} />
          <div style={{position: 'absolute', right: 16, top: i * 90 - scroll % 90, width: 30, height: 44, background: '#E8E1D4', borderRadius: 6}} />
        </React.Fragment>)}
        <div style={{position: 'absolute', left: 70, right: 70, top: 30, bottom: 30, overflow: 'hidden', background: 'linear-gradient(180deg, #F7C98B, #E07A4F)'}}>
          <div style={{position: 'absolute', left: -150, top: -360, width: 1080, height: 1920, transform: 'scale(0.62)', transformOrigin: '50% 50%'}}><Temple f={200} labels /></div>
        </div>
        <svg width={800} height={760} style={{position: 'absolute', left: 0, top: 0}}>
          <circle cx={400} cy={380} r={70} fill="rgba(0,0,0,0.45)" opacity={pr(f, 30, 44)} />
          <path d="M 375 340 L 375 420 L 440 380 Z" fill="#fff" opacity={pr(f, 30, 44)} />
        </svg>
      </div>
      <Grain />
    </AbsoluteFill>
  );
};

// ---------- S7: the columns changed, the structure didn't ----------
const Arch: React.FC = () => {
  const f = useCurrentFrame();
  const morph = pr(f, 30, 70, io);
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, #1C1440 0%, #6B2D5C 45%, #E0663A 100%)`}}>
      <div style={{position: 'absolute', left: 80, right: 150, top: 190}}>
        <Words text="Սյուները փոխվել են։" style={plain(70, '#fff', 700)} d={2} />
        <Words text="Կառույցը՝ ոչ։" style={goldText(110)} d={24} />
      </div>
      {/* ancient columns morph into modern film-frame pillars */}
      {[0, 1, 2].map((i) => (
        <React.Fragment key={i}>
          <div style={{opacity: 1 - morph}}><Column x={190 + i * 290} y={760} h={540} w={130} p={1} /></div>
          <div style={{position: 'absolute', left: 205 + i * 290, top: 780 + (1 - morph) * 80, width: 130, height: 520, opacity: morph, background: i === 1 ? RED : '#111', border: '4px solid #F6D9A8', borderRadius: 8}}>
            {[...Array(8)].map((_, k) => <div key={k} style={{position: 'absolute', left: 10, top: 14 + k * 64, width: 22, height: 32, background: '#F6D9A8', borderRadius: 4}} />)}
            <div style={{position: 'absolute', left: 44, right: 8, top: 0, bottom: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', ...plain(56, '#F6D9A8', 800, CINZEL)}}>{['I', 'II', 'III'][i]}</div>
          </div>
        </React.Fragment>
      ))}
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <path d="M 110 740 L 540 560 L 970 740 Z" fill={`rgba(246,217,168,${0.9})`} stroke="#8d806b" strokeWidth={4} />
        <rect x={110} y={740} width={860} height={30} fill="#F6D9A8" />
        <text x={540} y={705} textAnchor="middle" fontFamily="ArmSerif" fontWeight={800} fontSize={50} fill={TERRA}>ԴՐԱՄԱՏՈՒՐԳԻԱ</text>
      </svg>
      <div style={{position: 'absolute', left: 90, top: 1310, width: 900, height: 34, background: '#F6D9A8'}} />
      <Motes n={30} />
      <Grain />
    </AbsoluteFill>
  );
};

const Logo: React.FC = () => {
  const f = useCurrentFrame();
  const reveal = pr(f, 6, 36, io);
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #FBF6EC 0%, #E6DDCC 70%)`}}>
      <Meander x={140} y={420} w={800} h={36} color={GOLD2} p={pr(f, 0, 30)} />
      <div style={{position: 'absolute', left: 140, top: 480, width: 800, height: 800, clipPath: `inset(0 ${(1 - reveal) * 100}% 0 0)`}}>
        <Img src={staticFile('dr/logo.svg')} style={{width: 800, height: 800}} />
      </div>
      <Meander x={140} y={1220} w={800} h={36} color={GOLD2} p={pr(f, 10, 40)} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 1320, textAlign: 'center', opacity: pr(f, 30, 44)}}>
        <div style={{...plain(48, BLACKFIG, 700)}}>Սցենարի դաս · 01</div>
        <div style={{...plain(26, '#6b5a44', 600, SANS), letterSpacing: 6, marginTop: 14}}>MAGHAKIANSCRIPTS.COM</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- transitions ----------
const ColumnWipe: React.FC = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 18], [1200, -1400], {easing: io});
  return <div style={{position: 'absolute', left: x, top: -100, width: 1300, height: 2200, transform: 'rotate(8deg)'}}>
    <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(90deg, #7d7466, #EFE8DC 25%, #fffaf0 50%, #EFE8DC 75%, #7d7466)'}} />
    {[...Array(12)].map((_, i) => <div key={i} style={{position: 'absolute', left: 50 + i * 100, top: 0, width: 6, height: 2200, background: 'rgba(60,50,40,0.18)'}} />)}
  </div>;
};
const GoldFlash: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{background: 'radial-gradient(circle, #FFF4CF, #E8B455 60%, rgba(232,180,85,0) 100%)', opacity: interpolate(f, [0, 5, 14], [0, 1, 0], clamp), mixBlendMode: 'screen'}} />;
};

export const Greece: React.FC = () => {
  useFonts();
  const S = (a: number, b: number, el: React.ReactNode) => <Sequence from={a} durationInFrames={b - a}>{el}</Sequence>;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Audio src={staticFile('dr/greece_mix.wav')} />
      {S(G.hook, G.etym, <Hook />)}
      {S(G.etym, G.contest, <Etym />)}
      {S(G.contest, G.masks, <Contest />)}
      {S(G.masks, G.poet, <Masks />)}
      {S(G.poet, G.temple, <Poetics />)}
      {S(G.temple, G.peri, <TempleScene />)}
      {S(G.peri, G.cath, <Peri />)}
      {S(G.cath, G.today, <Cath />)}
      {S(G.today, G.arch, <Today />)}
      {S(G.arch, G.logo, <Arch />)}
      {S(G.logo, G_TOTAL, <Logo />)}
      <Vignette />
      <Caption />
      {[G.etym, G.temple, G.arch].map((t) => <Sequence key={t} from={t - 9} durationInFrames={18}><ColumnWipe /></Sequence>)}
      {[G.contest, G.masks, G.poet, G.peri, G.cath, G.today, G.logo].map((t) => <Sequence key={t} from={t - 6} durationInFrames={14}><GoldFlash /></Sequence>)}
    </AbsoluteFill>
  );
};
