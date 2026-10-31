import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, random, Easing} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {MeshTransmissionMaterial, Environment, Lightformer, Text} from '@react-three/drei';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';
import {useGreekFonts} from './Greece';

export const N_TOTAL = 630;
const S = {hook: 0, title: 45, ponr: 120, ex: 300, rule: 450, cta: 540};
const MAG = '#FF2BD6', CYAN = '#00E5FF', LIME = '#C6FF00', VIO = '#7B2CFF', BG = '#06030D';
const SANS = 'ArmSans, DejaVu Sans';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const outx = Easing.bezier(0.16, 1, 0.3, 1);
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = outx) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});
const back = (f: number, a: number, b: number) => interpolate(f, [a, b], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.8))});

// soft additive glow texture
const useGlow = () => useMemo(() => {
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d')!; const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,0.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256); const t = new THREE.CanvasTexture(c); return t;
}, []);
const Glow: React.FC<{color: string; pos: [number, number, number]; s: number; o?: number}> = ({color, pos, s, o = 1}) => {
  const tex = useGlow();
  return <mesh position={pos}><planeGeometry args={[s, s]} /><meshBasicMaterial map={tex} color={color} transparent opacity={o} blending={THREE.AdditiveBlending} depthWrite={false} /></mesh>;
};
const TextPlane: React.FC<{text: string; color: string; pos: [number, number, number]; w: number; size?: number}> = ({text, color, pos, w, size = 220}) => {
  const ready = typeof document !== 'undefined' && (document as any).fonts.check(`900 ${size}px ArmSans`);
  const tex = useMemo(() => {
    const c = document.createElement('canvas'); c.width = 2048; c.height = 1024; const g = c.getContext('2d')!;
    g.clearRect(0, 0, 2048, 1024); g.font = `900 ${size}px ArmSans`; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.shadowColor = color; g.shadowBlur = 40; g.fillStyle = '#ffffff'; g.fillText(text, 1024, 512); g.shadowBlur = 0; g.fillStyle = color; g.globalAlpha = 0.35; g.fillText(text, 1024, 512);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  }, [text, color, ready, size]);
  return <mesh position={pos}><planeGeometry args={[w, w / 2]} /><meshBasicMaterial map={tex} transparent toneMapped={false} depthWrite={false} /></mesh>;
};
const glass = {thickness: 0.7, roughness: 0.04, transmission: 1, ior: 1.45, chromaticAberration: 0.35, anisotropy: 0.2, backside: true, samples: 6, resolution: 512, distortion: 0.25, distortionScale: 0.4, temporalDistortion: 0} as const;

