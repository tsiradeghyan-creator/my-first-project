import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {MeshTransmissionMaterial, Environment, Lightformer} from '@react-three/drei';

export const GlassTest: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#07040F'}}>
      <ThreeCanvas width={width} height={height} camera={{position: [0, 0, 6], fov: 40}}>
        <color attach="background" args={['#07040F']} />
        <mesh position={[-1.2, 1.5, -2]}><sphereGeometry args={[1.4, 48, 48]} /><meshBasicMaterial color="#FF2BD6" /></mesh>
        <mesh position={[1.3, -1.2, -2.5]}><sphereGeometry args={[1.6, 48, 48]} /><meshBasicMaterial color="#00E5FF" /></mesh>
        <mesh position={[0.2, 0.2, -3]}><boxGeometry args={[6, 0.25, 0.1]} /><meshBasicMaterial color="#C6FF00" /></mesh>
        <mesh rotation={[f * 0.02, f * 0.03, 0]}>
          <torusKnotGeometry args={[0.9, 0.32, 200, 32]} />
          <MeshTransmissionMaterial thickness={0.6} roughness={0.05} transmission={1} ior={1.4} chromaticAberration={0.25} backside samples={6} resolution={512} />
        </mesh>
        <Environment resolution={256}>
          <Lightformer intensity={4} position={[0, 4, 3]} scale={[8, 2, 1]} />
          <Lightformer intensity={2} color="#FF2BD6" position={[-4, 0, 2]} scale={[2, 6, 1]} />
          <Lightformer intensity={2} color="#00E5FF" position={[4, 0, 2]} scale={[2, 6, 1]} />
        </Environment>
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
