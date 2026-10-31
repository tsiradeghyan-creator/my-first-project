import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill, Audio, Freeze, OffthreadVideo, Sequence, continueRender, delayRender,
  interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing, random,
} from 'remotion';

const RED = '#D90429';
const SRC = staticFile('in.mp4');
const ARM = 'ArmBlack';
const ANTON = 'AntonD';

// ---------- timeline (output frames @30fps) ----------
const A = {from: 0, dur: 75};         // hook, src 0s, 1x
const FZ = {from: 75, dur: 36};       // freeze slam
const B = {from: 111, dur: 232};      // src 3s, 2.2x
const C = {from: 343, dur: 90};       // collage
const D = {from: 433, dur: 218};      // src 20s, 2.2x
const E = {from: 651, dur: 180};      // src 41s, 0.5x slow-mo
const F = {from: 831, dur: 282};      // src 44s, 1x release + end card
export const TOTAL = F.from + F.dur;  // 1113 = 37.1s
const BURST = E.from + 102;           // snow hits windshield

// ---------- fonts ----------
const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const fonts = [
      new FontFace(ARM, `url(${staticFile('NotoArm.ttf')})`, {weight: '100 900', stretch: '62.5% 100%'}),
      new FontFace('ArmSerif', `url(${staticFile('NotoSerifArm.ttf')})`, {weight: '100 900'}),
      new FontFace(ANTON, `url(${staticFile('Anton.ttf')})`),
    ];
    Promise.all(fonts.map((f) => f.load())).then((ls) => {
      ls.forEach((f) => (document as any).fonts.add(f));
      continueRender(h);
    });
  }, [h]);
};

// ---------- footage ----------
const grade: React.CSSProperties = {
  filter: 'contrast(1.18) saturate(0.78) brightness(0.97)',
};
const Clip: React.FC<{start: number; rate?: number; zoom?: [number, number]; dur: number; shake?: number}> = ({start, rate = 1, zoom = [1.04, 1.12], dur, shake = 0}) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, dur], zoom, {extrapolateRight: 'clamp'});
  const sx = shake ? (random(`x${f}`) - 0.5) * shake : 0;
  const sy = shake ? (random(`y${f}`) - 0.5) * shake : 0;
  return (
    <AbsoluteFill style={{transform: `translate(${sx}px,${sy}px) scale(${s})`}}>
      <OffthreadVideo src={SRC} muted startFrom={Math.round(start * 30)} playbackRate={rate}
        style={{width: '100%', height: '100%', objectFit: 'cover', ...grade}} />
    </AbsoluteFill>
  );
};

// cold tint + vignette + grain + letterbox lines
const Look: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(10,30,60,0.28), rgba(0,0,0,0) 40%, rgba(0,0,0,0.55))', mixBlendMode: 'multiply'}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,0.65) 100%)'}} />
      <AbsoluteFill style={{opacity: 0.09, backgroundImage: `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' seed='${f % 7}'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`}} />
    </AbsoluteFill>
  );
};

