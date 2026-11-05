// node render.mjs [stills|video]  — stills: final-frame PNGs; video: 8 s MP4 @30fps
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
const mode = process.argv[2] || 'stills';
const dir = path.dirname(new URL(import.meta.url).pathname);
mkdirSync(`${dir}/out`, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: mode === 'stills' ? 2 : 1 });
const seek = t => page.evaluate(t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }), t);
for (let i = 1; i <= 7; i++) {
  await page.goto(`file://${dir}/post.html?i=${i}`);
  await page.evaluate(() => document.fonts.ready);
  if (mode === 'stills') { await seek(8000); await page.screenshot({ path: `${dir}/out/post-0${i}.png` }); continue; }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'slow', '-movflags', '+faststart', `${dir}/out/post-0${i}.mp4`]);
  for (let f = 0; f < 240; f++) { await seek(f * 1000 / 30); ff.stdin.write(await page.screenshot({ type: 'jpeg', quality: 95 })); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  console.log('done', i);
}
await browser.close();
