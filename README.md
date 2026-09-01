# KITT AI Workers

> Out-of-process, on-demand AI and ML execution protocol foundation for KITT.

Provides a lightweight, dependency-free foundation for executing machine learning, vision, and compute workloads on demand via standard input/output line-delimited JSON (NDJSON).

---

## 🎯 Architecture & Philosophy

- **Zero-Dependency Base**: The core runner and protocol require only standard Python library modules (`json`, `sys`, `unittest`).
- **Non-Resident**: Workers are spawned strictly on demand and terminate immediately after processing their workload.
- **Process Isolation**: Prevents heavy CUDA / PyTorch runtimes from inflating resident memory of background daemons.

---

## 🚀 Usage

### 1. Stdio NDJSON Worker Tasks

Execute requests by streaming JSON requests to stdin:

```bash
# Health check probe
printf '{"id":"1","capability":"health","payload":{}}\n' | python3 -m kitt_workers.runner
```

Sample output:
```json
{"id":"1","ok":true,"payload":{"status":"ok"},"error":null}
```

### 2. 100% Local STT (Whisper) Server

Install the STT extra once:

```bash
python3 -m pip install -e ".[stt]"
```

Then run the OpenAI-compatible local server on `127.0.0.1:8000`:

```bash
kitt-stt --port 8000 --model base
# equivalent:
python3 -m kitt_workers.stt_server --port 8000 --model base
```

`kitt-assistant` can start `kitt-stt` automatically when local voice STT is
required. A supervised worker receives `--parent-stdin-lifecycle` so it exits
when the Assistant that owns it terminates.

---

## 🧪 Testing

```bash
pytest
# or
python3 -m unittest discover tests
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE).
