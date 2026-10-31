import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, interpolate, random, Easing} from 'remotion';
import {G, G_TOTAL, VO, useGreekFonts} from './Greece';

// manim palette
const BG = '#14151A', WHITE = '#ECECEC', BLUE = '#58C4DD', YELLOW = '#F7D96F', GREEN = '#83C167', RED = '#FC6255', TEAL = '#5CD0B3', GOLD = '#F0AC5F', GREY = '#6B6E78', BRAND = '#D90429';
const ARM = 'ArmSerif, DejaVu Serif', GR = 'GrSerif, DejaVu Serif', SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const smooth = Easing.bezier(0.45, 0, 0.55, 1);
const pr = (f: number, a: number, b: number, e = smooth) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});
const STARTS = [G.hook, G.etym, G.contest, G.masks, G.poet, G.temple, G.peri, G.cath, G.today, G.arch, G.logo];

// "Create": stroke draws, then fill fades in
const P: React.FC<{d: string; p: number; c?: string; w?: number; fill?: string; fillP?: number; dash?: string}> = ({d, p, c = WHITE, w = 5, fill = 'none', fillP = 0, dash}) =>
  <path d={d} pathLength={dash ? undefined : 1} strokeDasharray={dash ?? `${Math.max(0.0001, p)} 2`} stroke={c} strokeWidth={w} fill={fill} fillOpacity={fillP} strokeLinecap="round" strokeLinejoin="round" />;
const Svg: React.FC<{children: React.ReactNode}> = ({children}) => <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>{children}</svg>;
// "Write": text revealed left->right with a glowing edge
const Write: React.FC<{x: number; y: number; p: number; children: React.ReactNode; center?: boolean; w?: number}> = ({x, y, p, children, center, w}) => (
  <div style={{position: 'absolute', left: center ? 0 : x, right: center ? 0 : undefined, top: y, width: w, textAlign: center ? 'center' : 'left', clipPath: `inset(-20% ${(1 - p) * 100}% -20% 0)`, opacity: p > 0 ? 1 : 0}}>{children}</div>
);
const tx = (size: number, c = WHITE, font = ARM, w = 500): React.CSSProperties => ({fontFamily: font, fontWeight: w, fontSize: size, color: c, lineHeight: 1.15});
const Fade: React.FC<{p: number; children: React.ReactNode; dy?: number}> = ({p, children, dy = 20}) => <div style={{opacity: p, transform: `translateY(${(1 - p) * dy}px)`}}>{children}</div>;

// axes helper
const Axes: React.FC<{x0: number; y0: number; w: number; h: number; p: number; xl?: string; yl?: string}> = ({x0, y0, w, h, p, xl, yl}) => (
  <>
    <Svg>
      <P d={`M ${x0} ${y0} L ${x0 + w} ${y0}`} p={p} c={GREY} w={4} />
      <P d={`M ${x0} ${y0} L ${x0} ${y0 - h}`} p={p} c={GREY} w={4} />
      <P d={`M ${x0 + w - 16} ${y0 - 10} L ${x0 + w} ${y0} L ${x0 + w - 16} ${y0 + 10}`} p={pr(p, 0.8, 1)} c={GREY} w={4} />
      <P d={`M ${x0 - 10} ${y0 - h + 16} L ${x0} ${y0 - h} L ${x0 + 10} ${y0 - h + 16}`} p={pr(p, 0.8, 1)} c={GREY} w={4} />
    </Svg>
    {xl && <div style={{position: 'absolute', left: x0 + w - 200, top: y0 + 16, width: 200, textAlign: 'right', ...tx(30, GREY, SANS), opacity: p}}>{xl}</div>}
    {yl && <div style={{position: 'absolute', left: x0 + 16, top: y0 - h - 10, ...tx(30, GREY, SANS), opacity: p}}>{yl}</div>}
  </>
);
const tension = (t: number) => 0.08 + 0.12 * t + 0.62 * Math.pow(Math.max(0, Math.sin(Math.PI * Math.min(t, 0.86) / 0.86 / 2)), 3) * (t < 0.78 ? 1 : 1) - (t > 0.78 ? (t - 0.78) * 3.1 : 0);
const curvePath = (x0: number, y0: number, w: number, h: number, upto: number, fn = tension, n = 120) => {
  let d = '';
  for (let i = 0; i <= n * upto; i++) { const t = i / n; d += `${i ? 'L' : 'M'} ${(x0 + t * w).toFixed(1)} ${(y0 - fn(t) * h).toFixed(1)} `; }
  return d;
};

