# K.I.T.T. AI Workers

## Release 0.1.51 — Agent CLI 0.84.5 loop alignment

AI Workers, Evals and Evolution now lock Agent CLI **0.84.5** revision `fc4646c98b2b55af8a992798440e079f8d3da124`. This carries the durable GOAL-contract completion-ownership correction into evaluation/evolution environments without changing worker behavior or shared Protocol contracts. See [release notes](docs/RELEASE_0.1.51.md).

## Release 0.1.50 — Agent CLI 0.84.4 alignment

AI Workers, Evals and Evolution now lock the validated Agent CLI **0.84.4** revision `fc985bc6d842d3c684ad1188ff2fc8a0c427e6a8`. No worker behavior or shared protocol changed; this is the minimal immutable-consumer alignment for the durable-loop hardening release. See [release notes](docs/RELEASE_0.1.50.md).

## Release 0.1.49 — Agent CLI 0.84.3 consumer alignment

Evolution and Evals now lock Agent CLI **0.84.3** at its validated main revision. Base worker, Evolution and Evals package metadata move together to **0.1.49**. Worker protocols and KITT Protocol remain unchanged.

## Release 0.1.48 — Agent CLI 0.84.2 consumer alignment

Evolution and Evals now lock Agent CLI **0.84.2** at its validated main revision. Base worker, Evolution and Evals package metadata move together to **0.1.48**. Worker protocols and KITT Protocol remain unchanged.

## Release 0.1.47 — Agent CLI 0.84.1 consumer alignment

Evolution and Evals now lock Agent CLI **0.84.1** at its validated main revision. Base worker, Evolution and Evals package metadata move together to **0.1.47**; worker and KITT Protocol contracts remain unchanged. See [release notes](docs/RELEASE_0.1.47.md).

## Release 0.1.46 — Agent CLI 0.84 consumer alignment

Evolution and Evals now lock Agent CLI **0.84.0** at its validated main revision. The base worker, Evolution and Evals package versions move together to **0.1.46**; worker protocols and KITT Protocol dependencies are unchanged. See [release notes](docs/RELEASE_0.1.46.md).

## Release 0.1.45 — unified model selection endpoint trust

Evolution and Evals lock Agent CLI 0.83.19, including the authenticated/pending and local/no-auth model picker correction. All three package/editable-lock versions agree at 0.1.45. See [release notes](docs/RELEASE_0.1.45.md).

## Release 0.1.44 — align the locked Agent consumer

Evolution and Evals now lock Agent CLI 0.83.18 at its validated main revision. Frozen environments include the managed Reverse Proxy endpoint-trust correction. All three worker package and editable-lock versions agree at 0.1.44; other dependencies and Protocol revisions remain unchanged. See [release notes](docs/RELEASE_0.1.44.md).

## Release 0.1.43 — execution boundary hardening

Make retrieval ablations exercise graph-disabled, graph-enabled and lexical feature reranking stages before selection. Add a real indexed dependency-neighbor case, per-case latency/token costs and stage diagnostics. Replace misleading small-model/large-direct labels with `hybrid_graph_lexical_rerank` and `single_lexical_hit`. Synthetic lexical embeddings do not represent model quality. The fixture shows 5/6 structural versus 6/6 graph recall@5; lexical reranking remains optional and is not promoted.

See [release notes](docs/RELEASE_0.1.43.md).

<p align="center">
  <strong>Isolated AI/ML workloads, evaluation and staged self-evolution for K.I.T.T.</strong><br>
  On-demand workers · local STT · Evolution · Evals · bounded NDJSON execution
</p>

<p align="center">
  <a href="https://github.com/rfdetoni/kitt-ai-workers/blob/main/LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white">
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

The base `kitt-ai-workers` package supports Python **3.14+** and depends on the shared K.I.T.T. protocol package.

Install the base package for development:

```bash
python -m pip install -e .
```

Install local STT support only when required:

```bash
python -m pip install -e '.[stt]'
```

`kitt-evolution` is a separate Python 3.14+ package under `packages/kitt-evolution`; `kitt-evals` is also packaged separately. Version 0.1.42 follows `kitt-agent-cli` and `kitt-protocol` `main`; the current validated lock baseline is Agent CLI 0.83.12 and Protocol 0.9.0. Evolution and Evals remain separately packaged, evidence-driven companions rather than live runtime authorities. The root K.I.T.T. installer composes these packages with the Agent instead of vendoring them into `kitt-agent-cli`.

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

## AI Workers 0.1.32 — ecosystem cleanup

Evolution and Evals pin Agent CLI 0.78.2. The base runner intentionally exposes only the implemented `health` and `echo` NDJSON capabilities; STT remains a separate local service. Vision/OCR is not advertised until a concrete worker capability exists.


## AI Workers 0.1.33 — Agent 0.78.3 alignment

Evolution and Evals pin Agent CLI 0.78.3 revision `89a63da16368a59eac5eee185373bfbf89f516b1`. The base worker contract remains intentionally narrow: NDJSON `health`/`echo`, separate STT service, and no advertised vision/OCR capability without an implementation.


## AI Workers 0.1.34 — Agent 0.78.4 alignment

Evolution and Evals pin Agent CLI 0.78.4 revision `7d56faec43fa6f5c0e4b1f63c0c18e269a0eb9d8`, including the staged reverse-proxy execution envelope and semantic/raw prompt deduplication.


## AI Workers 0.1.35 — Agent 0.78.5 staged prompt alignment

Evolution and Evals pin Agent CLI 0.78.5 revision `5315847b09dbe6d0ebbf3f7b714a1b6ceb1469b3`, consuming the compact reverse-proxy boundary and deterministic discovery/mutation/validation execution plan.


## AI Workers 0.1.36 — Agent 0.78.6 tool-schema alignment

Evolution and Evals pin Agent CLI 0.78.6 revision `24c104f76d1e2f10055c616bc8f34ad8776d3cd3`, where reverse-proxy tool schemas are transported structurally and no longer depend on textual prompt parsing.


## AI Workers 0.1.39 — Agent 0.78.7 runtime alignment

Evolution and Evals pin Agent CLI 0.78.7 revision `f06e4d6990228aae6283042e4c8b9d1092f4c58e`, including authoritative objective preservation and runtime identity diagnostics used by the updated ecosystem installer.


## AI Workers 0.1.39 — Agent 0.78.9 cancellation alignment

Evolution and Evals pin Agent CLI 0.78.9 revision `f06e4d6990228aae6283042e4c8b9d1092f4c58e`, including the Ctrl+C cancellation isolation fix and recoverable model-response flow.


## AI Workers 0.1.39 — main-first sibling dependencies

Evolution and Evals now depend on `kitt-agent-cli@main` instead of a cross-repository commit SHA. The ecosystem installer resolves sibling `main` branches together and records the exact installed SHAs as runtime provenance.