// ---------- 3D world ----------
const World: React.FC<{f: number}> = ({f}) => {
  const font = staticFile('dr/NotoArm.ttf');
  // background glows drift
  const d = (k: number, a: number) => Math.sin(f / 50 + k) * a;
  // hook: blob crashes in from far away
  const hz = interpolate(f, [0, 14], [-30, 0], {...clamp, easing: Easing.out(Easing.cubic)});
  const hookVis = f < S.title + 10;
  // title capsule
  const tVis = f >= S.title - 5 && f < S.ponr + 10;
  const tIn = back(f, S.title, S.title + 18);
  // point of no return: a neon tube travelling through a glass portal, path behind it shatters
  const pVis = f >= S.ponr - 5 && f < S.ex + 10;
  const prog = pr(f, S.ponr + 10, S.ponr + 110, io);
  const breakAt = S.ponr + 92;
  const shards = useMemo(() => [...Array(40)].map((_, i) => ({x: -3.2 + random(`sx${i}`) * 3.0, y: (random(`sy${i}`) - 0.5) * 0.3, vx: (random(`vx${i}`) - 0.5) * 0.06, vy: random(`vy${i}`) * 0.05, r: random(`r${i}`) * 6, s: 0.06 + random(`s${i}`) * 0.12})), []);
  const tube = useMemo(() => new THREE.CatmullRomCurve3([new THREE.Vector3(-4, -0.2, 0), new THREE.Vector3(-2, 0.3, 0), new THREE.Vector3(0, 0, 0), new THREE.Vector3(2, -0.3, 0), new THREE.Vector3(4, 0.2, 0)]), []);
  const tubeGeoFront = useMemo(() => new THREE.TubeGeometry(tube, 200, 0.06, 12, false), [tube]);
  // example scene: floating glass spheres
  const eVis = f >= S.ex - 5 && f < S.rule + 10;
  // rule: glass cube with text inside
  const rVis = f >= S.rule - 5 && f < S.cta + 10;
  // cta: glass button
  const cVis = f >= S.cta - 5;
  const cIn = back(f, S.cta, S.cta + 16);
  const pulse = 1 + Math.sin((f - S.cta) / 5) * 0.03;
  return (
    <>
      <color attach="background" args={[BG]} />
      <Glow color={MAG} pos={[-2 + d(0, 0.6), 3 + d(1, 0.4), -6]} s={9} o={0.9} />
      <Glow color={CYAN} pos={[2.4 + d(2, 0.5), -2.5 + d(3, 0.5), -6]} s={10} o={0.85} />
      <Glow color={VIO} pos={[0 + d(4, 0.8), 0 + d(5, 0.6), -7]} s={12} o={0.7} />
      <Glow color={LIME} pos={[2.5 + d(6, 0.4), 4.2, -6.5]} s={4} o={f > S.cta ? 0.9 : 0.35} />
      {/* neon text living BEHIND the glass, so the glass refracts it */}
      {tVis && <TextPlane text="#01" color={CYAN} pos={[0, 0.2, -2.2]} w={9} size={420} />}
      {rVis && <TextPlane text="ԵՏ ՉԿԱ" color={LIME} pos={[0, 0.1, -1.6]} w={6} size={260} />}

      {hookVis && <mesh position={[0, 0.3, hz]} rotation={[f * 0.05, f * 0.07, 0]} scale={1 - pr(f, S.title - 4, S.title + 6) * 0.9}>
        <icosahedronGeometry args={[1.25, 12]} />
        <MeshTransmissionMaterial {...glass} distortion={0.6} distortionScale={0.6} />
      </mesh>}
      {tVis && <mesh rotation={[Math.PI / 2 + Math.sin(f / 20) * 0.2, 0, Math.PI / 2 + (f - S.title) * 0.01]} scale={tIn * (1 - pr(f, S.ponr - 6, S.ponr + 4))} position={[0, 0.2, 0]}>
        <capsuleGeometry args={[0.85, 1.6, 16, 48]} />
        <MeshTransmissionMaterial {...glass} />
      </mesh>}
      {pVis && <group position={[0, 0.6, 0]} scale={0.9}>
        <mesh position={[0, 0, 0]} rotation={[0, Math.PI / 2 - 0.35, 0]} scale={back(f, S.ponr, S.ponr + 18)}>
          <torusGeometry args={[1.1, 0.22, 32, 96]} />
          <MeshTransmissionMaterial {...glass} />
        </mesh>
        {/* neon tube, drawn by progress */}
        {(() => { const seg = 12 * 6; const end = Math.floor(prog * 200); const start = f > breakAt ? 100 : 0; tubeGeoFront.setDrawRange(start * seg, Math.max(0, end - start) * seg); return null; })()}
        <mesh geometry={tubeGeoFront}>
          <meshBasicMaterial color={f > breakAt ? CYAN : MAG} toneMapped={false} />
        </mesh>
        {f > breakAt && shards.map((s, i) => { const t = f - breakAt; return <mesh key={i} position={[s.x + s.vx * t, s.y + s.vy * t - 0.004 * t * t, 0.2]} rotation={[s.r + t * 0.1, s.r * 2 + t * 0.08, 0]}>
          <tetrahedronGeometry args={[s.s]} /><meshBasicMaterial color={i % 3 ? MAG : '#ffffff'} transparent opacity={Math.max(0, 1 - t / 60)} toneMapped={false} />
        </mesh>; })}
        <mesh position={[-4 + prog * 8, interpolate(prog, [0, 0.25, 0.5, 0.75, 1], [-0.2, 0.3, 0, -0.3, 0.2]), 0.05]}><sphereGeometry args={[0.16, 24, 24]} /><meshBasicMaterial color="#ffffff" toneMapped={false} /></mesh>
      </group>}
      {eVis && [0, 1, 2].map((k) => <mesh key={k} position={[[-1.6, 1.7, -0.3][k] + Math.sin(f / 30 + k) * 0.2, [2.6, 1.2, -2.4][k] + Math.cos(f / 35 + k) * 0.2, -1]} scale={back(f, S.ex + k * 6, S.ex + 18 + k * 6) * [0.7, 0.5, 0.9][k]}>
        <sphereGeometry args={[1, 48, 48]} /><MeshTransmissionMaterial {...glass} />
      </mesh>)}
      {rVis && <mesh rotation={[0.5 + (f - S.rule) * 0.02, 0.7 + (f - S.rule) * 0.025, 0]} position={[0, 0.1, 0]} scale={back(f, S.rule, S.rule + 18) * 1.25}>
        <boxGeometry args={[1.6, 1.6, 1.6, 8, 8, 8]} /><MeshTransmissionMaterial {...glass} />
      </mesh>}
      {cVis && <mesh position={[0, -0.6, 0]} scale={[cIn * 1.9 * pulse, cIn * 0.75 * pulse, cIn * 0.5]} rotation={[0.15, Math.sin(f / 25) * 0.15, 0]}>
        <capsuleGeometry args={[0.5, 1.4, 16, 48]} /><MeshTransmissionMaterial {...glass} />
      </mesh>}
      <Environment resolution={256}>
        <Lightformer intensity={4} position={[0, 5, 3]} scale={[10, 2, 1]} />
        <Lightformer intensity={3} color={MAG} position={[-5, 0, 2]} scale={[2, 8, 1]} />
        <Lightformer intensity={3} color={CYAN} position={[5, 0, 2]} scale={[2, 8, 1]} />
      </Environment>
    </>
  );
};

