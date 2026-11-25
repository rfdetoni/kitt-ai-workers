"""Reproducible worker transport benchmark; no LLM or external service required."""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import tracemalloc

from kitt_protocol import Envelope, WORKER_EXECUTE_REQUEST, WORKER_EXECUTE_RESPONSE
from kitt_workers.runner import run_stream


class _Requests:
    def __init__(self, jobs, payload_bytes):
        self.remaining = jobs
        self.frame = Envelope(
            kind=WORKER_EXECUTE_REQUEST,
            payload={"capability": "echo", "payload": {"value": "x" * payload_bytes}},
            id="benchmark",
        ).dumps().encode() + b"\n"
        self.started = 0

    def readline(self, limit):
        if not self.remaining:
            return b""
        self.remaining -= 1
        self.started = time.perf_counter_ns()
        return self.frame[:limit]


class _Results:
    def __init__(self, source):
        self.source = source
        self.latencies = []
        self.bytes = 0

    def write(self, raw):
        # Verify actual protocol output before measuring the next request.
        result = Envelope.loads(raw.rstrip(b"\r\n"))
        if result.kind != WORKER_EXECUTE_RESPONSE or result.correlation_id != "benchmark":
            raise RuntimeError("worker benchmark received invalid response")
        self.latencies.append((time.perf_counter_ns() - self.source.started) / 1e6)
        self.bytes += len(raw)
        return len(raw)

    def flush(self):
        pass


def run(jobs=1000, payload_bytes=4096):
    if not 1 <= jobs <= 10000 or not 1 <= payload_bytes <= 65536:
        raise ValueError("benchmark jobs/payload outside bounded range")
    source = _Requests(jobs, payload_bytes)
    sink = _Results(source)
    tracemalloc.start()
    start_cpu = time.process_time()
    start = time.perf_counter()
    try:
        code = run_stream(source, sink, max_jobs=jobs)
        elapsed = time.perf_counter() - start
        cpu = time.process_time() - start_cpu
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    if code != 0 or len(sink.latencies) != jobs:
        raise RuntimeError("benchmark did not finish all requested jobs")
    ordered = sorted(sink.latencies)
    rss = None
    try:
        import resource
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != "darwin":
            rss *= 1024
    except ImportError:
        pass
    return {
        "benchmark": "worker_echo_protocol",
        "jobs": jobs,
        "payload_bytes": payload_bytes,
        "wall_seconds": elapsed,
        "cpu_seconds": cpu,
        "jobs_per_second": jobs / max(elapsed, 1e-9),
        "latency_p50_ms": statistics.median(ordered),
        "latency_p95_ms": ordered[max(0, (95 * jobs + 99) // 100 - 1)],
        "python_peak_bytes": peak,
        "process_peak_rss_bytes": rss,
        "response_bytes": sink.bytes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=1000)
    parser.add_argument("--payload-bytes", type=int, default=4096)
    args = parser.parse_args()
    print(json.dumps(run(args.jobs, args.payload_bytes), sort_keys=True))


if __name__ == "__main__":
    main()
