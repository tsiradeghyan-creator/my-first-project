"""Pack the film into one self-contained HTML file: black letterboxed cinema frame, one quiet play button."""
import base64, sys
mp4, out = sys.argv[1], sys.argv[2]
b64 = base64.b64encode(open(mp4, 'rb').read()).decode()
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Last Page</title>
<style>
  :root {{ --bg:#000; --fg:#e9dfc8; }}
  html,body {{ margin:0; height:100%; background:var(--bg); overflow:hidden; }}
  .frame {{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center; background:#000; }}
  .scope {{ position:relative; width:min(100vw, calc(100vh * 2.388)); aspect-ratio:1280/536; background:#000; }}
  video {{ width:100%; height:100%; display:block; background:#000; }}
  button {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:64px; height:64px;
           border-radius:50%; border:1px solid rgba(233,223,200,.35); background:rgba(0,0,0,.35); cursor:pointer;
           transition:opacity .6s ease, border-color .3s ease; padding:0; }}
  button:hover, button:focus-visible {{ border-color:rgba(233,223,200,.8); outline:none; }}
  button svg {{ width:22px; height:22px; margin-left:4px; fill:var(--fg); opacity:.85; }}
  button.hidden {{ opacity:0; pointer-events:none; }}
</style></head>
<body>
<div class="frame"><div class="scope">
  <video id="v" playsinline preload="auto" src="data:video/mp4;base64,{b64}"></video>
  <button id="b" aria-label="Play"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12-7.5z"/></svg></button>
</div></div>
<script>
  const v = document.getElementById('v'), b = document.getElementById('b');
  b.addEventListener('click', () => {{ v.currentTime = v.ended ? 0 : v.currentTime; v.play(); b.classList.add('hidden'); }});
  v.addEventListener('click', () => {{ if (!v.paused) {{ v.pause(); b.classList.remove('hidden'); }} }});
  v.addEventListener('ended', () => b.classList.remove('hidden'));
</script>
</body></html>"""
open(out, 'w').write(html)
print(out, len(html) / 1e6, 'MB')
