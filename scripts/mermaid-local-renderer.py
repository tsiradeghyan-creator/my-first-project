#!/usr/bin/env python3
"""Local stand-in for mermaid.ink, for places where mermaid.ink is unreachable (Cloud proxy).

Serves /svg/pako:<data> and /img/pako:<data>?type=png by running the local `mmdc`
(@mermaid-js/mermaid-cli). Point cli-anything-mermaid at it:

    python3 scripts/mermaid-local-renderer.py &            # listens on 127.0.0.1:8765
    export MERMAID_RENDERER_URL=http://127.0.0.1:8765

Chromium for mmdc: set PUPPETEER_CONFIG to a puppeteer config JSON with executablePath
(on Cloud: /root/.puppeteerrc.json, written by scripts/install-cli-anything.sh).
"""
import base64
import json
import os
import subprocess
import sys
import tempfile
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, unquote

PORT = int(os.environ.get("MERMAID_LOCAL_PORT", "8765"))
PUPPETEER_CONFIG = os.environ.get("PUPPETEER_CONFIG", os.path.expanduser("~/.puppeteerrc.json"))


def decode(token: str) -> str:
    token = unquote(token)
    if token.startswith("pako:"):
        raw = token[5:]
        raw += "=" * (-len(raw) % 4)
        state = json.loads(zlib.decompress(base64.urlsafe_b64decode(raw)))
        return state["code"]
    raw = token + "=" * (-len(token) % 4)
    return base64.urlsafe_b64decode(raw).decode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        parts = url.path.strip("/").split("/", 1)
        if len(parts) != 2 or parts[0] not in ("svg", "img"):
            self.send_error(404)
            return
        fmt = "svg" if parts[0] == "svg" else ("png" if "type=png" in url.query or not url.query else "png")
        try:
            code = decode(parts[1])
        except Exception as exc:  # noqa: BLE001
            self.send_error(400, f"bad diagram payload: {exc}")
            return
        with tempfile.TemporaryDirectory() as tmp:
            src, out = os.path.join(tmp, "d.mmd"), os.path.join(tmp, f"d.{fmt}")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(code)
            cmd = ["mmdc", "-i", src, "-o", out, "-b", "white"]
            if os.path.exists(PUPPETEER_CONFIG):
                cmd += ["-p", PUPPETEER_CONFIG]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if proc.returncode != 0 or not os.path.exists(out):
                self.send_error(500, (proc.stderr or "mmdc failed")[:300])
                return
            data = open(out, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml" if fmt == "svg" else "image/png")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"mermaid local renderer on http://127.0.0.1:{PORT}", file=sys.stderr)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
