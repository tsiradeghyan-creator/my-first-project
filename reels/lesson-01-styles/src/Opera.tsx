import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, interpolate, random, Easing, Sequence} from 'remotion';
import {G, G_TOTAL, VO, Amphitheatre, Column, Vase, Mask, Meander, Temple, Motes, useGreekFonts} from './Greece';

const VELVET = '#6E0A14', VELVET_D = '#2A0307', GOLD = '#E3B45A', GOLD_D = '#8C6420', CREAM = '#F6EBD6', INK = '#140A08', RED = '#D90429';
const ARM = 'ArmSerif, DejaVu Serif', SANS = 'ArmSans, DejaVu Sans', GR = 'GrSerif, DejaVu Serif', CINZEL = 'Cinzel, serif';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = Easing.bezier(0.65, 0, 0.35, 1);
const outx = Easing.bezier(0.16, 1, 0.3, 1);
const pr = (f: number, a: number, b: number, e = outx) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});

const STARTS = [G.hook, G.etym, G.contest, G.masks, G.poet, G.temple, G.peri, G.cath, G.today, G.arch, G.logo];
const ACTS = ['ԱԹԵՆՔ', 'ԾՆՈՒՆԴ', 'ՄՐՑՈՒՅԹ', 'ԴԻՄԱԿՆԵՐ', 'ԱՐԻՍՏՈՏԵԼ', 'ԿԱՌՈՒՑՎԱԾՔ', 'ՇՐՋԱԴԱՐՁ', 'ԿԱԹԱՐՍԻՍ', 'ԱՅՍՕՐ', 'ԵԶՐԱՓԱԿՈՒՄ'];
const TITLES = ['2500 տարի առաջ', 'դրամատուրգիա', 'Դիոնիսոսի տոները', 'դիմակներ', '«Պոետիկա»', 'սկիզբ · միջնամաս · վերջ', 'պերիպետիա', 'կաթարսիս', '2500 տարի անց', 'Կառույցը՝ նույնը'];
const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];
const CURTAIN_AT = [G.etym, G.contest, G.poet, G.peri, G.today, G.logo];

// stage window
const WX = 90, WY = 560, WW = 900, WH = 840;

const gold = (size: number, w = 700, font = ARM): React.CSSProperties => ({fontFamily: font, fontWeight: w, fontSize: size, lineHeight: 1.06,
  background: 'linear-gradient(180deg, #FFF3CC 0%, #E3B45A 45%, #9A6A1E 70%, #F1D18A 100%)', WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent',
  filter: 'drop-shadow(0 3px 0 rgba(60,20,5,0.6)) drop-shadow(0 8px 20px rgba(0,0,0,0.5))'});

