import React from 'react';
import {Composition} from 'remotion';
import {Reel, TOTAL} from './Reel';
import {Maison, M_TOTAL} from './Maison';
import {TikTok, T_TOTAL} from './TikTok';
export const Root: React.FC = () => (
  <>
    <Composition id="G63" component={Reel} durationInFrames={TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="G63Maison" component={Maison} durationInFrames={M_TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="G63TikTok" component={TikTok} durationInFrames={T_TOTAL} fps={30} width={1080} height={1920} />
  </>
);
