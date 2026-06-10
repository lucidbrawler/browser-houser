#!/usr/bin/env python3
"""
Simple HTTP server for serving the built Astro dashboard (dist/).

Run this after `npm run build`.

Why this exists:
- The dashboard uses plain ws:// targets for Local / LAN / Public.
- Modern browsers block ws:// connections when the page itself is served over https://
  (mixed content blocking). This is not a CORS problem.
- COOP/COEP headers (Cross-Origin-Opener-Policy + Cross-Origin-Embedder-Policy)
  are for cross-origin isolation (SharedArrayBuffer etc.) and are unrelated to WebSockets.
  Adding them can break asset loading.

Usage:
    python serve.py            # serves on :8000 (prefers ./dist if present)
    python serve.py 3000       # custom port

Then open http://<ip-or-hostname>:<port> in a browser.
From that http:// page the ws:// Public and LAN targets are allowed.

For a real public HTTPS dashboard + working Public target you will eventually
need to front the warthog node's /stream with TLS (wss://).
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import os
import sys


class DashboardRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Permissive CORS (harmless for a static dashboard, useful if you ever
        # add fetch() calls or want to load the page in certain embedded contexts).
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

        # Intentionally NOT setting:
        #   Cross-Origin-Opener-Policy: same-origin
        #   Cross-Origin-Embedder-Policy: require-corp
        # Those are for cross-origin isolation and will likely cause you pain
        # (images, fonts, or other resources may stop loading).

        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        # Respond to CORS preflight requests
        self.send_response(204)
        self.end_headers()

    def log_message(self, format, *args):
        # Quieter logging
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

    # Prefer serving the Astro production build if it exists
    if os.path.isdir("dist"):
        os.chdir("dist")
        print(f"[serve] Serving built dashboard from ./dist on port {port}")
    else:
        print(f"[serve] Serving current directory on port {port}")

    print("[serve] IMPORTANT: Access the page using http:// (not https://)")
    print("[serve] Only http:// pages are allowed to open ws:// WebSocket targets.")
    print("[serve] Press Ctrl-C to stop.\n")

    test(DashboardRequestHandler, HTTPServer, port=port)