// ---------- text ----------
const Kinetic: React.FC<{lines: {t: string; red?: boolean; size?: number}[]; y?: number; out?: number; align?: 'left' | 'center'}> = ({lines, y = 1180, out = 9999, align = 'left'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const fadeOut = interpolate(f, [out - 6, out], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{top: y, left: 70, right: 70, alignItems: align === 'center' ? 'center' : 'flex-start', opacity: fadeOut}}>
      {lines.map((l, i) => {
        const words = l.t.split(' ');
        return (
          <div key={i} style={{display: 'flex', flexWrap: 'wrap', gap: '0 22px', justifyContent: align === 'center' ? 'center' : 'flex-start', marginBottom: 6}}>
            {words.map((w, j) => {
              const d = i * 14 + j * 4;
              const p = spring({frame: f - d, fps, config: {damping: 14, stiffness: 180}});
              const blur = interpolate(p, [0, 1], [14, 0]);
              return (
                <span key={j} style={{
                  fontFamily: ARM, fontWeight: 900, fontStretch: '75%', fontSize: l.size ?? 92, lineHeight: 1.05,
                  color: l.red ? RED : '#fff', textTransform: 'uppercase', letterSpacing: -1,
                  opacity: p, filter: `blur(${blur}px)`,
                  transform: `translateY(${(1 - p) * 60}px) scale(${1 + (1 - p) * 0.4})`,
                  textShadow: '0 6px 30px rgba(0,0,0,0.7)',
                  display: 'inline-block',
                }}>{w}</span>
              );
            })}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// slammed giant word with impact shake
const Slam: React.FC<{t: string; color?: string; size?: number; sub?: string; y?: number}> = ({t, color = '#fff', size = 210, sub, y = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 9, stiffness: 260, mass: 0.6}});
  const scale = interpolate(p, [0, 1], [3, 1]);
  const shake = f < 10 ? (random(`s${f}`) - 0.5) * 30 * (1 - f / 10) : 0;
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: `translate(${shake}px, ${y}px)`}}>
      <div style={{fontFamily: ARM, fontWeight: 900, fontStretch: '62.5%', fontSize: size, color, lineHeight: 0.95, textAlign: 'center',
        transform: `scale(${scale})`, opacity: Math.min(1, p * 2), textShadow: '0 10px 50px rgba(0,0,0,0.8)', padding: '0 40px'}}>{t}</div>
      {sub && <div style={{marginTop: 30, fontFamily: ARM, fontWeight: 600, fontSize: 46, color: '#fff', letterSpacing: 6,
        opacity: interpolate(f, [8, 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{sub}</div>}
    </AbsoluteFill>
  );
};

const Flash: React.FC<{dur?: number; color?: string}> = ({dur = 8, color = '#fff'}) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{background: color, opacity: interpolate(f, [0, dur], [0.95, 0], {extrapolateRight: 'clamp'})}} />;
};

// HUD overlay for the "plow" sections
const Hud: React.FC<{label: string; dur: number}> = ({label, dur}) => {
  const f = useCurrentFrame();
  const inP = interpolate(f, [0, 12], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const out = interpolate(f, [dur - 10, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const rpm = 0.72 + Math.sin(f / 3) * 0.12 + random(`r${f}`) * 0.08;
  const blink = Math.floor(f / 10) % 2 === 0;
  const mono: React.CSSProperties = {fontFamily: ANTON, color: '#fff', letterSpacing: 4};
  return (
    <AbsoluteFill style={{opacity: inP * out}}>
      <div style={{position: 'absolute', top: 120, left: 70, transform: `translateX(${(1 - inP) * -80}px)`}}>
        <div style={{...mono, fontSize: 34, opacity: 0.85}}><span style={{color: RED, opacity: blink ? 1 : 0.2}}>●</span> REC · G 63 · 4MATIC</div>
        <div style={{fontFamily: ARM, fontWeight: 800, fontSize: 40, color: '#fff', marginTop: 10}}>{label}</div>
      </div>
      <div style={{position: 'absolute', top: 120, right: 70, textAlign: 'right'}}>
        <div style={{fontFamily: ARM, fontWeight: 800, color: "#fff", fontSize: 30, opacity: 0.8}}>ԳԱԶ</div>
        <div style={{width: 26, height: 260, border: '2px solid rgba(255,255,255,0.8)', position: 'relative', marginLeft: 'auto', marginTop: 8}}>
          <div style={{position: 'absolute', bottom: 0, left: 0, right: 0, height: `${rpm * 100}%`, background: RED}} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 3-panel collage: SNOW / MUD / GUTS
const Collage: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const panels = [
    {src: 9, word: 'ՁՅՈՒՆ', pos: '50% 62%'},
    {src: 41.2, word: 'ՑԵԽ', pos: '50% 70%'},
    {src: 27, word: 'ԴՈՒԽ', pos: '50% 55%', red: true},
  ];
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {panels.map((p, i) => {
        const d = i * 8;
        const sp = spring({frame: f - d, fps, config: {damping: 16, stiffness: 140}});
        const dir = i % 2 === 0 ? -1 : 1;
        const wp = spring({frame: f - d - 10, fps, config: {damping: 10, stiffness: 220}});
        return (
          <div key={i} style={{position: 'absolute', left: 0, width: 1080, top: i * 646, height: 628, overflow: 'hidden',
            transform: `translateX(${(1 - sp) * dir * 1100}px)`, borderTop: i ? `6px solid ${RED}` : undefined}}>
            <Sequence from={d} layout="none">
              <OffthreadVideo src={SRC} muted startFrom={Math.round(p.src * 30)}
                style={{position: 'absolute', width: 1080, height: 1920, top: -640, objectFit: 'cover', objectPosition: p.pos, transform: `scale(${1.15 + f * 0.002})`, ...grade}} />
            </Sequence>
            <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(0,0,0,0.6), rgba(0,0,0,0) 60%)'}} />
            <div style={{position: 'absolute', left: 60, bottom: 40, fontFamily: ARM, fontWeight: 900, fontStretch: '62.5%', fontSize: 170, lineHeight: 1,
              color: p.red ? RED : '#fff', transform: `scale(${interpolate(wp, [0, 1], [2.2, 1])})`, transformOrigin: 'left bottom', opacity: Math.min(1, wp * 2),
              textShadow: '0 8px 40px rgba(0,0,0,0.7)'}}>{p.word}</div>
            <div style={{position: 'absolute', right: 50, top: 36, fontFamily: ANTON, fontSize: 40, color: '#fff', opacity: 0.8 * sp}}>0{i + 1}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// final card over the release shot
const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dark = interpolate(f, [0, 20], [0, 0.6], {extrapolateRight: 'clamp'});
  const p = spring({frame: f - 6, fps, config: {damping: 11, stiffness: 200}});
  const line = interpolate(f, [18, 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const sub = interpolate(f, [30, 44], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: `rgba(0,0,0,${dark})`, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontFamily: ARM, fontWeight: 900, fontStretch: '62.5%', fontSize: 300, color: 'transparent', WebkitTextStroke: `4px ${RED}`,
        position: 'absolute', top: 640, transform: `scale(${1.25 - p * 0.15})`, opacity: p * 0.5}}>ԴՈՒԽ</div>
      <div style={{fontFamily: ARM, fontWeight: 900, fontStretch: '62.5%', fontSize: 300, color: '#fff', position: 'absolute', top: 640,
        transform: `scale(${interpolate(p, [0, 1], [2.4, 1])})`, opacity: Math.min(1, p * 1.5), textShadow: '0 12px 60px rgba(0,0,0,0.8)'}}>ԴՈՒԽ</div>
      <div style={{position: 'absolute', top: 1010, width: 700 * line, height: 8, background: RED}} />
      <div style={{position: 'absolute', top: 1060, fontFamily: ARM, fontWeight: 700, fontSize: 50, letterSpacing: 12, color: '#fff', opacity: sub}}>G 63 · ՁՄԵՌ · ՎԱՐՊԵՏ</div>
    </AbsoluteFill>
  );
};

const Progress: React.FC = () => {
  const f = useCurrentFrame();
  return <div style={{position: 'absolute', left: 0, bottom: 0, height: 8, width: `${(f / TOTAL) * 100}%`, background: RED}} />;
};

export const Reel: React.FC = () => {
  useFonts();
  const f = useCurrentFrame();
  const vol = interpolate(f, [0, 10, TOTAL - 45, TOTAL], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Audio src={SRC} volume={vol} />

      {/* A — hook */}
      <Sequence from={A.from} durationInFrames={A.dur}>
        <Clip start={0} dur={A.dur} zoom={[1.0, 1.15]} />
        <Look />
        <Sequence from={8}><Kinetic lines={[{t: 'Ճանապարհ'}, {t: 'չկա։'}]} y={1150} /></Sequence>
      </Sequence>

      {/* freeze slam */}
      <Sequence from={FZ.from} durationInFrames={FZ.dur}>
        <Freeze frame={74}><Clip start={0} dur={1} zoom={[1.2, 1.2]} /></Freeze>
        <AbsoluteFill style={{background: 'rgba(0,0,0,0.45)'}} />
        <Look />
        <Slam t="ԲԱՅՑ ԿԱ G 63" size={150} color="#fff" />
        <Flash dur={6} color={RED} />
      </Sequence>

      {/* B — plowing, 2.2x */}
      <Sequence from={B.from} durationInFrames={B.dur}>
        <Clip start={3} rate={2.2} dur={B.dur} zoom={[1.08, 1.16]} />
        <Look />
        <Hud label="ՌԵԺԻՄ՝ ՁՅՈՒՆ ՃԵՂՔՈՂ" dur={B.dur} />
        <Sequence from={10} durationInFrames={100}><Kinetic lines={[{t: 'Ձյունը՝'}, {t: 'մինչև բամպեր։'}]} out={100} /></Sequence>
        <Sequence from={120} durationInFrames={112}><Kinetic lines={[{t: 'Իսկ նա'}, {t: 'ոտքը գազից'}, {t: 'չի հանում։', red: true}]} out={112} /></Sequence>
        <Flash dur={6} />
      </Sequence>

      {/* C — collage */}
      <Sequence from={C.from} durationInFrames={C.dur}>
        <Collage />
      </Sequence>

      {/* D — plowing 2 */}
      <Sequence from={D.from} durationInFrames={D.dur}>
        <Clip start={20} rate={2.2} dur={D.dur} zoom={[1.16, 1.06]} />
        <Look />
        <Flash dur={6} />
        <Sequence from={8} durationInFrames={95}><Kinetic lines={[{t: 'Սա վարել չի։'}]} out={95} y={1250} /></Sequence>
        <Sequence from={95} durationInFrames={123}><Slam t="ՍԱ ԶԳԱԼ Է" size={170} y={260} sub="ղեկը՝ ձեռքին · սիրտը՝ տեղում" /></Sequence>
      </Sequence>

      {/* E — slow-mo snow burst */}
      <Sequence from={E.from} durationInFrames={E.dur}>
        <Clip start={41} rate={0.5} dur={E.dur} zoom={[1.05, 1.2]} />
        <Look />
        <Flash dur={6} />
        <Sequence from={10} durationInFrames={BURST - E.from - 10}><Kinetic lines={[{t: 'Մենք՝ հետևից։'}]} y={1250} out={BURST - E.from - 10} /></Sequence>
      </Sequence>
      <Sequence from={BURST} durationInFrames={E.from + E.dur - BURST}>
        <Clip start={41 + (BURST - E.from) / 30 * 0.5} rate={0.5} dur={E.from + E.dur - BURST} zoom={[1.25, 1.32]} shake={26} />
        <Look />
        <Flash dur={10} />
        <Slam t="ՆԱ՝ ՃԱՆԱՊԱՐՀ Է ԲԱՑՈՒՄ" size={128} y={-120} />
      </Sequence>

      {/* F — release + end card */}
      <Sequence from={F.from} durationInFrames={F.dur}>
        <Clip start={44} dur={F.dur} zoom={[1.12, 1.0]} />
        <Look />
        <Flash dur={8} />
        <Sequence from={12} durationInFrames={150}><Kinetic lines={[{t: 'Ձիաուժը'}, {t: 'մեքենայինն է։'}]} out={70 + 80} y={1150} /></Sequence>
        <Sequence from={80} durationInFrames={70}><Kinetic lines={[{t: 'Դուխը՝ վարորդինը։', red: true}]} out={70} y={1340} /></Sequence>
        <Sequence from={160}><EndCard /></Sequence>
      </Sequence>

      <Progress />
    </AbsoluteFill>
  );
};
