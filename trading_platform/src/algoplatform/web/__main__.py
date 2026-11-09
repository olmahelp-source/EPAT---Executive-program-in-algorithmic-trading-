import argparse

from .server import serve

ap = argparse.ArgumentParser(description="algoplatform web UI")
ap.add_argument("--host", default="127.0.0.1", help="bind address (keep 127.0.0.1 unless behind TLS + auth proxy)")
ap.add_argument("--port", type=int, default=8080)
a = ap.parse_args()
serve(a.host, a.port)
