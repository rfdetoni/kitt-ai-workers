# KITT AI Workers

On-demand Python workers for capabilities that benefit from the Python ML ecosystem. The base package has **zero runtime dependencies** and does not keep a Python process resident when KITT is idle.

v0.1 provides the worker protocol/supervisor contract and a deterministic echo worker for end-to-end lifecycle tests. Heavy STT/TTS/Vision dependencies are intentionally not installed until their corresponding capability is enabled (YAGNI).

```bash
python -m unittest discover tests
printf '{"id":"1","capability":"health","payload":{}}\n' | python -m kitt_workers.runner
```
