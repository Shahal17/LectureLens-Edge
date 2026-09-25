"""Small local-only HTTP server for LectureLens Edge."""

from __future__ import annotations

import argparse
import json
import threading
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .lecture_engine import LectureEngine
from .runtime import detect_runtime


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = PROJECT_ROOT / "app"
ENGINE = LectureEngine()


class LectureLensHandler(SimpleHTTPRequestHandler):
    server_version = "LectureLensEdge/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_ROOT), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[LectureLens] {self.address_string()} - {fmt % args}")

    def _json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 1_000_000:
            raise ValueError("Invalid request size.")
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json(
                {
                    "status": "ready",
                    "local_only": True,
                    "runtime": detect_runtime().to_dict(),
                    "engine_version": ENGINE.version,
                }
            )
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/analyze":
                result = ENGINE.analyze(
                    str(payload.get("transcript", "")),
                    str(payload.get("title", "Untitled lecture")),
                    str(payload.get("subject", "General")),
                )
                self._json(result)
                return
            if path == "/api/ask":
                result = ENGINE.answer(
                    str(payload.get("transcript", "")),
                    str(payload.get("question", "")),
                )
                self._json(result)
                return
            self._json({"error": "Unknown API route."}, HTTPStatus.NOT_FOUND)
        except (ValueError, json.JSONDecodeError) as exc:
            self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except Exception:
            self._json({"error": "Unexpected local processing error."}, HTTPStatus.INTERNAL_SERVER_ERROR)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LectureLens Edge locally")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: local device only)")
    parser.add_argument("--port", type=int, default=8765, help="Port (default: 8765)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open a browser automatically")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), LectureLensHandler)
    url = f"http://{args.host}:{args.port}"
    print(f"LectureLens Edge is ready at {url}")
    print("All processing stays on this computer. Press Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping LectureLens Edge.")
    finally:
        server.server_close()
