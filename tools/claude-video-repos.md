# Claude makes video with code: repos to keep (from the «Вот это кино» guide, @mama_mozg, Nov 2026)

Method: Claude writes the film as a web page (canvas, p5.js, three.js or Remotion), headless Chrome screenshots every
frame (24 to 60 a second), ffmpeg joins frames and music into an MP4. Strong for motion graphics, titles, explainers,
lyric videos, hand-painted cartoons, 3D product shots. Not for photoreal people: use Seedance / Higgsfield for those
(and the `film-crew` rule for every video prompt). Start with 10 to 30 second pieces; long renders eat usage limits.
Checked on GitHub 2026-11-03 (stars, licence):

| Repo | What it is | Stars | Licence | Use for us |
|---|---|---|---|---|
| [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 66 film styles in code for Claude Code (watercolour, ink, anime, news), saves a client's style | 11.6k | MIT | studio Instagram, series titles, brand-consistent promos |
| [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | hand-painted cartoon starter (p5.js + p5.brush) | 2.5k | MIT | **children's books**: animated characters, book trailers, fairy-tale shorts |
| [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) | 15 motion-design styles from one prompt each | 3.0k | MIT | title sequences, pitch-deck motion, logline trailers |
| [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) | full music video directed by Claude (source) | 2.8k | none stated | reference for a multi-scene animated piece |
| [joeseesun/opus-video-prompts](https://github.com/joeseesun/opus-video-prompts) | copy-ready prompts and 54 cases | 0.9k | none stated | prompt library |
| [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | viral videos with their prompts | 13.4k | MIT | inspiration, proven prompts |
| [athemeroy/awesome-claude-5-5-videos](https://github.com/athemeroy/awesome-claude-5-5-videos) | source-linked workflows | 0.9k | CC-BY-4.0 | workflows |
Also in the guide: pdoom-video (4K clip), Skillry (originals and remakes). The guide's stats (215-video study, 71.6%)
and its "5 ways to earn" are unverified marketing; the repos are real.

Our existing piece in this direction: `remotion-video-creation` skill. Install candidates for the laptop (VS Code):
Lemo-Opuscar and ClaudeAnimationBase, then one 15 second test (children's book character, or «84-ի ամառը» titles).
