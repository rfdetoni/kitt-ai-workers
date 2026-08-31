from __future__ import annotations

from io import BytesIO
import unittest

from kitt_protocol import Envelope, WORKER_EXECUTE_REQUEST, WORKER_EXECUTE_RESPONSE, SYSTEM_ERROR
from kitt_workers.runner import run_stream


class WorkerProtocolTest(unittest.TestCase):
    def _run(self, envelope: Envelope) -> Envelope:
        stdin = BytesIO(envelope.dumps().encode() + b"\n")
        stdout = BytesIO()
        self.assertEqual(0, run_stream(stdin, stdout))
        return Envelope.loads(stdout.getvalue().strip())

    def test_health_is_correlated(self):
        req = Envelope(
            kind=WORKER_EXECUTE_REQUEST,
            payload={"capability": "health", "payload": {}},
            id="worker-1",
        )
        response = self._run(req)
        self.assertEqual(WORKER_EXECUTE_RESPONSE, response.kind)
        self.assertEqual("worker-1", response.correlation_id)
        self.assertEqual("ok", response.payload["payload"]["status"])

    def test_wrong_kind_is_rejected(self):
        req = Envelope(kind="legacy.worker", payload={}, id="legacy")
        response = self._run(req)
        self.assertEqual(SYSTEM_ERROR, response.kind)
        self.assertEqual("worker_request_failed", response.payload["code"])

    def test_oversized_line_is_bounded(self):
        stdin = BytesIO(b"x" * (256 * 1024 + 10) + b"\n")
        stdout = BytesIO()
        run_stream(stdin, stdout)
        response = Envelope.loads(stdout.getvalue().strip())
        self.assertEqual(SYSTEM_ERROR, response.kind)
        self.assertEqual("worker_frame_too_large", response.payload["code"])


if __name__ == "__main__":
    unittest.main()