// ---------- scenes ----------
const S1: React.FC<{lf: number}> = ({lf}) => {
  // 1 700 dots in amphitheatre arcs, each dot = 10 people
  const total = 1700;
  const shown = Math.floor(interpolate(lf, [20, 150], [0, total], clamp));
  const dots: React.ReactElement[] = [];
  let k = 0;
  for (let r = 0; r < 26 && k < total; r++) {
    const R = 150 + r * 16; const n = Math.floor(Math.PI * R / 14);
    for (let i = 0; i < n && k < total; i++, k++) {
      const a = Math.PI * (i + 0.5) / n;
      if (k < shown) dots.push(<circle key={k} cx={540 - Math.cos(a) * R} cy={1250 - Math.sin(a) * R * 0.55} r={4} fill={k % 37 === 0 ? YELLOW : BLUE} opacity={0.9} />);
    }
  }
  return (
    <>
      <Write x={80} y={230} p={pr(lf, 4, 30)}><span style={tx(110, WHITE, ARM, 600)}>2500 տարի առաջ</span></Write>
      <Fade p={pr(lf, 24, 40)}><div style={{position: 'absolute', left: 84, top: 370, ...tx(44, GREY, ARM)}}>Աթենք · Դիոնիսոսի թատրոն</div></Fade>
      <Svg>{dots}<P d="M 360 1290 L 720 1290" p={pr(lf, 10, 30)} c={GOLD} w={6} /></Svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', ...tx(120, YELLOW, GR, 600)}}>≈ {(shown * 10).toLocaleString('en-US').replace(',', ' ')}</div>
      <Fade p={pr(lf, 60, 76)}><div style={{position: 'absolute', left: 0, right: 0, top: 850, textAlign: 'center', ...tx(36, GREY, SANS)}}><span style={{color: BLUE}}>●</span> = 10 հանդիսատես</div></Fade>
    </>
  );
};
const S2: React.FC<{lf: number}> = ({lf}) => {
  const m = pr(lf, 110, 140);
  return (
    <>
      <Write x={80} y={230} p={pr(lf, 2, 26)}><span style={tx(70, WHITE, ARM, 500)}>Այնտեղ ծնվեց</span></Write>
      <Write x={80} y={320} p={pr(lf, 16, 44)}><span style={tx(104, YELLOW, ARM, 600)}>դրամատուրգիան</span></Write>
      <div style={{position: 'absolute', left: 90 + m * 150, top: 720, opacity: pr(lf, 40, 54) * (1 - m)}}><div style={tx(96, BLUE, GR, 500)}>δρᾶμα</div><div style={tx(36, GREY, ARM)}>գործողություն</div></div>
      <div style={{position: 'absolute', left: 520, top: 720, opacity: pr(lf, 56, 62) * (1 - m), ...tx(96, WHITE, GR)}}>+</div>
      <div style={{position: 'absolute', left: 640 - m * 200, top: 720, opacity: pr(lf, 62, 76) * (1 - m)}}><div style={tx(96, GREEN, GR, 500)}>ἔργον</div><div style={tx(36, GREY, ARM)}>աշխատանք</div></div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 720, textAlign: 'center', opacity: m}}>
        <span style={tx(92, BLUE, GR)}>δραμα</span><span style={tx(92, GREEN, GR)}>τουργία</span>
      </div>
      <Svg><P d="M 140 900 C 300 960, 780 960, 940 900" p={pr(lf, 140, 160)} c={YELLOW} w={5} /></Svg>
      <Write center x={0} y={980} p={pr(lf, 150, 180)}><span style={tx(54, WHITE, ARM)}>գործողությունը <span style={{color: YELLOW}}>կառուցելու</span> արվեստ</span></Write>
    </>
  );
};
const S3: React.FC<{lf: number}> = ({lf}) => {
  // timeline -530 .. -400, lifespans as bars
  const x0 = 120, x1 = 960, yr = (y: number) => x0 + ((y + 530) / 130) * (x1 - x0);
  const people = [{n: 'Էսքիլես', a: -525, b: -456, c: BLUE}, {n: 'Սոֆոկլես', a: -497, b: -406, c: GREEN}, {n: 'Եվրիպիդես', a: -480, b: -406, c: GOLD}];
  return (
    <>
      <Write x={80} y={230} p={pr(lf, 2, 26)}><span style={tx(74, WHITE, ARM, 600)}>Թատրոնը՝ մրցույթ</span></Write>
      <Fade p={pr(lf, 20, 34)}><div style={{position: 'absolute', left: 84, top: 330, ...tx(42, GREY, ARM)}}>Դիոնիսոսի տոներին</div></Fade>
      <Svg>
        <P d={`M ${x0} 1200 L ${x1} 1200`} p={pr(lf, 10, 34)} c={GREY} w={4} />
        {[-525, -500, -475, -450, -425, -400].map((y, i) => <g key={y} opacity={pr(lf, 20 + i * 3, 30 + i * 3)}><line x1={yr(y)} y1={1188} x2={yr(y)} y2={1212} stroke={GREY} strokeWidth={4} /><text x={yr(y)} y={1256} textAnchor="middle" fontFamily="GrSerif" fontSize={28} fill={GREY}>{-y}</text></g>)}
        {people.map((q, i) => { const p = pr(lf, 40 + i * 16, 70 + i * 16); const y = 640 + i * 170; return <g key={i}>
          <rect x={yr(q.a)} y={y} width={(yr(q.b) - yr(q.a)) * p} height={70} rx={10} fill={q.c} fillOpacity={0.25} stroke={q.c} strokeWidth={4} />
          <line x1={yr(q.a)} y1={y + 70} x2={yr(q.a)} y2={1200} stroke={q.c} strokeWidth={2} strokeDasharray="6 8" opacity={p} />
        </g>; })}
      </Svg>
      {people.map((q, i) => <div key={i} style={{position: 'absolute', left: yr(q.a) + 16, top: 650 + i * 170, opacity: pr(lf, 56 + i * 16, 70 + i * 16), ...tx(42, WHITE, ARM, 600)}}>{q.n}</div>)}
      <Fade p={pr(lf, 110, 126)}><div style={{position: 'absolute', left: 0, right: 0, top: 1290, textAlign: 'center', ...tx(32, GREY, SANS)}}>մ.թ.ա. տարիներ</div></Fade>
    </>
  );
};
const S4: React.FC<{lf: number}> = ({lf}) => {
  const a = interpolate(lf, [30, 60, 75, 100], [0.9, 0.9, -0.9, -0.9], clamp); // y = a x^2
  const mouth = (cx: number, cy: number, aa: number) => { let d = ''; for (let i = 0; i <= 40; i++) { const x = -1 + i / 20; d += `${i ? 'L' : 'M'} ${cx + x * 110} ${cy - aa * x * x * 70 + aa * 35} `; } return d; };
  const face = (cx: number, p: number, aa: number, c: string) => <>
    <P d={`M ${cx} 700 C ${cx + 180} 700, ${cx + 200} 860, ${cx + 190} 960 C ${cx + 170} 1100, ${cx + 80} 1180, ${cx} 1190 C ${cx - 80} 1180, ${cx - 170} 1100, ${cx - 190} 960 C ${cx - 200} 860, ${cx - 180} 700, ${cx} 700 Z`} p={p} c={c} w={6} />
    <P d={`M ${cx - 110} 900 Q ${cx - 70} 870 ${cx - 30} 900`} p={p} c={c} w={6} /><P d={`M ${cx + 30} 900 Q ${cx + 70} 870 ${cx + 110} 900`} p={p} c={c} w={6} />
    <P d={mouth(cx, 1060, aa)} p={p} c={c} w={7} />
  </>;
  return (
    <>
      <Write x={80} y={230} p={pr(lf, 2, 30)}><span style={tx(74, WHITE, ARM, 600)}>Դերասաններ՝ դիմակներով</span></Write>
      <Svg>{face(300, pr(lf, 4, 30), Math.abs(a), YELLOW)}{face(780, pr(lf, 10, 36), -Math.abs(a), BLUE)}</Svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1240, textAlign: 'center', ...tx(54, WHITE, GR), opacity: pr(lf, 30, 44)}}>y = <span style={{color: a > 0 ? YELLOW : BLUE}}>{a.toFixed(1)}</span>·x²</div>
    </>
  );
};
const S5: React.FC<{lf: number}> = ({lf}) => {
  const x0 = 100, x1 = 980, yr = (y: number) => x0 + ((y + 600) / 2650) * (x1 - x0);
  const mk = pr(lf, 50, 80);
  return (
    <>
      <Write x={80} y={230} p={pr(lf, 2, 26)}><span style={tx(110, YELLOW, ARM, 600)}>Արիստոտել</span></Write>
      <Write x={84} y={370} p={pr(lf, 20, 44)}><span style={tx(54, WHITE, ARM)}>«Պոետիկա» · <span style={tx(48, GREY, GR)}>ΠΕΡΙ ΠΟΙΗΤΙΚΗΣ</span></span></Write>
      <Svg>
        <P d={`M ${x0} 1000 L ${x1} 1000`} p={pr(lf, 10, 40)} c={GREY} w={4} />
        <P d={`M ${x1 - 16} 990 L ${x1} 1000 L ${x1 - 16} 1010`} p={pr(lf, 36, 42)} c={GREY} w={4} />
        {[-500, 0, 1000, 2026].map((y, i) => <g key={y} opacity={pr(lf, 20 + i * 4, 30 + i * 4)}><line x1={yr(y)} y1={988} x2={yr(y)} y2={1012} stroke={GREY} strokeWidth={4} /><text x={yr(y)} y={1056} textAnchor="middle" fontFamily="GrSerif" fontSize={30} fill={GREY}>{y < 0 ? `${-y} մ.թ.ա.` : y}</text></g>)}
        <circle cx={yr(-335)} cy={1000} r={14 * mk} fill={YELLOW} />
        <P d={`M ${yr(-335)} 980 L ${yr(-335)} 820`} p={mk} c={YELLOW} w={4} />
        <P d={`M ${yr(-335)} 1020 C ${yr(-335) + 200} 1200, ${yr(2026) - 200} 1200, ${yr(2026)} 1020`} p={pr(lf, 100, 150)} c={BLUE} w={4} dash={undefined} />
      </Svg>
      <div style={{position: 'absolute', left: yr(-335) - 40, top: 740, opacity: mk, ...tx(56, YELLOW, GR, 600)}}>−335</div>
      <Fade p={pr(lf, 80, 96)}><div style={{position: 'absolute', left: 90, right: 150, top: 1180, ...tx(46, WHITE, ARM)}}>դրամայի առաջին հայտնի տեսությունը</div></Fade>
      <Fade p={pr(lf, 130, 150)}><div style={{position: 'absolute', left: 0, right: 0, top: 1290, textAlign: 'center', ...tx(40, BLUE, ARM)}}>2360 տարի անց՝ դեռ գործում է</div></Fade>
    </>
  );
};
const S6: React.FC<{lf: number}> = ({lf}) => {
  const bars = [{l: 'սկիզբ', c: BLUE}, {l: 'միջնամաս', c: GREEN}, {l: 'վերջ', c: RED}];
  return (
    <>
      <Write center x={0} y={240} p={pr(lf, 2, 30)}><span style={tx(64, WHITE, ARM, 600)}>Պատմություն =</span></Write>
      {bars.map((b, i) => { const p = pr(lf, 14 + i * 12, 34 + i * 12); return <React.Fragment key={i}>
        <div style={{position: 'absolute', left: 120 + i * 290, top: 760 + (1 - p) * 60, width: 260, height: 300, border: `5px solid ${b.c}`, background: `${b.c}22`, borderRadius: 12, opacity: p}} />
        <div style={{position: 'absolute', left: 120 + i * 290, width: 260, top: 880, textAlign: 'center', opacity: p, ...tx(42, b.c, ARM, 600)}}>{b.l}</div>
        {i < 2 && <div style={{position: 'absolute', left: 120 + i * 290 + 262, top: 880, opacity: p, ...tx(46, WHITE, GR)}}>+</div>}
      </React.Fragment>; })}
      <Svg><P d="M 120 1110 Q 120 1150 160 1150 L 500 1150 Q 540 1150 540 1190 Q 540 1150 580 1150 L 920 1150 Q 960 1150 960 1110" p={pr(lf, 60, 90)} c={YELLOW} w={5} /></Svg>
      <Fade p={pr(lf, 80, 96)}><div style={{position: 'absolute', left: 0, right: 0, top: 1210, textAlign: 'center', ...tx(44, YELLOW, ARM)}}>ամբողջություն</div></Fade>
    </>
  );
};
const S7: React.FC<{lf: number}> = ({lf}) => {
  const x0 = 120, y0 = 1250, w = 840, h = 520;
  const fortune = (t: number) => 0.2 + 0.7 * Math.sin(Math.PI * Math.min(t, 1) * 0.9) * (t < 0.55 ? t / 0.55 : 1) - (t > 0.55 ? Math.pow((t - 0.55) / 0.45, 1.6) * 0.72 : 0);
  const up = pr(lf, 20, 130, Easing.linear);
  const t = up; const px = x0 + t * w, py = y0 - fortune(t) * h;
  const dt = 0.01, slope = (fortune(Math.min(1, t + dt)) - fortune(Math.max(0, t - dt))) / (2 * dt);
  const ang = Math.atan2(-slope * h, w);
  return (
    <>
      <Write x={80} y={220} p={pr(lf, 2, 26)}><span style={tx(80, WHITE, ARM, 600)}>Սյուժեն՝ հոգին է</span></Write>
      <Axes x0={x0} y0={y0} w={w} h={h + 60} p={pr(lf, 4, 24)} xl="ժամանակ" yl="ճակատագիր" />
      <Svg>
        <P d={curvePath(x0, y0, w, h, up, fortune)} p={1} c={BLUE} w={7} dash="none" />
        {lf > 20 && <><line x1={px - Math.cos(ang) * 140} y1={py - Math.sin(ang) * 140} x2={px + Math.cos(ang) * 140} y2={py + Math.sin(ang) * 140} stroke={YELLOW} strokeWidth={4} />
          <circle cx={px} cy={py} r={12} fill={YELLOW} /></>}
        {t > 0.5 && <circle cx={x0 + 0.5 * w} cy={y0 - fortune(0.5) * h} r={22} fill="none" stroke={RED} strokeWidth={5} opacity={pr(lf, 80, 90)} />}
      </Svg>
      <Fade p={pr(lf, 90, 104)}><div style={{position: 'absolute', left: 0, right: 0, top: 1300, textAlign: 'center'}}><span style={tx(80, RED, GR, 600)}>περιπέτεια</span><div style={tx(44, WHITE, ARM)}>f′(t) փոխում է նշանը՝ շրջադարձ</div></div></Fade>
    </>
  );
};
const S8: React.FC<{lf: number}> = ({lf}) => {
  const x0 = 120, y0 = 1250, w = 840, h = 560;
  const up = pr(lf, 10, 100, Easing.linear);
  let area = `M ${x0} ${y0} `;
  for (let i = 0; i <= 120 * up; i++) { const t = i / 120; area += `L ${x0 + t * w} ${y0 - tension(t) * h} `; }
  area += `L ${x0 + up * w} ${y0} Z`;
  return (
    <>
      <Write x={80} y={220} p={pr(lf, 2, 26)}><span style={tx(60, WHITE, ARM, 500)}><span style={{color: BLUE}}>վախ</span> + <span style={{color: GREEN}}>կարեկցանք</span> →</span></Write>
      <Write x={80} y={310} p={pr(lf, 30, 56)}><span style={tx(110, YELLOW, ARM, 600)}>կաթարսիս</span></Write>
      <Axes x0={x0} y0={y0} w={w} h={h + 60} p={pr(lf, 4, 24)} xl="ժամանակ" yl="լարում" />
      <Svg><path d={area} fill={YELLOW} fillOpacity={0.18} /><P d={curvePath(x0, y0, w, h, up)} p={1} c={YELLOW} w={7} dash="none" /></Svg>
      <Fade p={pr(lf, 100, 116)}><div style={{position: 'absolute', left: 0, right: 0, top: 1300, textAlign: 'center', ...tx(48, WHITE, GR)}}>κάθαρσις · <span style={{fontFamily: ARM}}>մաքրում</span></div></Fade>
    </>
  );
};
const S9: React.FC<{lf: number}> = ({lf}) => {
  const x0 = 120, y0 = 1250, w = 840, h = 560;
  const n = Math.floor(interpolate(lf, [30, 140], [0, 40], clamp));
  return (
    <>
      <Write x={80} y={220} p={pr(lf, 2, 26)}><span style={tx(100, YELLOW, ARM, 600)}>2500 տարի անց</span></Write>
      <Fade p={pr(lf, 20, 36)}><div style={{position: 'absolute', left: 84, top: 350, ...tx(46, WHITE, ARM)}}>գրեթե ամեն ֆիլմ ու սերիա</div></Fade>
      <Axes x0={x0} y0={y0} w={w} h={h + 60} p={pr(lf, 4, 24)} xl="ժամանակ" yl="լարում" />
      <Svg>
        {[...Array(n)].map((_, i) => { const a = 0.85 + random(`a${i}`) * 0.3, s = (random(`s${i}`) - 0.5) * 0.08; return <path key={i} d={curvePath(x0, y0, w, h * a, 1, (t) => tension(Math.max(0, Math.min(1, t + s))))} stroke={[BLUE, GREEN, TEAL, GOLD][i % 4]} strokeWidth={2} fill="none" opacity={0.35} />; })}
        <P d={curvePath(x0, y0, w, h, 1)} p={pr(lf, 20, 60)} c={WHITE} w={8} />
      </Svg>
      <Fade p={pr(lf, 110, 126)}><div style={{position: 'absolute', left: 0, right: 0, top: 1300, textAlign: 'center', ...tx(46, WHITE, ARM)}}>նույն կորը</div></Fade>
    </>
  );
};
const S10: React.FC<{lf: number}> = ({lf}) => {
  const m = pr(lf, 40, 70);
  const cols = [BLUE, GREEN, RED];
  return (
    <>
      <Write x={80} y={220} p={pr(lf, 2, 26)}><span style={tx(72, WHITE, ARM, 600)}>Սյուները փոխվել են։</span></Write>
      <Write x={80} y={320} p={pr(lf, 24, 50)}><span style={tx(92, YELLOW, ARM, 600)}>Կառույցը՝ ոչ։</span></Write>
      <Svg>
        <P d="M 120 760 L 540 600 L 960 760 Z" p={pr(lf, 6, 40)} c={YELLOW} w={6} />
        {[0, 1, 2].map((i) => { const x = 200 + i * 290; const c = cols[i];
          // column (fluted lines) morphs into an act bar
          return <g key={i}>
            <rect x={x - 10 * (1 - m)} y={790} width={140 + 20 * (1 - m)} height={460} rx={12 * m} fill={c} fillOpacity={0.15 * m} stroke={m > 0.5 ? c : WHITE} strokeWidth={5} opacity={pr(lf, 10 + i * 6, 30 + i * 6)} />
            {[...Array(4)].map((_, k) => <line key={k} x1={x + 28 + k * 28} y1={810} x2={x + 28 + k * 28} y2={1230} stroke={WHITE} strokeWidth={3} opacity={(1 - m) * 0.6} />)}
          </g>; })}
        <P d="M 100 1270 L 980 1270" p={pr(lf, 20, 40)} c={WHITE} w={6} />
      </Svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 690, textAlign: 'center', ...tx(40, YELLOW, SANS, 700), letterSpacing: 4, opacity: pr(lf, 30, 44)}}>ԴՐԱՄԱՏՈՒՐԳԻԱ</div>
      {['I', 'II', 'III'].map((r, i) => <div key={r} style={{position: 'absolute', left: 200 + i * 290, width: 140, top: 990, textAlign: 'center', opacity: m, ...tx(64, cols[i], GR, 600)}}>{r}</div>)}
      <Fade p={pr(lf, 90, 106)}><div style={{position: 'absolute', left: 0, right: 0, top: 1310, textAlign: 'center', ...tx(44, WHITE, ARM)}}>պատմության ճարտարապետությունը</div></Fade>
    </>
  );
};
const SCENES = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10];