// ---------- velvet ----------
const velvet = (dir = 90, shift = 0) => `repeating-linear-gradient(${dir}deg, ${VELVET_D} ${shift}px, #8E1220 ${shift + 22}px, #B01A2A ${shift + 34}px, #7A0D19 ${shift + 50}px, ${VELVET_D} ${shift + 70}px)`;
const Curtain: React.FC<{side: 'L' | 'R'; open: number; f: number}> = ({side, open, f}) => {
  const w = 600;
  const x = side === 'L' ? -open * (w - 70) : 1080 - w + open * (w - 70);
  const sway = Math.sin(f / 25 + (side === 'L' ? 0 : 1)) * 4;
  return (
    <div style={{position: 'absolute', left: x, top: 0, width: w, height: 1920, background: velvet(90, sway), boxShadow: side === 'L' ? '20px 0 40px rgba(0,0,0,0.6)' : '-20px 0 40px rgba(0,0,0,0.6)',
      clipPath: side === 'L' ? `polygon(0 0, 100% 0, ${100 - open * 18}% 100%, 0 100%)` : `polygon(0 0, 100% 0, 100% 100%, ${open * 18}% 100%)`}}>
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(0,0,0,0.35), rgba(0,0,0,0) 30%, rgba(0,0,0,0.5))'}} />
      {/* gold tassel tie */}
      <div style={{position: 'absolute', [side === 'L' ? 'right' : 'left']: 30, top: 1180, width: 40, height: 120, background: `linear-gradient(90deg, ${GOLD_D}, ${GOLD}, ${GOLD_D})`, borderRadius: 20, opacity: open}} />
    </div>
  );
};
const Proscenium: React.FC = () => (
  <>
    <div style={{position: 'absolute', left: WX - 30, top: WY - 30, width: WW + 60, height: WH + 60, border: '30px solid transparent', borderImage: `linear-gradient(135deg, #FFF0C2, ${GOLD} 25%, ${GOLD_D} 50%, ${GOLD} 75%, #FFF0C2) 1`, boxShadow: 'inset 0 0 40px rgba(0,0,0,0.8), 0 20px 60px rgba(0,0,0,0.6)'}} />
    {/* gilded crest */}
    <svg width={1080} height={300} style={{position: 'absolute', left: 0, top: WY - 160}}>
      <defs><linearGradient id="gl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#FFF0C2" /><stop offset="0.5" stopColor={GOLD} /><stop offset="1" stopColor={GOLD_D} /></linearGradient></defs>
      <path d="M 300 150 Q 540 20 780 150" stroke="url(#gl)" strokeWidth={14} fill="none" />
      <circle cx={540} cy={70} r={34} fill="url(#gl)" />
      <path d="M 520 70 L 540 50 L 560 70 L 540 92 Z" fill={VELVET} />
      {[...Array(9)].map((_, i) => <circle key={i} cx={330 + i * 52.5} cy={150 - Math.sin((i / 8) * Math.PI) * 112} r={7} fill="url(#gl)" />)}
    </svg>
  </>
);
const Valance: React.FC = () => (
  <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 150}}>
    <div style={{position: 'absolute', inset: 0, background: velvet(0)}} />
    <svg width={1080} height={200} style={{position: 'absolute', top: 100}}>
      {[...Array(6)].map((_, i) => <path key={i} d={`M ${i * 180} 0 Q ${i * 180 + 90} 90 ${i * 180 + 180} 0 Z`} fill="#8E1220" stroke={GOLD} strokeWidth={6} />)}
      {[...Array(54)].map((_, i) => { const x = i * 20 + 10; const k = (x % 180) / 180; const y = Math.sin(k * Math.PI) * 88; return <line key={i} x1={x} y1={y} x2={x} y2={y + 26} stroke={GOLD} strokeWidth={4} />; })}
    </svg>
  </div>
);

