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

    def test_worker_can_exit_after_bounded_number_of_jobs(self):
        first = Envelope(
            kind=WORKER_EXECUTE_REQUEST,
            payload={"capability": "health", "payload": {}},
            id="worker-1",
        )
        second = Envelope(
            kind=WORKER_EXECUTE_REQUEST,
            payload={"capability": "health", "payload": {}},
            id="worker-2",
        )
        stdin = BytesIO(
            first.dumps().encode() + b"\n"
            + second.dumps().encode() + b"\n"
        )
        stdout = BytesIO()
        self.assertEqual(0, run_stream(stdin, stdout, max_jobs=1))
        lines = [line for line in stdout.getvalue().splitlines() if line]
        self.assertEqual(1, len(lines))
        response = Envelope.loads(lines[0])
        self.assertEqual("worker-1", response.correlation_id)


class WorkerBenchmarkTest(unittest.TestCase):
    def test_metrics_report_verified_correlated_responses(self):
        from kitt_workers.benchmark import run

        result = run(20, 128)
        self.assertEqual(result["jobs"], 20)
        self.assertGreater(result["response_bytes"], 20 * 128)
        self.assertGreater(result["jobs_per_second"], 0)
        self.assertGreater(result["python_peak_bytes"], 0)
        self.assertGreaterEqual(result["latency_p95_ms"], result["latency_p50_ms"])
        with self.assertRaises(ValueError):
            run(10001, 128)


if __name__ == "__main__":
    unittest.main()
