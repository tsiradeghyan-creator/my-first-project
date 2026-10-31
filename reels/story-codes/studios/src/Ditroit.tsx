import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, random, Easing} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import {Environment, Lightformer, RoundedBox} from '@react-three/drei';
import * as THREE from 'three';
import {useGreekFonts} from '../Greece';
import {SC, TXT, ST_TOTAL} from './common';

// premium abstract 3D: pristine materials, pastel colour fields, satisfying physics, quiet typography
const CREAM = '#EFE6DA', BUTTER = '#F4D38A', TERRA = '#D9714E', COBALT = '#2E4BD8', INK = '#1E1B18', BLUSH = '#F1B9AE';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = Easing.bezier(0.65, 0, 0.35, 1);
const pr = (f: number, a: number, b: number, e = io) => interpolate(f, [a, b], [0, 1], {...clamp, easing: e});
const spring = (f: number, a: number) => { const t = Math.max(0, f - a) / 30; return f < a ? 0 : 1 - Math.exp(-6 * t) * Math.cos(10 * t); };

const useTextTex = (lines: {t: string; size: number; color: string; w?: number}[], bg: string | null, W = 1024, H = 512) => {
  const ready = typeof document !== 'undefined' && (document as any).fonts.check('700 60px ArmSans');
  return useMemo(() => {
    const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d')!;
    if (bg) { g.fillStyle = bg; g.fillRect(0, 0, W, H); }
    const total = lines.reduce((a, l) => a + l.size * 1.25, 0); let y = H / 2 - total / 2;
    for (const l of lines) { g.font = `${l.w ?? 700} ${l.size}px ArmSans`; g.fillStyle = l.color; g.textAlign = 'center'; g.textBaseline = 'top'; g.fillText(l.t, W / 2, y); y += l.size * 1.25; }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  }, [ready, bg, W, H, JSON.stringify(lines)]);
};
const Card: React.FC<{lines: {t: string; size: number; color: string; w?: number}[]; color: string; pos: [number, number, number]; rot?: [number, number, number]; s?: number; w?: number; h?: number}> = ({lines, color, pos, rot = [0, 0, 0], s = 1, w = 3.2, h = 1.6}) => {
  const tex = useTextTex(lines, color, 1024, Math.round(1024 * h / w));
  return (
    <group position={pos} rotation={rot} scale={s}>
      <RoundedBox args={[w, h, 0.18]} radius={0.09} smoothness={6} castShadow receiveShadow>
        <meshPhysicalMaterial color={color} roughness={0.35} clearcoat={1} clearcoatRoughness={0.15} />
      </RoundedBox>
      <mesh position={[0, 0, 0.0905]}><planeGeometry args={[w * 0.96, h * 0.92]} /><meshBasicMaterial map={tex} toneMapped={false} /></mesh>
    </group>
  );
};

