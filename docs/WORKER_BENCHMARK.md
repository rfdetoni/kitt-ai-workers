# Worker resource benchmark

Run `python -m kitt_workers.benchmark --jobs 1000 --payload-bytes 4096`.
The benchmark exercises the real JSON envelope decode/dispatch/encode path
with a generated echo workload, verifies every response and retains only
latency samples. Reports wall/CPU time, throughput, p50/p95 latency,
Python allocation peak (tracemalloc) and OS process peak RSS where available.
RSS includes interpreter startup; tracemalloc adds measurement overhead.
CI records a small bounded run without flaky absolute performance gates.
This is a protocol microbenchmark, not LLM inference, GPU or remote engine
performance. Compare identical hardware, interpreter and job sizes.
