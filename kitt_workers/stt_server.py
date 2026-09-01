"""100% local Speech-to-Text (STT) HTTP server for the K.I.T.T. ecosystem.

The service is intentionally loopback-only and exposes the OpenAI-compatible
POST /v1/audio/transcriptions endpoint using faster-whisper or openai-whisper.
"""

from __future__ import annotations

import argparse
import email
import ipaddress
import json
import os
import sys
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

_WHISPER_MODEL_INSTANCE: Any = None
_ENGINE_NAME: str = "none"
_SERVER_MODEL_NAME: str = "base"

_MAX_REQUEST_BYTES = 26 * 1024 * 1024
_CLIENT_READ_TIMEOUT_SECONDS = 15.0


def _validate_loopback_host(host: str) -> str:
    value = (host or "").strip()
    if not value:
        raise ValueError("STT bind host is required")
    if value.lower() == "localhost":
        return "localhost"
    try:
        ip = ipaddress.ip_address(value.split("%", 1)[0])
    except ValueError as exc:
        raise ValueError("STT bind host must be localhost or a loopback IP") from exc
    if not ip.is_loopback:
        raise ValueError("STT server is local-only; non-loopback bind is forbidden")
    if ip.version != 4:
        raise ValueError("IPv6 loopback is not supported by this HTTPServer build")
    return value


def _validated_content_length(raw: str | None) -> int:
    if raw is None or not raw.strip():
        raise ValueError("Content-Length is required")
    try:
        size = int(raw)
    except ValueError as exc:
        raise ValueError("invalid Content-Length") from exc
    if size < 0:
        raise ValueError("invalid Content-Length")
    if size > _MAX_REQUEST_BYTES:
        raise OverflowError(f"request exceeds {_MAX_REQUEST_BYTES} bytes")
    return size


def get_whisper_engine(model_name: str = "base"):
    global _WHISPER_MODEL_INSTANCE, _ENGINE_NAME
    if _WHISPER_MODEL_INSTANCE is not None:
        return _WHISPER_MODEL_INSTANCE

    try:
        from faster_whisper import WhisperModel

        print(f"[STT] Loading local faster-whisper model: '{model_name}'...", flush=True)
        _WHISPER_MODEL_INSTANCE = WhisperModel(
            model_name,
            device="auto",
            compute_type="default",
        )
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

    _ENGINE_NAME = "unavailable"
    print(
        "[STT] Warning: neither 'faster-whisper' nor 'whisper' is installed. "
        "STT is unavailable until a local engine is installed.",
        flush=True,
    )
    return None


def _engine_ready() -> bool:
    return (
        _WHISPER_MODEL_INSTANCE is not None
        and (
            _ENGINE_NAME.startswith("faster-whisper")
            or _ENGINE_NAME.startswith("whisper")
        )
    )


def transcribe_audio_file(
    audio_path: str,
    model_name: str = "base",
    language: str | None = None,
) -> str:
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


def _parse_multipart(
    content_type_header: str,
    body: bytes,
) -> tuple[bytes | None, str | None, str | None]:
    """Parse multipart/form-data payload without the deprecated cgi module."""
    raw_message = (
        b"Content-Type: "
        + content_type_header.encode("latin-1")
        + b"\r\n\r\n"
        + body
    )
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
                    language = val.decode("utf-8", errors="ignore").strip()[:16]
            elif 'name="model"' in cd:
                val = part.get_payload(decode=True)
                if val:
                    model = val.decode("utf-8", errors="ignore").strip()[:128]

    return file_bytes, language, model


class LocalSTTRequestHandler(BaseHTTPRequestHandler):
    server_version = "KITT-Local-STT/1"
    sys_version = ""

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(_CLIENT_READ_TIMEOUT_SECONDS)

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _send_json(self, status: int, data: dict) -> None:
        body = json.dumps(data, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/", "/health", "/v1/health"):
            ready = _engine_ready()
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "ok" if ready else "degraded",
                    "ready": ready,
                    "service": "kitt-local-stt",
                    "engine": _ENGINE_NAME,
                    "model": _SERVER_MODEL_NAME,
                },
            )
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/v1/audio/transcriptions":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        if not _engine_ready():
            self._send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {"error": "local STT engine is unavailable"},
            )
            return

        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type.lower():
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "Expected multipart/form-data"},
            )
            return

        try:
            content_length = _validated_content_length(
                self.headers.get("Content-Length")
            )
        except OverflowError as exc:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": str(exc)})
            return
        except ValueError as exc:
            status = (
                HTTPStatus.LENGTH_REQUIRED
                if self.headers.get("Content-Length") is None
                else HTTPStatus.BAD_REQUEST
            )
            self._send_json(status, {"error": str(exc)})
            return

        try:
            body = self.rfile.read(content_length)
        except TimeoutError:
            self._send_json(
                HTTPStatus.REQUEST_TIMEOUT,
                {"error": "request body read timed out"},
            )
            return
        if len(body) != content_length:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "incomplete request body"},
            )
            return

        file_data, language, _requested_model = _parse_multipart(content_type, body)
        if not file_data:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "missing 'file' field in multipart payload"},
            )
            return

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(file_data)

        try:
            transcript = transcribe_audio_file(
                tmp_path,
                model_name=_SERVER_MODEL_NAME,
                language=language,
            )
            self._send_json(HTTPStatus.OK, {"text": transcript})
        except Exception as exc:
            print(f"[STT] transcription failed: {exc}", file=sys.stderr, flush=True)
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "transcription failed"},
            )
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def run_stt_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    model: str = "base",
) -> None:
    global _SERVER_MODEL_NAME
    host = _validate_loopback_host(host)
    if not 1 <= int(port) <= 65535:
        raise ValueError("STT port must be between 1 and 65535")
    model = (model or "").strip()
    if not model:
        raise ValueError("STT model cannot be empty")
    _SERVER_MODEL_NAME = model
    get_whisper_engine(model)

    server = HTTPServer((host, int(port)), LocalSTTRequestHandler)
    print(
        f"[STT] Local STT server listening on "
        f"http://{host}:{port}/v1/audio/transcriptions (100% local)",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[STT] Stopping local STT server...", flush=True)
    finally:
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(description="K.I.T.T. 100% Local STT Server")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Loopback bind host only (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Bind port (default: 8000)",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("WHISPER_MODEL", "base"),
        help="Whisper model loaded once at startup (tiny, base, small, medium)",
    )
    args = parser.parse_args()

    try:
        run_stt_server(host=args.host, port=args.port, model=args.model)
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
