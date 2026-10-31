import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, staticFile} from 'remotion';
import {useGreekFonts} from './Greece';
import {Subs} from './Manim';
// real Manim render (scene morphs) + Armenian karaoke subtitles + score
export const ManimReal: React.FC = () => {
  useGreekFonts();
  return (
    <AbsoluteFill style={{background: '#14151A'}}>
      <OffthreadVideo src={staticFile('dr/manim_real.mp4')} muted />
      <Subs />
      <Audio src={staticFile('dr/manim_mix.wav')} />
    </AbsoluteFill>
  );
};
