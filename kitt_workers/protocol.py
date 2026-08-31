from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kitt_protocol import (
    Envelope,
    ProtocolError,
    WORKER_EXECUTE_REQUEST,
    WORKER_EXECUTE_RESPONSE,
)

MAX_WORKER_FRAME_BYTES = 256 * 1024


@dataclass(frozen=True)
class WorkerRequest:
    capability: str
    payload: dict[str, Any]


def decode_request(raw: bytes | str) -> tuple[Envelope, WorkerRequest]:
    encoded = raw.encode("utf-8") if isinstance(raw, str) else raw
    if len(encoded) > MAX_WORKER_FRAME_BYTES:
        raise ProtocolError("worker_frame_too_large")
    envelope = Envelope.loads(encoded)
    if envelope.kind != WORKER_EXECUTE_REQUEST:
        raise ProtocolError(f"unexpected worker envelope kind: {envelope.kind}")
    if envelope.correlation_id is not None:
        raise ProtocolError("worker request cannot have correlation_id")
    if not isinstance(envelope.payload, dict):
        raise ProtocolError("worker request payload must be an object")
    capability = envelope.payload.get("capability")
    payload = envelope.payload.get("payload", {})
    if not isinstance(capability, str) or not capability.strip():
        raise ProtocolError("worker capability is required")
    if not isinstance(payload, dict):
        raise ProtocolError("worker capability payload must be an object")
    return envelope, WorkerRequest(capability=capability, payload=payload)


def success(request_id: str, payload: dict[str, Any]) -> Envelope:
    return Envelope.response(
        WORKER_EXECUTE_RESPONSE,
        request_id,
        {"payload": payload},
    )


def failure(request_id: str | None, code: str, message: str) -> Envelope:
    return Envelope.error(request_id, code, message)


def encode_line(envelope: Envelope) -> bytes:
    return envelope.dumps().encode("utf-8") + b"\n"
