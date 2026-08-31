from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import json, uuid

@dataclass(frozen=True)
class Request:
    capability: str
    payload: dict[str, Any]
    id: str = ""
    def __post_init__(self):
        if not self.id: object.__setattr__(self,"id",str(uuid.uuid4()))

@dataclass(frozen=True)
class Response:
    id: str
    ok: bool
    payload: dict[str, Any]
    error: str | None = None

def encode(value: Request | Response) -> str:
    return json.dumps(asdict(value), ensure_ascii=False, separators=(",",":"))

def decode_request(line: str) -> Request:
    data=json.loads(line); return Request(id=str(data.get("id") or ""),capability=str(data["capability"]),payload=dict(data.get("payload") or {}))