// ---------- 2D overlay: kinetic neon type + liquid-glass UI ----------
const neon = (size: number, glow = MAG, color = '#fff', w = 900): React.CSSProperties => ({fontFamily: SANS, fontWeight: w, fontStretch: '75%', fontSize: size, color, lineHeight: 1.0, letterSpacing: -size * 0.02,
  textShadow: `0 0 8px ${glow}, 0 0 24px ${glow}, 0 0 60px ${glow}`});
const Pill: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div style={{display: 'inline-block', padding: '18px 34px', borderRadius: 999, background: 'linear-gradient(180deg, rgba(255,255,255,0.22), rgba(255,255,255,0.06))', backdropFilter: 'blur(22px) saturate(180%)', WebkitBackdropFilter: 'blur(22px) saturate(180%)', border: '1.5px solid rgba(255,255,255,0.45)', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.6), inset 0 -10px 30px rgba(255,255,255,0.06), 0 20px 50px rgba(0,0,0,0.35)', ...style}}>{children}</div>
);
const Pop: React.FC<{f: number; at: number; children: React.ReactNode; style?: React.CSSProperties; out?: number}> = ({f, at, children, style, out}) => {
  const p = back(f, at, at + 12);
  const o = out ? 1 - pr(f, out - 6, out) : 1;
  return <div style={{position: 'absolute', opacity: Math.min(1, p * 1.5) * o, transform: `scale(${0.6 + p * 0.4}) translateY(${(1 - p) * 40}px)`, filter: `blur(${(1 - Math.min(1, p)) * 10}px)`, ...style}}>{children}</div>;
};
const Words: React.FC<{f: number; at: number; text: string; size: number; glow?: string; rate?: number; hi?: string[]}> = ({f, at, text, size, glow = MAG, rate = 3, hi = []}) => (
  <div style={{display: 'flex', flexWrap: 'wrap', gap: `0 ${size * 0.25}px`}}>
    {text.split(' ').map((w, i) => { const p = back(f, at + i * rate, at + i * rate + 10); const h = hi.some((x) => w.replace(/[։,՝.…]/g, '') === x);
      return <span key={i} style={{...neon(size, h ? LIME : glow, h ? LIME : '#fff', h ? 900 : 800), display: 'inline-block', opacity: Math.min(1, p * 1.6), transform: `translateY(${(1 - p) * 50}px) scale(${0.7 + p * 0.3})`}}>{w}</span>; })}
  </div>
);
const Bubble: React.FC<{f: number; at: number; text: string; right?: boolean}> = ({f, at, text, right}) => {
  const p = back(f, at, at + 12);
  return <div style={{alignSelf: right ? 'flex-end' : 'flex-start', maxWidth: 720, opacity: Math.min(1, p * 1.5), transform: `scale(${0.7 + p * 0.3})`, transformOrigin: right ? '100% 100%' : '0% 100%',
    padding: '26px 34px', borderRadius: 40, background: right ? 'linear-gradient(180deg, rgba(0,229,255,0.55), rgba(123,44,255,0.45))' : 'linear-gradient(180deg, rgba(255,255,255,0.24), rgba(255,255,255,0.08))', backdropFilter: 'blur(20px) saturate(180%)',
    border: '1.5px solid rgba(255,255,255,0.4)', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.6), 0 16px 40px rgba(0,0,0,0.35)', fontFamily: SANS, fontWeight: 600, fontSize: 48, color: '#fff', lineHeight: 1.25}}>{text}</div>;
};

const Overlay: React.FC<{f: number}> = ({f}) => {
  const shake = (f >= 12 && f < 24) ? (random(`k${f}`) - 0.5) * 30 : 0;
  return (
    <AbsoluteFill style={{transform: `translate(${shake}px, ${shake * 0.4}px)`}}>
      {/* HOOK */}
      {f < S.title && <>
        <Pop f={f} at={12} out={S.title} style={{left: 0, right: 0, top: 380, textAlign: 'center'}}><span style={neon(240, MAG)}>ՍՏՈՊ։</span></Pop>
        <Pop f={f} at={22} out={S.title} style={{left: 0, right: 0, top: 1280, textAlign: 'center'}}><span style={neon(64, CYAN)}>Մատդ արդեն թերթում էր։</span></Pop>
      </>}
      {/* TITLE */}
      {f >= S.title && f < S.ponr && <>
        <Pop f={f} at={S.title + 4} out={S.ponr} style={{left: 0, right: 0, top: 300, textAlign: 'center'}}><Pill><span style={{fontFamily: SANS, fontWeight: 700, fontSize: 34, color: '#fff', letterSpacing: 6}}>ՍՑԵՆԱՐԻ ԿՈԴ</span></Pill></Pop>
        <div style={{position: 'absolute', left: 80, right: 140, top: 1240}}><Words f={f} at={S.title + 14} text="Անվերադարձ կետ" size={130} glow={CYAN} /></div>
      </>}
      {/* POINT OF NO RETURN */}
      {f >= S.ponr && f < S.ex && <>
        <div style={{position: 'absolute', left: 80, right: 140, top: 260}}><Words f={f} at={S.ponr + 4} text="Հերոսը քայլ է անում," size={84} glow={MAG} /></div>
        <div style={{position: 'absolute', left: 80, right: 140, top: 450}}><Words f={f} at={S.ponr + 30} text="ու ետ ճանապարհ այլևս չկա։" size={84} glow={CYAN} hi={['չկա']} /></div>
        <Pop f={f} at={S.ponr + 96} style={{left: 0, right: 0, top: 1300, textAlign: 'center'}}><Pill style={{padding: '22px 40px'}}><span style={{...neon(52, LIME, '#fff', 800)}}>Դիտողը մնում է՝ իմանալու, թե ինչ կլինի</span></Pill></Pop>
      </>}
      {/* EXAMPLE */}
      {f >= S.ex && f < S.rule && <>
        <Pop f={f} at={S.ex + 2} out={S.rule} style={{left: 80, top: 240}}><Pill><span style={{fontFamily: SANS, fontWeight: 700, fontSize: 32, color: '#fff', letterSpacing: 4}}>ՕՐԻՆԱԿ · ԱՌԱՋԻՆ 3 ՎԱՅՐԿՅԱՆԸ</span></Pill></Pop>
        <div style={{position: 'absolute', left: 80, right: 140, top: 700, display: 'flex', flexDirection: 'column', gap: 30}}>
          <Bubble f={f} at={S.ex + 20} text="Այսօր դուրս եկա աշխատանքից։" right />
          <Bubble f={f} at={S.ex + 60} text="Հիմա կամ սա կստացվի, կամ…" right />
          <Bubble f={f} at={S.ex + 100} text="😳 լավ, պատմիր" />
        </div>
      </>}
      {/* RULE */}
      {f >= S.rule && f < S.cta && <>
        <Pop f={f} at={S.rule + 2} out={S.cta} style={{left: 80, top: 240}}><Pill><span style={{fontFamily: SANS, fontWeight: 700, fontSize: 32, color: '#fff', letterSpacing: 4}}>ԿԱՆՈՆ</span></Pill></Pop>
        <div style={{position: 'absolute', left: 80, right: 140, top: 1250}}><Words f={f} at={S.rule + 10} text="Սկսիր այն պահից, որից հետո ետ դառնալ չի լինի։" size={76} glow={VIO} hi={['ետ']} /></div>
      </>}
      {/* CTA */}
      {f >= S.cta && <>
        <div style={{position: 'absolute', left: 80, right: 140, top: 300}}><Words f={f} at={S.cta + 4} text="Գրիր մեկնաբանություններում" size={70} glow={CYAN} /></div>
        <Pop f={f} at={S.cta + 14} style={{left: 0, right: 0, top: 1090, textAlign: 'center'}}><span style={neon(150, LIME, '#fff', 900)}>ԿՈԴ</span></Pop>
        <Pop f={f} at={S.cta + 30} style={{left: 0, right: 0, top: 1360, textAlign: 'center'}}><span style={{fontFamily: SANS, fontWeight: 600, fontSize: 46, color: '#fff'}}>ու ստացիր 10 պատրաստի հուկ DM-ով</span></Pop>
        <Pop f={f} at={S.cta + 50} style={{left: 0, right: 0, top: 1480, textAlign: 'center'}}><Pill><span style={{fontFamily: SANS, fontWeight: 700, fontSize: 32, color: '#fff'}}>Հաջորդը՝ #02 Կլիֆհենգեր →</span></Pill></Pop>
      </>}
      {/* episode progress (series feel) */}
      <div style={{position: 'absolute', left: 80, right: 140, top: 150, height: 6, borderRadius: 3, background: 'rgba(255,255,255,0.15)'}}><div style={{width: `${(f / N_TOTAL) * 100}%`, height: 6, borderRadius: 3, background: `linear-gradient(90deg, ${MAG}, ${CYAN}, ${LIME})`, boxShadow: `0 0 12px ${CYAN}`}} /></div>
      {/* smash-cut flashes */}
      {[12, S.title, S.ponr, S.ponr + 92, S.ex, S.rule, S.cta].map((t) => f >= t && f < t + 5 ? <AbsoluteFill key={t} style={{background: t === 12 ? '#fff' : (t === S.ponr + 92 ? LIME : MAG), opacity: (1 - (f - t) / 5) * 0.55, mixBlendMode: 'screen'}} /> : null)}
    </AbsoluteFill>
  );
};

export const Neon: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  // camera: punchy push-ins on every cut
  let cut = 0; for (const t of Object.values(S)) if (f >= t) cut = t;
  const push = interpolate(f - cut, [0, 20, 90], [7.4, 6.4, 6.1], clamp);
  return (
    <AbsoluteFill style={{background: BG}}>
      <Audio src={staticFile('dr/neon_mix.wav')} />
      <ThreeCanvas width={width} height={height} camera={{position: [0, 0, 6.4], fov: 42}} gl={{antialias: true}}>
        <CameraRig z={push} f={f} />
        <World f={f} />
      </ThreeCanvas>
      <Overlay f={f} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.6) 100%)', pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};
const CameraRig: React.FC<{z: number; f: number}> = ({z, f}) => {
  const {camera} = useThree();
  camera.position.set(Math.sin(f / 60) * 0.25, Math.cos(f / 80) * 0.15, z);
  camera.lookAt(0, 0.2, 0);
  return null;
};
