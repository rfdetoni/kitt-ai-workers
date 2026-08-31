"""100% Local Speech-to-Text (STT) HTTP Server for K.I.T.T. Ecosystem.

Binds exclusively to loopback (127.0.0.1:8000) and provides OpenAI-compatible
POST /v1/audio/transcriptions using local faster-whisper or whisper engine.
Python 3.12+ compatible (zero external dependencies required for base runner).
"""

from __future__ import annotations

import argparse
import email
import json
import os
import sys
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

_WHISPER_MODEL_INSTANCE: Any = None
_ENGINE_NAME: str = "none"


def get_whisper_engine(model_name: str = "base"):
    global _WHISPER_MODEL_INSTANCE, _ENGINE_NAME
    if _WHISPER_MODEL_INSTANCE is not None:
        return _WHISPER_MODEL_INSTANCE

    try:
        from faster_whisper import WhisperModel

        print(f"[STT] Loading local faster-whisper model: '{model_name}'...", flush=True)
        _WHISPER_MODEL_INSTANCE = WhisperModel(model_name, device="auto", compute_type="default")
        _ENGINE_NAME = f"faster-whisper ({model_name})"
        print("[STT] Local faster-whisper model ready.", flush=True)
        return _WHISPER_MODEL_INSTANCE
    except ImportError:
        pass

    try:
        import whisper

        print(f"[STT] Loading local openai-whisper model: '{model_name}'...", flush=True)
        _WHISPER_MODEL_INSTANCE = whisper.load_model(model_name)
        _ENGINE_NAME = f"whisper ({model_name})"
        print("[STT] Local whisper model ready.", flush=True)
        return _WHISPER_MODEL_INSTANCE
    except ImportError:
        pass

    _ENGINE_NAME = "mock"
    print("[STT] Notice: neither 'faster-whisper' nor 'whisper' installed. Using fallback mock STT.", flush=True)
    return None


def transcribe_audio_file(audio_path: str, model_name: str = "base", language: str | None = None) -> str:
    if not os.path.isfile(audio_path):
        return ""

    engine = get_whisper_engine(model_name)
    if engine is None:
        return ""

    if _ENGINE_NAME.startswith("faster-whisper"):
        segments, _ = engine.transcribe(audio_path, language=language, beam_size=5)
        return " ".join(seg.text for seg in segments).strip()

    if _ENGINE_NAME.startswith("whisper"):
        result = engine.transcribe(audio_path, language=language)
        return str(result.get("text", "")).strip()

    return ""


def _parse_multipart(content_type_header: str, body: bytes) -> tuple[bytes | None, str | None, str | None]:
    """Parse multipart/form-data payload without deprecated cgi module."""
    raw_message = b"Content-Type: " + content_type_header.encode("latin-1") + b"\r\n\r\n" + body
    msg = email.message_from_bytes(raw_message)

    file_bytes: bytes | None = None
    language: str | None = None
    model: str | None = None

    if msg.is_multipart():
        for part in msg.get_payload():
            cd = part.get("Content-Disposition", "")
            if 'name="file"' in cd:
                file_bytes = part.get_payload(decode=True)
            elif 'name="language"' in cd:
                val = part.get_payload(decode=True)
                if val:
                    language = val.decode("utf-8", errors="ignore").strip()
            elif 'name="model"' in cd:
                val = part.get_payload(decode=True)
                if val:
                    model = val.decode("utf-8", errors="ignore").strip()

    return file_bytes, language, model


class LocalSTTRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _send_json(self, status: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/health", "/v1/health"):
            self._send_json(HTTPStatus.OK, {
                "status": "ok",
                "service": "kitt-local-stt",
                "engine": _ENGINE_NAME,
            })
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self):
        if not self.path.startswith("/v1/audio/transcriptions"):
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Expected multipart/form-data"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        file_data, language, model = _parse_multipart(content_type, body)
        if not file_data:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "missing 'file' field in multipart payload"})
            return

        model_name = model or os.environ.get("WHISPER_MODEL", "base")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(file_data)

        try:
            transcript = transcribe_audio_file(tmp_path, model_name=model_name, language=language)
            self._send_json(HTTPStatus.OK, {"text": transcript})
        except Exception as exc:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def run_stt_server(host: str = "127.0.0.1", port: int = 8000, model: str = "base"):
    get_whisper_engine(model)
    server = HTTPServer((host, port), LocalSTTRequestHandler)
    print(f"[STT] Local STT server listening on http://{host}:{port}/v1/audio/transcriptions (100% local)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[STT] Stopping local STT server...", flush=True)
    finally:
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(description="K.I.T.T. 100% Local STT Server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    parser.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "base"), help="Whisper model (tiny, base, small, medium)")
    args = parser.parse_args()

    run_stt_server(host=args.host, port=args.port, model=args.model)
    return 0


if __name__ == "__main__":
    sys.exit(main())
