from __future__ import annotations

import os
import sys
from typing import BinaryIO

from .protocol import (
    MAX_WORKER_FRAME_BYTES,
    decode_request,
    encode_line,
    failure,
    success,
)


def handle_echo(payload: dict) -> dict:
    return {"value": payload.get("value")}


HANDLERS = {
    "echo": handle_echo,
    "health": lambda _: {"status": "ok"},
}


def _drain_oversized_line(stream: BinaryIO) -> None:
    while True:
        chunk = stream.readline(MAX_WORKER_FRAME_BYTES + 1)
        if not chunk or chunk.endswith(b"\n"):
            return


def run_stream(
    stdin: BinaryIO,
    stdout: BinaryIO,
    *,
    max_jobs: int = 0,
) -> int:
    completed_jobs = 0
    max_jobs = max(0, int(max_jobs))
    while True:
        raw = stdin.readline(MAX_WORKER_FRAME_BYTES + 1)
        if not raw:
            return 0
        if len(raw) > MAX_WORKER_FRAME_BYTES:
            if not raw.endswith(b"\n"):
                _drain_oversized_line(stdin)
            stdout.write(
                encode_line(
                    failure(None, "worker_frame_too_large", "worker request exceeds frame limit")
                )
            )
            stdout.flush()
            completed_jobs += 1
            if max_jobs and completed_jobs >= max_jobs:
                return 0
            continue
        if not raw.strip():
            continue

        request_id: str | None = None
        try:
            envelope, request = decode_request(raw.rstrip(b"\r\n"))
            request_id = envelope.id
            handler = HANDLERS.get(request.capability)
            if handler is None:
                raise ValueError(f"unsupported capability: {request.capability}")
            out = success(request_id, handler(request.payload))
        except Exception as exc:
            out = failure(request_id, "worker_request_failed", str(exc))

        stdout.write(encode_line(out))
        stdout.flush()
        completed_jobs += 1
        if max_jobs and completed_jobs >= max_jobs:
            return 0


def _configured_max_jobs() -> int:
    raw = os.getenv("KITT_WORKER_MAX_JOBS", "0").strip()
    if not raw:
        return 0
    try:
        return max(0, int(raw))
    except ValueError:
        return 0


def main() -> int:
    return run_stream(
        sys.stdin.buffer,
        sys.stdout.buffer,
        max_jobs=_configured_max_jobs(),
    )


if __name__ == "__main__":
    raise SystemExit(main())