const N = 20; // tiles receding into depth
const tz = (i: number) => 3 - i * 1.0;
const World: React.FC<{f: number}> = ({f}) => {
  const travel = pr(f, SC.ponr + 10, SC.ex - 20, Easing.inOut(Easing.cubic));
  const gate = 8;
  const sz = f < SC.ponr ? tz(1) : interpolate(travel, [0, 1], [tz(1), tz(14)]);
  const drop = f < SC.title ? interpolate(f, [0, 16], [7, 0.6], {...clamp, easing: Easing.in(Easing.quad)}) : 0.6;
  const squash = f >= 16 && f < 34 ? 1 - Math.sin(((f - 16) / 18) * Math.PI) * 0.3 * Math.exp(-(f - 16) / 10) : 1;
  const {camera} = useThree();
  const sway = Math.sin(f / 70) * 0.8;
  const lift = pr(f, SC.ponr + 95, SC.ponr + 140) * (1 - pr(f, SC.ex - 30, SC.ex));
  camera.position.set(sway + 1.2 + lift * 2.5, 3.4 + lift * 4.5, sz + 6.2 + lift * 3);
  camera.lookAt(0, 0.6 - lift * 1.5, sz - 2.5 + lift * 2.5);
  const passed = sz < tz(gate) - 0.6;
  return (
    <>
      <color attach="background" args={[CREAM]} />
      <fog attach="fog" args={[CREAM, 10, 24]} />
      <directionalLight position={[4, 9, 4]} intensity={2.4} castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-8} shadow-camera-right={8} shadow-camera-top={14} shadow-camera-bottom={-14} />
      <ambientLight intensity={0.55} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -3, -6]} receiveShadow><planeGeometry args={[80, 80]} /><meshStandardMaterial color={BLUSH} roughness={0.95} /></mesh>
      {/* colour-field wall far away */}
      <mesh position={[0, 4, -22]}><planeGeometry args={[60, 30]} /><meshStandardMaterial color={BUTTER} roughness={1} /></mesh>
      {[...Array(N)].map((_, i) => {
        const behind = passed && tz(i) > sz + 0.7;
        const t = behind ? Math.max(0, f - (SC.ponr + 100 + Math.max(0, (gate - i)) * 3)) : 0;
        const y = -0.5 * 0.014 * t * t;
        return <RoundedBox key={i} args={[1.7, 0.32, 0.92]} radius={0.07} smoothness={4} position={[0, y, tz(i)]} rotation={[t * 0.035, 0, t * 0.02 * (i % 2 ? 1 : -1)]} castShadow receiveShadow>
          <meshPhysicalMaterial color={i === gate ? COBALT : i % 2 ? BUTTER : '#FBF4E8'} roughness={0.28} clearcoat={0.9} clearcoatRoughness={0.1} />
        </RoundedBox>;
      })}
      {/* the arch: point of no return */}
      <mesh position={[0, 0.16, tz(gate)]} castShadow>
        <torusGeometry args={[1.15, 0.11, 32, 96, Math.PI]} />
        <meshPhysicalMaterial color={TERRA} roughness={0.18} clearcoat={1} />
      </mesh>
      {/* hero: pearl ceramic sphere */}
      <mesh position={[0, drop, sz]} scale={[1 / Math.sqrt(squash), squash, 1 / Math.sqrt(squash)]} rotation={[-(tz(1) - sz) * 2.2, 0, 0]} castShadow>
        <sphereGeometry args={[0.42, 64, 64]} />
        <meshPhysicalMaterial color={'#ffffff'} roughness={0.12} clearcoat={1} clearcoatRoughness={0.05} sheen={0.4} sheenColor={BLUSH} />
      </mesh>
      {f >= SC.title - 4 && f < SC.ponr + 6 && <Card lines={[{t: TXT.kicker, size: 64, color: '#ffffff', w: 600}, {t: TXT.title, size: 104, color: '#ffffff', w: 800}]} color={COBALT} pos={[0, 2.5, tz(1) - 2.8]} rot={[-0.3, (1 - spring(f, SC.title)) * Math.PI, 0]} s={0.62} w={4.2} h={2} />}
      {f >= SC.ex - 4 && f < SC.rule + 6 && <>
        <Card lines={[{t: TXT.ex1, size: 64, color: INK, w: 700}]} color={'#ffffff'} pos={[-0.25, 2.9 + (1 - spring(f, SC.ex + 6)) * 3, sz - 2.8]} rot={[-0.3, 0.12, 0.04]} s={0.5} w={5.6} h={1.0} />
        <Card lines={[{t: TXT.ex2, size: 64, color: '#ffffff', w: 700}]} color={TERRA} pos={[0.3, 2.0 + (1 - spring(f, SC.ex + 46)) * 3, sz - 2.6]} rot={[-0.3, -0.12, -0.03]} s={0.5} w={5.6} h={1.0} />
      </>}
      {f >= SC.rule - 4 && f < SC.cta + 6 && <Card lines={[{t: 'Կանոն', size: 60, color: COBALT, w: 600}, {t: 'Սկսիր այն պահից,', size: 84, color: INK, w: 800}, {t: 'որից հետո ետ', size: 84, color: INK, w: 800}, {t: 'դառնալ չի լինի։', size: 84, color: INK, w: 800}]} color={'#FBF4E8'} pos={[0, 2.5, sz - 2.8]} rot={[-0.3, (1 - spring(f, SC.rule)) * -Math.PI, 0]} s={0.6} w={3.8} h={3.0} />}
      {f >= SC.cta - 4 && (() => { const press = f > SC.cta + 34 && f < SC.cta + 44 ? 0.9 : 1; return <Card lines={[{t: TXT.cta2, size: 230, color: '#ffffff', w: 900}]} color={TERRA} pos={[0, 2.3 + (1 - spring(f, SC.cta)) * 4, sz - 2.8]} rot={[-0.3, 0, 0]} s={0.6 * press} w={3.0} h={1.5} />; })()}
      <Environment resolution={256}>
        <Lightformer intensity={3} position={[0, 6, 4]} scale={[10, 3, 1]} />
        <Lightformer intensity={1.6} color={BUTTER} position={[-6, 2, 2]} scale={[3, 6, 1]} />
        <Lightformer intensity={1.6} color={BLUSH} position={[6, 2, 2]} scale={[3, 6, 1]} />
      </Environment>
    </>
  );
};

const Type: React.FC<{f: number}> = ({f}) => {
  const fade = (a: number, b: number) => pr(f, a, a + 12) * (1 - pr(f, b - 10, b));
  const lbl: React.CSSProperties = {fontFamily: 'ArmSans', fontWeight: 600, letterSpacing: 2, color: INK, textAlign: 'center', position: 'absolute', left: 80, right: 140};
  return (
    <AbsoluteFill>
      <div style={{...lbl, top: 260, fontSize: 64, opacity: fade(18, SC.title)}}>{TXT.hook}</div>
      <div style={{...lbl, top: 1500, fontSize: 56, opacity: fade(SC.ponr + 6, SC.ex)}}>{TXT.p1}</div>
      <div style={{...lbl, top: 1580, fontSize: 56, fontWeight: 800, opacity: fade(SC.ponr + 50, SC.ex)}}>{TXT.p2}</div>
      <div style={{...lbl, top: 1520, fontSize: 52, opacity: fade(SC.cta + 10, ST_TOTAL + 20)}}>{TXT.cta1} <b>ԿՈԴ</b> {TXT.cta3.replace('ու ', 'ու ')}</div>
      <div style={{position: 'absolute', left: 80, top: 150, fontFamily: 'ArmSans', fontWeight: 600, fontSize: 24, letterSpacing: 6, color: INK, opacity: 0.6}}>01 / 12</div>
    </AbsoluteFill>
  );
};

export const DitroitStyle: React.FC = () => {
  useGreekFonts();
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: CREAM}}>
      <Audio src={staticFile('dr/st_ditroit.wav')} />
      <ThreeCanvas width={width} height={height} shadows camera={{position: [0, 4, 8], fov: 48}}>
        <World f={f} />
      </ThreeCanvas>
      <Type f={f} />
    </AbsoluteFill>
  );
};
