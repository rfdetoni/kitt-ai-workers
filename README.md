# K.I.T.T. AI Workers

<p align="center">
  <strong>Isolated AI/ML workloads, evaluation and staged self-evolution for K.I.T.T.</strong><br>
  On-demand workers · local STT · Evolution · Evals · bounded NDJSON execution
</p>

<p align="center">
  <a href="https://github.com/rfdetoni/kitt-ai-workers/blob/main/LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Isolation" src="https://img.shields.io/badge/execution-on--demand-6f42c1">
</p>

K.I.T.T. AI Workers keeps heavyweight or experiment-oriented AI capabilities outside long-lived Agent and Assistant processes. The base worker protocol stays lightweight, while optional STT dependencies and separately packaged Evolution/Evals capabilities are loaded only when the workload needs them.

---

## What’s included

- Dependency-light NDJSON worker protocol and runner.
- On-demand process isolation for ML/compute workloads.
- Local OpenAI-compatible speech-to-text server.
- Optional `faster-whisper` STT backend.
- `kitt-evolution`: staged offline skill-evolution engine.
- `kitt-evals`: evaluation corpora, retrieval benchmarks and external-eval bridges.
- Parent-process lifecycle supervision for spawned workers.
- Shared integration with K.I.T.T. Protocol and Agent CLI.

---

## Quick links

- **K.I.T.T. ecosystem:** https://github.com/rfdetoni/kitt
- **Agent CLI:** https://github.com/rfdetoni/kitt-agent-cli
- **Assistant:** https://github.com/rfdetoni/kitt-assistant
- **Protocol:** https://github.com/rfdetoni/kitt-protocol
- **Manual:** [MANUAL.md](MANUAL.md)
- **Security:** [SECURITY.md](SECURITY.md)

---

## Architecture

```text
kitt-ai-workers
│
├── kitt_workers/
│   ├── protocol.py       bounded worker messages
│   ├── runner.py         on-demand NDJSON runner
│   └── stt_server.py     local OpenAI-compatible STT
│
└── packages/
    ├── kitt-evolution/   staged skill evolution
    └── kitt-evals/       corpora, retrieval evals and bridges
```

The architecture keeps CUDA/PyTorch/Whisper-class dependencies out of resident services unless explicitly requested.

---

## Requirements & installation

The base `kitt-ai-workers` package supports Python **3.10+** and depends on the shared K.I.T.T. protocol package.

Install the base package for development:

```bash
python -m pip install -e .
```

Install local STT support only when required:

```bash
python -m pip install -e '.[stt]'
```

`kitt-evolution` is a separate Python 3.12+ package under `packages/kitt-evolution`; `kitt-evals` is also packaged separately. The root K.I.T.T. installer composes these packages with the Agent instead of vendoring them into `kitt-agent-cli`.

---

## NDJSON worker execution

Run a lightweight health task over stdio:

```bash
printf '{"id":"1","capability":"health","payload":{}}\n' \
  | python3 -m kitt_workers.runner
```

Example response:

```json
{"id":"1","ok":true,"payload":{"status":"ok"},"error":null}
```

Workers are intended to be spawned for a bounded task and exit rather than keeping heavyweight runtimes resident indefinitely.

---

## Local speech-to-text

Start the local OpenAI-compatible STT server:

```bash
kitt-stt --port 8000 --model base
```

Equivalent module invocation:

```bash
python3 -m kitt_workers.stt_server --port 8000 --model base
```

`kitt-assistant` can supervise the STT process when voice input needs it. A supervised worker can receive `--parent-stdin-lifecycle`, causing it to terminate when the owning Assistant process goes away.

---

## Evolution

`packages/kitt-evolution` owns offline, staged self-evolution for K.I.T.T. skills. Its responsibilities include datasets, constraints, egress controls, optimization, persistent run state and promotion workflows.

From a composed K.I.T.T. installation, the Agent exposes workflows such as:

```bash
kitt evolve runs
kitt evolve skill <skill-name>
kitt evolve promote <run-id>
```

Evolution is intentionally **not** an automatic live-code replacement mechanism. Candidates are generated and evaluated first; promotion remains explicit.

---

## Evals

`packages/kitt-evals` provides reusable evaluation support including corpora, retrieval evaluation and bridges for external evaluation tooling such as Inspect and Promptfoo.

This separation allows K.I.T.T. to measure retrieval, prompts and evolved skills without adding evaluation dependencies to the Agent’s normal execution path.

---

## Performance & isolation

The core principle is simple: expensive runtimes should not inflate idle K.I.T.T. memory usage.

- The base worker protocol uses small stdio messages.
- Heavy dependencies are optional.
- Workers are created on demand and can terminate with their owner.
- Evaluation/evolution packages are separate from the normal Agent hot path.
- Resident services remain focused on orchestration rather than model-runtime hosting.

---

## Security

Worker input is an execution boundary. Capabilities should be explicitly enumerated and payloads validated before dispatch. Evolution additionally applies constraints and egress controls so evaluation or optimization data does not silently cross privacy boundaries.

Process isolation reduces blast radius, but callers remain responsible for deciding which workloads and files a worker is authorized to access.

---

## Testing

Base workers:

```bash
pytest
# or
python3 -m unittest discover tests
```

The package-specific test suites under `packages/kitt-evolution` and `packages/kitt-evals` should also be run when changing those components.

---

## Contributing

Keep the base worker runtime small. Heavy dependencies should remain optional and workload-specific; experiments and evaluation tooling should not leak into the Agent’s steady-state hot path.

---

## K.I.T.T. ecosystem

| Repository | Responsibility |
| --- | --- |
| [`kitt`](https://github.com/rfdetoni/kitt) | installer and ecosystem composition |
| [`kitt-agent-cli`](https://github.com/rfdetoni/kitt-agent-cli) | autonomous agent control plane |
| [`kitt-reverse-proxy`](https://github.com/rfdetoni/kitt-reverse-proxy) | authorized provider gateway |
| [`kitt-protocol`](https://github.com/rfdetoni/kitt-protocol) | shared contracts and SDKs |
| [`kitt-memory`](https://github.com/rfdetoni/kitt-memory) | persistent memory engine |
| [`kitt-toolbox`](https://github.com/rfdetoni/kitt-toolbox) | native code/system data plane |
| [`kitt-assistant`](https://github.com/rfdetoni/kitt-assistant) | resident assistant and Control Center |

---

## License

MIT. See [LICENSE](LICENSE).