const Subs: React.FC = () => {
  const f = useCurrentFrame();
  let cur = VO[0];
  for (const v of VO) if (f >= v.at) cur = v;
  const next = VO[VO.indexOf(cur) + 1];
  const end = next ? next.at : G_TOTAL;
  const words = cur.t.split(' ');
  const span = (end - cur.at - 12) / words.length;
  const o = pr(f, cur.at + 4, cur.at + 10) * (1 - pr(f, end - 6, end));
  return <div style={{position: 'absolute', left: 80, right: 150, top: 1500, opacity: o, display: 'flex', flexWrap: 'wrap', gap: '2px 12px'}}>
    {words.map((w, i) => <span key={i} style={{...tx(38, f >= cur.at + i * span ? WHITE : '#4a4d57', SANS, 500)}}>{w}</span>)}
  </div>;
};

export const Manim: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  let cur = 0;
  for (let i = 0; i < STARTS.length; i++) if (f >= STARTS[i]) cur = i;
  const lf = f - STARTS[cur];
  const next = STARTS[cur + 1] ?? G_TOTAL;
  // manim-style FadeOut of everything at the end of each scene
  const out = 1 - pr(f, next - 8, next);
  const Sc = SCENES[cur];
  return (
    <AbsoluteFill style={{background: BG}}>
      <Audio src={staticFile('dr/manim_mix.wav')} />
      <AbsoluteFill style={{opacity: cur === 10 ? 1 : out}}>
        {Sc && <Sc lf={lf} />}
        {cur === 10 && <>
          <div style={{position: 'absolute', left: 140, top: 520, width: 800, height: 800, clipPath: `inset(0 ${(1 - pr(lf, 4, 36)) * 100}% 0 0)`}}><Img src={staticFile('dr/logo_rev.svg')} style={{width: 800, height: 800}} /></div>
          <Fade p={pr(lf, 30, 44)}><div style={{position: 'absolute', left: 0, right: 0, top: 1240, textAlign: 'center', ...tx(46, YELLOW, ARM, 600)}}>Սցենարի դաս · 01</div></Fade>
        </>}
      </AbsoluteFill>
      {cur < 10 && <Subs />}
      {cur < 10 && <div style={{position: 'absolute', left: 80, top: 140, ...tx(24, GREY, SANS, 600), letterSpacing: 6}}>ՍՑԵՆԱՐԻ ԴԱՍ 01 · {String(cur + 1).padStart(2, '0')}/10</div>}
    </AbsoluteFill>
  );
};
