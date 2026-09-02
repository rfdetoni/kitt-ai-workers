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
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

_WHISPER_MODEL_INSTANCE: Any = None
_ENGINE_NAME: str = "none"
_SERVER_MODEL_NAME: str | None = None

_MAX_REQUEST_BYTES = 26 * 1024 * 1024
_CLIENT_READ_TIMEOUT_SECONDS = 15.0

_TRANSCRIPTION_LOCK = threading.Lock()
_REQUESTS_TOTAL = 0
_FAILURES_TOTAL = 0
_LAST_TRANSCRIPTION_MS = 0

# Tuning options configured at startup
_STT_DEVICE = "auto"
_STT_COMPUTE_TYPE = "default"
_STT_CPU_THREADS = 0
_STT_NUM_WORKERS = 1
_STT_BEAM_SIZE = 2
_STT_LOCAL_FILES_ONLY = True
_STT_VAD_FILTER = True
_STT_VAD_MIN_SILENCE_MS = 300
_STT_VAD_SPEECH_PAD_MS = 220
_STT_NO_SPEECH_THRESHOLD = 0.6


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


def _browser_origin_forbidden(origin: str | None) -> bool:
    """The STT endpoint is machine-to-machine; browsers must not drive it."""
    return origin is not None


def _env_port(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not 1 <= value <= 65535:
        raise ValueError(f"{name} must be between 1 and 65535")
    return value


def _shutdown_on_parent_stdin_eof(server: ThreadingHTTPServer, stream: Any) -> None:
    """Stop a supervised worker when the parent closes its stdin pipe."""
    try:
        stream.read()
    finally:
        server.shutdown()


def _detect_stt_device(
    requested_device: str = "auto",
    requested_compute: str = "default",
) -> tuple[str, str]:
    """Detect available hardware acceleration and compute type.

    If 'auto' or 'cuda' is requested:
    - Tests for CTranslate2 / PyTorch GPU acceleration.
    - If functional, uses GPU acceleration ('cuda' with 'float16'/'default').
    - If unavailable or on initialization error, gracefully falls back to 'cpu' with 'float32'.
    """
    req_dev = (requested_device or "auto").strip().lower()
    req_comp = (requested_compute or "default").strip().lower()

    if req_dev == "cpu":
        return "cpu", "float32" if req_comp == "default" else req_comp

    # 1. Probe CTranslate2 CUDA support
    try:
        import ctranslate2
        cuda_count = ctranslate2.get_cuda_device_count()
        if cuda_count > 0:
            supported = ctranslate2.get_supported_compute_types("cuda")
            compute = "float16" if ("float16" in supported and req_comp == "default") else req_comp
            print(
                f"[STT] GPU acceleration detected: CTranslate2 CUDA ({cuda_count} device(s), compute_type={compute})",
                flush=True,
            )
            return "cuda", compute
    except Exception as exc:
        if req_dev == "cuda":
            print(f"[STT] GPU check failed for CUDA ({exc}). Falling back to CPU.", flush=True)

    # 2. Probe PyTorch CUDA / MPS support as secondary check
    try:
        import torch
        if torch.cuda.is_available() and torch.cuda.device_count() > 0:
            compute = "float16" if req_comp == "default" else req_comp
            print(
                f"[STT] GPU acceleration detected: PyTorch CUDA ({torch.cuda.device_count()} device(s), compute_type={compute})",
                flush=True,
            )
            return "cuda", compute
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            compute = "float32" if req_comp == "default" else req_comp
            print(f"[STT] GPU acceleration detected: Apple Silicon MPS (compute_type={compute})", flush=True)
            return "mps", compute
    except Exception:
        pass

    # 3. CPU fallback
    compute = "float32" if req_comp == "default" else req_comp
    if req_dev == "cuda":
        print("[STT] Warning: GPU ('cuda') was requested but no functional CUDA device was found. Falling back to CPU.", flush=True)
    else:
        print(f"[STT] Hardware acceleration: No supported GPU found. Using CPU (device=cpu, compute_type={compute}).", flush=True)

    return "cpu", compute


def get_whisper_engine(
    model_name: str,
    device: str = "auto",
    compute_type: str = "default",
    cpu_threads: int = 0,
    num_workers: int = 1,
    local_files_only: bool = True,
):
    global _WHISPER_MODEL_INSTANCE, _ENGINE_NAME
    if _WHISPER_MODEL_INSTANCE is not None:
        return _WHISPER_MODEL_INSTANCE

    target_device, target_compute = _detect_stt_device(device, compute_type)

    try:
        from faster_whisper import WhisperModel

        print(
            f"[STT] Loading local faster-whisper model: '{model_name}' "
            f"(device={target_device}, compute_type={target_compute}, "
            f"cpu_threads={cpu_threads}, num_workers={num_workers}, "
            f"local_files_only={local_files_only})...",
            flush=True,
        )
        kwargs: dict[str, Any] = {
            "device": target_device,
            "compute_type": target_compute,
            "num_workers": max(1, num_workers),
        }
        if cpu_threads > 0:
            kwargs["cpu_threads"] = cpu_threads
        if local_files_only:
            kwargs["local_files_only"] = True

        try:
            _WHISPER_MODEL_INSTANCE = WhisperModel(model_name, **kwargs)
        except Exception as exc:
            if target_device != "cpu":
                print(
                    f"[STT] Faster-Whisper initialization failed on '{target_device}': {exc}. "
                    f"Retrying on CPU...",
                    flush=True,
                )
                kwargs["device"] = "cpu"
                kwargs["compute_type"] = "float32"
                _WHISPER_MODEL_INSTANCE = WhisperModel(model_name, **kwargs)
            elif local_files_only and ("not found" in str(exc).lower() or "local_files_only" in str(exc).lower()):
                print(f"[STT] Local file lookup for model '{model_name}' failed with local_files_only=True: {exc}", flush=True)
                raise
            else:
                _WHISPER_MODEL_INSTANCE = WhisperModel(model_name, device="cpu", compute_type="float32")

        _ENGINE_NAME = f"faster-whisper ({model_name})"
        actual_device = getattr(getattr(_WHISPER_MODEL_INSTANCE, "model", None), "device", target_device)
        print(f"[STT] Local faster-whisper model ready on device '{actual_device}'.", flush=True)
        return _WHISPER_MODEL_INSTANCE
    except ImportError:
        pass

    try:
        import whisper

        print(f"[STT] Loading local openai-whisper model: '{model_name}' (device={target_device})...", flush=True)
        try:
            _WHISPER_MODEL_INSTANCE = whisper.load_model(model_name, device=target_device if target_device != "auto" else None)
        except Exception as exc:
            if target_device != "cpu":
                print(f"[STT] OpenAI-Whisper initialization failed on '{target_device}': {exc}. Retrying on CPU...", flush=True)
                _WHISPER_MODEL_INSTANCE = whisper.load_model(model_name, device="cpu")
            else:
                raise
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


def _clean_transcript(text: str) -> str:
    text = text.strip()
    cleaned = text.replace(".", "").replace("…", "").replace("-", "").strip().lower()
    if not cleaned or cleaned in ("[música]", "[som]", "(silêncio)", "(música)"):
        return ""
    return text


def transcribe_audio_file(
    audio_path: str,
    model_name: str,
    language: str | None = None,
    initial_prompt: str | None = None,
    beam_size: int | None = None,
    vad_filter: bool | None = None,
    vad_min_silence_ms: int | None = None,
    vad_speech_pad_ms: int | None = None,
    no_speech_threshold: float | None = None,
    return_metadata: bool = False,
) -> str | dict[str, Any]:
    global _REQUESTS_TOTAL, _FAILURES_TOTAL, _LAST_TRANSCRIPTION_MS
    start_time = time.perf_counter()

    if not os.path.isfile(audio_path):
        return {"text": "", "language": None, "language_probability": None, "avg_logprob": None, "duration_ms": 0} if return_metadata else ""

    model_name = (model_name or "").strip()
    if not model_name:
        raise ValueError("STT model must be configured explicitly")

    engine = get_whisper_engine(
        model_name,
        device=_STT_DEVICE,
        compute_type=_STT_COMPUTE_TYPE,
        cpu_threads=_STT_CPU_THREADS,
        num_workers=_STT_NUM_WORKERS,
        local_files_only=_STT_LOCAL_FILES_ONLY,
    )
    if engine is None:
        if return_metadata:
            return {"text": "", "language": None, "language_probability": None, "avg_logprob": None, "duration_ms": 0}
        return ""

    prompt = (initial_prompt or "").strip() or None
    b_size = beam_size if beam_size is not None else _STT_BEAM_SIZE
    v_filter = vad_filter if vad_filter is not None else _STT_VAD_FILTER
    v_min_silence = vad_min_silence_ms if vad_min_silence_ms is not None else _STT_VAD_MIN_SILENCE_MS
    v_speech_pad = vad_speech_pad_ms if vad_speech_pad_ms is not None else _STT_VAD_SPEECH_PAD_MS
    ns_thresh = no_speech_threshold if no_speech_threshold is not None else _STT_NO_SPEECH_THRESHOLD

    _REQUESTS_TOTAL += 1
    try:
        if _ENGINE_NAME.startswith("faster-whisper"):
            segments, info = engine.transcribe(
                audio_path,
                language=language,
                beam_size=b_size,
                vad_filter=v_filter,
                vad_parameters={
                    "min_silence_duration_ms": v_min_silence,
                    "speech_pad_ms": v_speech_pad,
                },
                condition_on_previous_text=False,
                initial_prompt=prompt,
                no_speech_threshold=ns_thresh,
            )
            segments_list = list(segments)
            clean_text = _clean_transcript(" ".join(seg.text for seg in segments_list))
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            _LAST_TRANSCRIPTION_MS = duration_ms

            detected_lang = getattr(info, "language", None)
            lang_prob = getattr(info, "language_probability", None)
            avg_logprob = None
            if segments_list:
                logprobs = [getattr(s, "avg_logprob", None) for s in segments_list if getattr(s, "avg_logprob", None) is not None]
                if logprobs:
                    avg_logprob = sum(logprobs) / len(logprobs)

            if return_metadata:
                return {
                    "text": clean_text,
                    "language": detected_lang,
                    "language_probability": lang_prob,
                    "avg_logprob": avg_logprob,
                    "duration_ms": duration_ms,
                }
            return clean_text

        if _ENGINE_NAME.startswith("whisper"):
            kwargs = {
                "language": language,
                "condition_on_previous_text": False,
            }
            if prompt:
                kwargs["initial_prompt"] = prompt
            result = engine.transcribe(audio_path, **kwargs)
            clean_text = _clean_transcript(str(result.get("text", "")))
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            _LAST_TRANSCRIPTION_MS = duration_ms

            if return_metadata:
                return {
                    "text": clean_text,
                    "language": result.get("language"),
                    "language_probability": None,
                    "avg_logprob": None,
                    "duration_ms": duration_ms,
                }
            return clean_text

    except Exception:
        _FAILURES_TOTAL += 1
        raise

    return {"text": "", "language": None, "language_probability": None, "avg_logprob": None, "duration_ms": 0} if return_metadata else ""


def _parse_multipart(
    content_type_header: str,
    body: bytes,
) -> tuple[bytes | None, str | None, str | None, str | None]:
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
    prompt: str | None = None

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
            elif 'name="prompt"' in cd:
                val = part.get_payload(decode=True)
                if val:
                    prompt = val.decode("utf-8", errors="ignore").strip()[:512]

    return file_bytes, language, model, prompt


class LocalSTTRequestHandler(BaseHTTPRequestHandler):
    server_version = "KITT-Local-STT/1"
    sys_version = ""

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(_CLIENT_READ_TIMEOUT_SECONDS)

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _send_json(self, status: int, data: dict, headers: dict[str, str] | None = None) -> None:
        body = json.dumps(data, separators=(",", ":")).encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if headers:
                for k, v in headers.items():
                    self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self) -> None:
        if self.path in ("/", "/health", "/v1/health"):
            ready = _engine_ready()
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "ok" if ready else "degraded",
                    "ready": ready,
                    "busy": _TRANSCRIPTION_LOCK.locked(),
                    "service": "kitt-local-stt",
                    "engine": _ENGINE_NAME,
                    "model": _SERVER_MODEL_NAME,
                    "requests_total": _REQUESTS_TOTAL,
                    "failures_total": _FAILURES_TOTAL,
                    "last_transcription_ms": _LAST_TRANSCRIPTION_MS,
                },
            )
            return
        if self.path in ("/v1/models", "/models"):
            data = []
            if _SERVER_MODEL_NAME:
                data.append(
                    {
                        "id": _SERVER_MODEL_NAME,
                        "object": "model",
                        "owned_by": "local-whisper",
                    }
                )
            self._send_json(
                HTTPStatus.OK,
                {
                    "object": "list",
                    "data": data,
                },
            )
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/v1/audio/transcriptions":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        if _browser_origin_forbidden(self.headers.get("Origin")):
            self._send_json(
                HTTPStatus.FORBIDDEN,
                {"error": "browser-originated requests are forbidden"},
            )
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

        file_data, language, _requested_model, prompt = _parse_multipart(
            content_type,
            body,
        )
        if not file_data:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "missing 'file' field in multipart payload"},
            )
            return

        # Attempt to acquire transcription lock; reject with 429 if busy
        acquired = _TRANSCRIPTION_LOCK.acquire(blocking=True, timeout=0.1)
        if not acquired:
            self._send_json(
                HTTPStatus.TOO_MANY_REQUESTS,
                {"error": "STT engine is busy processing another transcription"},
                headers={"Retry-After": "1"},
            )
            return

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(file_data)

        try:
            if not _SERVER_MODEL_NAME:
                raise RuntimeError("STT server model is not configured")
            result = transcribe_audio_file(
                tmp_path,
                model_name=_SERVER_MODEL_NAME,
                language=language,
                initial_prompt=prompt,
                return_metadata=True,
            )
            if isinstance(result, dict):
                self._send_json(HTTPStatus.OK, result)
            else:
                self._send_json(HTTPStatus.OK, {"text": result})
        except Exception as exc:
            print(f"[STT] transcription failed: {exc}", file=sys.stderr, flush=True)
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "transcription failed"},
            )
        finally:
            _TRANSCRIPTION_LOCK.release()
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def run_stt_server(
    model: str,
    host: str = "127.0.0.1",
    port: int = 8000,
    parent_stdin_lifecycle: bool = False,
    device: str = "auto",
    compute_type: str = "default",
    cpu_threads: int = 0,
    num_workers: int = 1,
    beam_size: int = 2,
    local_files_only: bool = True,
    vad_filter: bool = True,
    vad_min_silence_ms: int = 300,
    vad_speech_pad_ms: int = 220,
    no_speech_threshold: float = 0.6,
) -> None:
    global _SERVER_MODEL_NAME, _STT_DEVICE, _STT_COMPUTE_TYPE, _STT_CPU_THREADS, _STT_NUM_WORKERS, _STT_BEAM_SIZE, _STT_LOCAL_FILES_ONLY, _STT_VAD_FILTER, _STT_VAD_MIN_SILENCE_MS, _STT_VAD_SPEECH_PAD_MS, _STT_NO_SPEECH_THRESHOLD
    host = _validate_loopback_host(host)
    if not 1 <= int(port) <= 65535:
        raise ValueError("STT port must be between 1 and 65535")
    model = (model or "").strip()
    if not model:
        raise ValueError("STT model cannot be empty")
    _SERVER_MODEL_NAME = model
    _STT_DEVICE = device
    _STT_COMPUTE_TYPE = compute_type
    _STT_CPU_THREADS = cpu_threads
    _STT_NUM_WORKERS = num_workers
    _STT_BEAM_SIZE = beam_size
    _STT_LOCAL_FILES_ONLY = local_files_only
    _STT_VAD_FILTER = vad_filter
    _STT_VAD_MIN_SILENCE_MS = vad_min_silence_ms
    _STT_VAD_SPEECH_PAD_MS = vad_speech_pad_ms
    _STT_NO_SPEECH_THRESHOLD = no_speech_threshold

    get_whisper_engine(
        model,
        device=device,
        compute_type=compute_type,
        cpu_threads=cpu_threads,
        num_workers=num_workers,
        local_files_only=local_files_only,
    )

    server = ThreadingHTTPServer((host, int(port)), LocalSTTRequestHandler)
    if parent_stdin_lifecycle:
        threading.Thread(
            target=_shutdown_on_parent_stdin_eof,
            args=(server, sys.stdin.buffer),
            name="kitt-stt-parent-lifecycle",
            daemon=True,
        ).start()
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
        default=os.environ.get("KITT_STT_HOST", "127.0.0.1"),
        help="Loopback bind host only (default: KITT_STT_HOST or 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=_env_port("KITT_STT_PORT", 8000),
        help="Bind port (default: KITT_STT_PORT or 8000)",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("KITT_WHISPER_MODEL") or os.environ.get("WHISPER_MODEL"),
        help="Required model name/path (or set KITT_WHISPER_MODEL / WHISPER_MODEL)",
    )
    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Device to run inference on (auto, cpu, cuda)",
    )
    parser.add_argument(
        "--compute-type",
        default="default",
        choices=["default", "int8", "float16", "int8_float16", "float32"],
        help="Compute type for model weights and inference",
    )
    parser.add_argument(
        "--cpu-threads",
        type=int,
        default=0,
        help="Number of CPU threads for inference (0 = auto)",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=1,
        help="Number of worker threads in engine",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=2,
        help="Beam size for decoding (default: 2)",
    )
    parser.add_argument(
        "--local-files-only",
        action="store_true",
        default=True,
        help="Do not attempt remote downloads on wake (default: True)",
    )
    parser.add_argument(
        "--allow-download",
        action="store_false",
        dest="local_files_only",
        help="Allow remote download if model is not present locally",
    )
    parser.add_argument(
        "--vad-filter",
        action="store_true",
        default=True,
        help="Enable VAD filtering",
    )
    parser.add_argument(
        "--no-vad-filter",
        action="store_false",
        dest="vad_filter",
        help="Disable VAD filtering",
    )
    parser.add_argument(
        "--vad-min-silence-ms",
        type=int,
        default=300,
        help="VAD minimum silence duration in ms",
    )
    parser.add_argument(
        "--vad-speech-pad-ms",
        type=int,
        default=220,
        help="VAD speech padding in ms",
    )
    parser.add_argument(
        "--no-speech-threshold",
        type=float,
        default=0.6,
        help="Threshold to consider a segment silent",
    )
    parser.add_argument(
        "--parent-stdin-lifecycle",
        action="store_true",
        help="Exit when the supervising parent closes stdin",
    )
    args = parser.parse_args()
    if not args.model or not args.model.strip():
        parser.error(
            "--model is required unless KITT_WHISPER_MODEL or WHISPER_MODEL is set"
        )

    try:
        run_stt_server(
            model=args.model,
            host=args.host,
            port=args.port,
            parent_stdin_lifecycle=args.parent_stdin_lifecycle,
            device=args.device,
            compute_type=args.compute_type,
            cpu_threads=args.cpu_threads,
            num_workers=args.num_workers,
            beam_size=args.beam_size,
            local_files_only=args.local_files_only,
            vad_filter=args.vad_filter,
            vad_min_silence_ms=args.vad_min_silence_ms,
            vad_speech_pad_ms=args.vad_speech_pad_ms,
            no_speech_threshold=args.no_speech_threshold,
        )
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
