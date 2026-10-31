import React from 'react';
import {Composition} from 'remotion';
import {Reel, TOTAL} from './Reel';
import {Maison, M_TOTAL} from './Maison';
export const Root: React.FC = () => (
  <>
    <Composition id="G63" component={Reel} durationInFrames={TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="G63Maison" component={Maison} durationInFrames={M_TOTAL} fps={30} width={1080} height={1920} />
  </>
);
