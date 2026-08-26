#!/usr/bin/env python3
"""
Dev server for the YarnAI page.

python3 -m http.server lets the browser cache index.html / styles.css /
motion.js, so edits silently don't appear and it looks like the animations
are broken. This sends no-store on everything.

Serves the project root regardless of where you run it from.

    python3 dev/serve.py          # http://localhost:8777
    python3 dev/serve.py 3000     # different port
"""
import sys
from functools import partial
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent.parent


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "304" not in (args[1] if len(args) > 1 else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8777
    print(f"YarnAI page  →  http://localhost:{port}   (no-cache, serving {ROOT})")
    ThreadingHTTPServer(("", port), partial(NoCacheHandler, directory=str(ROOT))).serve_forever()
