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

Execute requests by streaming JSON requests to stdin:

```bash
# Health check probe
printf '{"id":"1","capability":"health","payload":{}}\n' | python -m kitt_workers.runner
```

Output:
```json
{"id":"1","ok":true,"payload":{"status":"ok"},"error":null}
```

---

## 🧪 Testing

```bash
python -m unittest discover tests
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE).