// ---------- what plays on stage ----------
const Win: React.FC<{children: React.ReactNode; bg?: string}> = ({children, bg = '#120606'}) => (
  <div style={{position: 'absolute', left: WX, top: WY, width: WW, height: WH, overflow: 'hidden', background: bg}}>{children}</div>
);
const BustImg: React.FC<{src: string; x: number; y: number; w: number; rot?: number; tint?: string}> = ({src, x, y, w, rot = 0, tint}) => (
  <Img src={staticFile(`dr/img/${src}.png`)} style={{position: 'absolute', left: x, top: y, width: w, transform: `rotate(${rot}deg)`, filter: `drop-shadow(0 20px 30px rgba(0,0,0,0.6)) ${tint ? 'sepia(0.5) saturate(1.4) hue-rotate(-12deg) brightness(0.95)' : ''}`}} />
);
const Spot: React.FC<{f: number; x?: number}> = ({f, x = 450}) => (
  <div style={{position: 'absolute', left: x - 330 + Math.sin(f / 40) * 40, top: -100, width: 660, height: 1100, background: 'radial-gradient(ellipse at 50% 85%, rgba(255,236,190,0.35), rgba(255,236,190,0) 60%)', clipPath: 'polygon(42% 0, 58% 0, 100% 100%, 0 100%)', mixBlendMode: 'screen'}} />
);
const StageScene: React.FC<{i: number; lf: number; f: number}> = ({i, lf, f}) => {
  switch (i) {
    case 0: return <Win><div style={{position: 'absolute', left: -90, top: -520, width: 1080, height: 1920}}><Amphitheatre f={Math.min(lf, 150)} /></div>
      <div style={{position: 'absolute', right: 30, bottom: 30, textAlign: 'right', opacity: pr(lf, 40, 52)}}><div style={{...gold(96, 700, CINZEL)}}>{Math.round(interpolate(lf, [40, 150], [0, 17000], {...clamp, easing: Easing.out(Easing.cubic)})).toLocaleString('en-US').replace(',', ' ')}</div><div style={{fontFamily: SANS, fontWeight: 700, fontSize: 24, letterSpacing: 6, color: CREAM}}>ՀԱՆԴԻՍԱՏԵՍ</div></div></Win>;
    case 1: { const m = pr(lf, 110, 140, io); return <Win bg="radial-gradient(ellipse at 50% 40%, #3a0b10, #120606)"><Spot f={f} /><BustImg src="bust_front" x={250} y={60 + (1 - pr(lf, 0, 30)) * 200} w={400} tint="g" />
      <div style={{position: 'absolute', left: 40, top: 560, opacity: pr(lf, 40, 56) * (1 - m), ...gold(80, 700, GR)}}>δρᾶμα</div>
      <div style={{position: 'absolute', right: 40, top: 560, opacity: pr(lf, 66, 82) * (1 - m), ...gold(80, 700, GR)}}>ἔργον</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center', opacity: m, ...gold(78, 700, GR)}}>δραματουργία</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 690, textAlign: 'center', opacity: pr(lf, 150, 170), fontFamily: ARM, fontWeight: 600, fontSize: 44, color: CREAM}}>գործողությունը կառուցելու արվեստ</div></Win>; }
    case 2: return <Win bg="radial-gradient(ellipse at 50% 40%, #D9673A, #8E3519)"><Meander x={0} y={20} w={900} h={34} /><Meander x={0} y={770} w={900} h={34} />
      <Vase x={-10} y={150} s={0.78} p={pr(lf, 30, 50)} name="Էսքիլես" dates="525–456" /><Vase x={300} y={120} s={0.78} p={pr(lf, 46, 66)} name="Սոֆոկլես" dates="497–406" /><Vase x={610} y={150} s={0.78} p={pr(lf, 62, 82)} name="Եվրիպիդես" dates="480–406" /></Win>;
    case 3: return <Win bg="radial-gradient(ellipse at 50% 55%, #2A1F5C, #0d0818)"><Spot f={f} /><Mask x={20} y={180} sad p={pr(lf, 4, 26)} rot={-14 + Math.sin(lf / 12) * 6} /><Mask x={520} y={150} p={pr(lf, 14, 36)} rot={12 - Math.sin(lf / 12) * 6} /></Win>;
    case 4: return <Win bg="radial-gradient(ellipse at 50% 45%, #3B2A1A, #140C08)"><Spot f={f} x={300} />
      <div style={{position: 'absolute', left: 50, top: 60, width: 500 * pr(lf, 10, 50, io) + 20, height: 720, background: 'linear-gradient(90deg, #d8c08f, #F3E2B8 30%, #F7EACB 50%, #F3E2B8 70%, #d8c08f)', overflow: 'hidden', boxShadow: '0 20px 50px rgba(0,0,0,0.6)'}}>
        <div style={{width: 520, padding: '60px 30px', textAlign: 'center', opacity: pr(lf, 40, 56)}}><div style={{fontFamily: GR, fontWeight: 700, fontSize: 44, color: INK}}>ΠΕΡΙ ΠΟΙΗΤΙΚΗΣ</div><div style={{width: 200, height: 3, background: '#B5452A', margin: '20px auto'}} /><div style={{fontFamily: ARM, fontWeight: 800, fontSize: 64, color: '#B5452A'}}>«Պոետիկա»</div><div style={{fontFamily: ARM, fontWeight: 600, fontSize: 40, color: INK, marginTop: 20}}>Արիստոտել</div><div style={{fontFamily: CINZEL, fontWeight: 700, fontSize: 30, color: '#6b4a22', marginTop: 16}}>Մ.Թ.Ա. ~335</div></div>
      </div><BustImg src="bust_34" x={500} y={300} w={420} tint="g" /></Win>;
    case 5: return <Win bg="linear-gradient(180deg, #F7C98B, #E07A4F)"><div style={{position: 'absolute', left: -90, top: -500, width: 1080, height: 1920}}><Temple f={lf} /></div></Win>;
    case 6: { const flip = pr(lf, 80, 110, io) * 180; return <Win bg="radial-gradient(ellipse at 50% 50%, #0E3B5C, #06121d)"><Spot f={f} />
      <div style={{position: 'absolute', left: 240, top: 80, width: 420, height: 520, transform: `rotate(${flip}deg)`, transformOrigin: '50% 50%'}}><BustImg src="bust_up" x={0} y={0} w={420} tint="g" /></div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 620, textAlign: 'center', opacity: pr(lf, 96, 110), ...gold(84, 700, GR)}}>περιπέτεια</div></Win>; }
    case 7: { const g = pr(lf, 40, 100); return <Win bg={`radial-gradient(circle at 50% 50%, rgba(255,236,190,${g}) 0%, rgba(227,180,90,${g * 0.7}) 30%, #2A1530 75%)`}>
      <BustImg src="bust_34r" x={240} y={120} w={420} tint="g" /><div style={{position: 'absolute', left: 0, right: 0, top: 640, textAlign: 'center', opacity: pr(lf, 56, 70), ...gold(70, 700, GR)}}>κάθαρσις</div></Win>; }
    case 8: return <Win bg="#0b0b12"><div style={{position: 'absolute', left: 120, top: 60, width: 660, height: 700, background: '#050505', borderRadius: 8, overflow: 'hidden', boxShadow: `0 0 80px rgba(227,180,90,0.25)`}}>
      {[...Array(9)].map((_, k) => <React.Fragment key={k}><div style={{position: 'absolute', left: 14, top: k * 84 - (lf * 5) % 84, width: 26, height: 40, background: CREAM, borderRadius: 5}} /><div style={{position: 'absolute', right: 14, top: k * 84 - (lf * 5) % 84, width: 26, height: 40, background: CREAM, borderRadius: 5}} /></React.Fragment>)}
      <div style={{position: 'absolute', left: 60, right: 60, top: 26, bottom: 26, overflow: 'hidden', background: 'linear-gradient(180deg, #F7C98B, #E07A4F)'}}><div style={{position: 'absolute', left: -230, top: -490, width: 1080, height: 1920, transform: 'scale(0.55)'}}><Temple f={200} /></div></div></div></Win>;
    case 9: { const m = pr(lf, 40, 70, io); return <Win bg="radial-gradient(ellipse at 50% 40%, #3a0b10, #120606)"><Spot f={f} />
      {[0, 1, 2].map((k) => <React.Fragment key={k}><div style={{opacity: 1 - m}}><Column x={130 + k * 250} y={260} h={480} w={110} p={1} /></div>
        <div style={{position: 'absolute', left: 145 + k * 250, top: 280, width: 110, height: 460, opacity: m, background: k === 1 ? RED : '#111', border: `4px solid ${GOLD}`, borderRadius: 8}}>{[...Array(7)].map((_, q) => <div key={q} style={{position: 'absolute', left: 8, top: 14 + q * 64, width: 20, height: 30, background: GOLD, borderRadius: 4}} />)}</div></React.Fragment>)}
      <svg width={900} height={300} style={{position: 'absolute', left: 0, top: 0}}><path d="M 80 250 L 450 90 L 820 250 Z" fill={GOLD} /><rect x={80} y={250} width={740} height={22} fill={GOLD} /><text x={450} y={220} textAnchor="middle" fontFamily="ArmSans" fontWeight={900} fontSize={40} fill={VELVET}>ԴՐԱՄԱՏՈՒՐԳԻԱ</text></svg></Win>; }
    default: return null;
  }
};

