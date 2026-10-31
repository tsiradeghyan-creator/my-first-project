import React from 'react';
import {Composition} from 'remotion';
import {Reel, TOTAL} from './Reel';
import {Maison, M_TOTAL} from './Maison';
import {TikTok, T_TOTAL} from './TikTok';
import {Drama, D_TOTAL} from './Drama';
import {Lesson, L_TOTAL} from './Lesson';
import {StoryLesson, S_TOTAL} from './Story';
import {Greece, G_TOTAL} from './Greece';
export const Root: React.FC = () => (
  <>
    <Composition id="G63" component={Reel} durationInFrames={TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="G63Maison" component={Maison} durationInFrames={M_TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="G63TikTok" component={TikTok} durationInFrames={T_TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="Dramaturgy" component={Drama} durationInFrames={D_TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="Lesson01" component={Lesson} durationInFrames={L_TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="StoryLesson" component={StoryLesson} durationInFrames={S_TOTAL} fps={30} width={1080} height={1920} />
    <Composition id="Greece" component={Greece} durationInFrames={G_TOTAL} fps={30} width={1080} height={1920} />
  </>
);
