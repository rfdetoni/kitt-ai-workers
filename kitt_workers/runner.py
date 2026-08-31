from __future__ import annotations
import sys
from .protocol import Response, decode_request, encode

def handle_echo(payload: dict) -> dict: return {"value": payload.get("value")}
HANDLERS={"echo":handle_echo,"health":lambda _: {"status":"ok"}}

def main() -> int:
    for line in sys.stdin:
        line=line.strip()
        if not line: continue
        try:
            req=decode_request(line); handler=HANDLERS.get(req.capability)
            if handler is None: raise ValueError(f"unsupported capability: {req.capability}")
            out=Response(req.id,True,handler(req.payload))
        except Exception as exc:
            req_id=locals().get("req").id if "req" in locals() else "unknown"
            out=Response(req_id,False,{},str(exc))
        sys.stdout.write(encode(out)+"\n"); sys.stdout.flush()
    return 0

if __name__=="__main__": raise SystemExit(main())