// playbill caption
const Playbill: React.FC = () => {
  const f = useCurrentFrame();
  let cur = VO[0];
  for (const v of VO) if (f >= v.at) cur = v;
  const next = VO[VO.indexOf(cur) + 1];
  const end = next ? next.at : G_TOTAL;
  const words = cur.t.split(' ');
  const span = (end - cur.at - 12) / words.length;
  const o = pr(f, cur.at + 6, cur.at + 14) * (1 - pr(f, end - 6, end));
  return (
    <div style={{position: 'absolute', left: 70, right: 150, top: 1480, opacity: o}}>
      <div style={{background: CREAM, border: `3px solid ${GOLD_D}`, outline: `2px solid ${GOLD}`, outlineOffset: -10, padding: '22px 30px', display: 'flex', flexWrap: 'wrap', gap: '2px 12px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)'}}>
        {words.map((w, i) => <span key={i} style={{fontFamily: ARM, fontWeight: 600, fontSize: 38, lineHeight: 1.3, color: f >= cur.at + i * span ? INK : 'rgba(20,10,8,0.3)'}}>{w}</span>)}
      </div>
    </div>
  );
};

export const Opera: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  let cur = 0;
  for (let i = 0; i < STARTS.length; i++) if (f >= STARTS[i]) cur = i;
  const lf = f - STARTS[cur];
  // curtains: closed at the very start, open; close+reopen around curtain cuts
  let open = pr(f, 6, 40, io);
  for (const c of CURTAIN_AT) {
    if (f >= c - 12 && f < c) open = Math.min(open, 1 - pr(f, c - 12, c, io));
    if (f >= c && f < c + 22 && c !== G.logo) open = Math.min(open, pr(f, c + 2, c + 22, io));
    if (c === G.logo && f >= c) open = 0;
  }
  const isLogo = cur === 10;
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, #4A0710 0%, ${VELVET_D} 70%)`}}>
      <Audio src={staticFile('dr/opera_mix.wav')} />
      {/* act heading */}
      {!isLogo && <div style={{position: 'absolute', left: 0, right: 0, top: 190, textAlign: 'center'}}>
        <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 28, letterSpacing: 8, color: GOLD, opacity: pr(lf, 4, 16)}}>ԳՈՐԾՈՂՈՒԹՅՈՒՆ {ROMAN[cur]} · {ACTS[cur]}</div>
        <div style={{marginTop: 14, opacity: pr(lf, 8, 22), transform: `translateY(${(1 - pr(lf, 8, 22)) * 20}px)`}}><span style={gold(cur === 5 ? 60 : 82)}>{TITLES[cur]}</span></div>
      </div>}
      {!isLogo && <StageScene i={cur} lf={lf} f={f} />}
      <Proscenium />
      <Curtain side="L" open={open} f={f} /><Curtain side="R" open={open} f={f} />
      <Valance />
      <Motes n={36} color="#FFD98A" />
      {isLogo && <div style={{position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center'}}>
        <div style={{display: 'inline-block', width: 760, height: 760, borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,240,200,0.95), rgba(246,235,214,0.9) 55%, rgba(246,235,214,0) 72%)', opacity: pr(lf, 10, 26), position: 'relative'}}>
          <Img src={staticFile('dr/logo.svg')} style={{position: 'absolute', left: 30, top: 30, width: 700, height: 700}} />
        </div>
        <div style={{marginTop: -60, opacity: pr(lf, 30, 44)}}><span style={gold(56, 700)}>Սցենարի դաս · 01</span></div>
      </div>}
      {!isLogo && <Playbill />}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};
