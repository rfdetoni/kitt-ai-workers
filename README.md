## AI Workers v0.1.75 — Agent CLI v0.87.29 semantic integration

Pin shared Agent CLI revision `cb530c2ecddaafa1241e957c3d379ea853f43863` (v0.87.29) in Evolution/Evals locks, and validate all uv locks in CI. No new runtime or generative-model dependency. [Release notes](docs/RELEASE_0.1.75.md).

## AI Workers 0.1.74 — no automatic WebChat capture replay

Evals and Evolution now pin Agent CLI **0.87.28** at `f5eaff224b80c02ceaaf390bc3b84e0943d95abf`, which blocks ambiguous submitted browser turns pending operator inspection rather than resending a potentially completed unseen KAP response. Python package versions and affected locks are synchronized. [Release details](docs/RELEASE_0.1.74.md).

## AI Workers 0.1.73 — Agent live planning feedback compatibility

Evals/Evolution pin Agent CLI **0.87.27** at `33c83bbb6b05d06ea4dc91020ac9d7e2f78dfed3`, including truthful planning/review TUI stage and elapsed provider wait. Package metadata and all uv locks are synchronized. [Release note](docs/RELEASE_0.1.73.md).

## AI Workers 0.1.72 — Agent contract reviewer convergence

Evals/Evolution now pin Agent CLI **0.87.26** at `cea70a4227b3ba66455ef968cddcbc3468f65e61`, keeping planner FINAL criteria/dependencies independent of per-task verifications and preventing repeated REVISE loops on complex missions. All package versions and uv locks are synchronized. [Release note](docs/RELEASE_0.1.72.md).

## AI Workers 0.1.71 — independently routed specialist models

Evals and Evolution now pin Agent CLI **0.87.25** at `4138895c84b673c8dfef54ddb8f7276ee4ca1eb4`, which supports per-worker TaskRouter model policies, direct providers and reverse-proxy instances with privacy-filtered failovers. Python package versions and all affected uv locks are aligned. See [release notes](docs/RELEASE_0.1.71.md).

## AI Workers 0.1.70 — specialist Agent compatibility

Evals and Evolution pin Agent CLI **0.87.23** at `4e643b11f00902d7afc7ee2e6315b4724cfec4f4`, adding the declarative multi-agent profiles and host-governed messaging. Root/package versions and Python locks are synchronized; worker runtime behavior is unchanged. See [release notes](docs/RELEASE_0.1.70.md).

## AI Workers 0.1.69 — indexed Agent CLI consumer pins

Evals/Evolution now pin Agent CLI 0.87.22 (`7a010b2dfba3e3356b7b49aeb32186b69605df7f`) for targeted graph updates and indexed lexical routing; project and uv.lock versions are synchronized. [Release notes](docs/RELEASE_0.1.69.md).

## AI Workers 0.1.68 — Agent CLI 0.87.21 consumer alignment

Evals and Evolution now consume Agent CLI 0.87.21 (`872c7f89d6a9dcce8e014b9141ee507fb9d234e3`) with nonblocking SQLite index reconciliation. Package metadata and uv.lock are synchronized; STT and wire contracts are unchanged. [Release notes](docs/RELEASE_0.1.68.md).

## AI Workers 0.1.67 — guarded vector memory consumer pins

Evals and Evolution now pin Agent CLI 0.87.20 at immutable commit `bae99751b082523bc3d44bc26f249f085a25fc3a`, allowing concurrent-memory updates and bounded durable-source vector backfill with Memory 0.10.2. Workspace versions and uv locks are aligned. No change to STT or the shared Protocol. [Release notes](docs/RELEASE_0.1.67.md).

## AI Workers 0.1.66 — hybrid-memory Agent pin

The Evals and Evolution Python consumers now pin Agent CLI **0.87.19** at immutable SHA `5d6f6b2ac4a10826ab7b551694146928e06f2023`, enabling optional local Ollama vector-memory search when paired with kitt-memory 0.10.0. Their package versions and uv locks are synchronized; no worker, protocol or runtime behavior is changed. See [release notes](docs/RELEASE_0.1.66.md).

## AI Workers 0.1.65 — aligned evaluation and evolution consumers

The Evals and Evolution Python locks now consume Agent CLI 0.87.18 at immutable commit `7d8e821352964addb9ab25acef8aa9f96f3461f6`; the base workers package and both optional packages are versioned 0.1.65. Worker NDJSON, STT, and Protocol semantics are unchanged. See [release notes](docs/RELEASE_0.1.65.md).

## AI Workers 0.1.64 / Evals + Evolution 0.1.61 — KAP/2 host-tool bridge

Pins Agent CLI **0.87.13** at commit `d50e3fe6aa4258fa24e2c69645968f6c845c18a0` to deliver canonical KAP/2 `K2 T` host-tool requests in durable Goals. All other Protocol and native dependencies retain their existing versions.

## AI Workers 0.1.63 / Evals + Evolution 0.1.60 — Goals KAP/2 host-action contract

The Python consumer pins Agent CLI **0.87.12** at immutable SHA `4b955a82633fccc4ba6ffef3c97703b1dfda0916`, which requires authorized host-tool execution before a durable Goals K2 F completion report. The update does not change Protocol 0.13.3, the assistant native runtime or any host permissions.

## AI Workers 0.1.62 / Evals + Evolution 0.1.59 — compact KAP/2 locks

Root and subpackage uv locks pin Protocol 0.13.3 and Agent CLI 0.87.11.
These versions add an explicit indentation-free KAP/2 structured final
for long plans. No AI Worker execution or security behavior changes.
See [release 0.1.62](docs/RELEASE_0.1.62.md).

## AI Workers 0.1.61 / Evals + Evolution 0.1.58 — KAP/2 Python lock alignment

Python locks now resolve Agent CLI **0.87.10** with the restricted KAP/2
`sandbox.python` operation and Protocol **0.13.2**. This corrects stale
Evals/Evolution development lock revisions without changing worker runtime
behavior. See [release 0.1.61](docs/RELEASE_0.1.61.md).

## 0.1.60 — Protocol 0.13.1 lock

Worker dependencies are synchronized with KAP/2 SDK hardening; existing worker IPC remains unchanged.

## 0.1.59 — shared KAP/2 protocol lock

The worker environment is pinned to Protocol 0.12.1. Existing worker IPC/JSON behavior is unchanged.

## Contract sync 0.1.58

Update the shared kitt-protocol SDK pin to 0.12.0 for compact KAP/2 structured final decoding. Worker service and existing IPC JSON contracts remain unchanged.

## Release 0.1.57 — Structured Agent result composition

Workers, Evals and Evolution locks align Agent 0.85.0 and Protocol 0.10.0. No worker execution behavior or new dependency is introduced. See [release notes](docs/RELEASE_0.1.57.md).

# K.I.T.T. AI Workers

## Release 0.1.56 — WebChat token ownership alignment

Evals and Evolution locks select Agent CLI 0.84.10, which delegates reverse-proxy input/output token limits to WebChat.

See [release notes](docs/RELEASE_0.1.56.md).

## Release 0.1.55 — Local-only STT fallback

The openai-whisper fallback resolves an existing checkpoint path when local_files_only is enabled and fails before invoking its download-capable loader when absent. CPU retries preserve the faster-whisper local-only and worker/thread options. Workers, Evals and Evolution align their Agent and Protocol locks with this ecosystem release.

See [release notes](docs/RELEASE_0.1.55.md).

## Release 0.1.54 — Agent CLI 0.84.8 alignment

AI Workers, Evals and Evolution now lock Agent CLI **0.84.8** revision `809151b40ef4600c8364c73583bd38717b1665cf`. This carries the durable-contract live-progress and bounded memory-context behavior into evaluation/evolution environments. Worker behavior and shared Protocol remain unchanged. See [release notes](docs/RELEASE_0.1.54.md).

## Release 0.1.53 — Agent CLI 0.84.7 alignment

AI Workers, Evals and Evolution now lock Agent CLI **0.84.7** revision `f9c07452dd211359e754c2b9a1eb54e3854c41a1`. This carries the first-prompt TUI visibility fix into evaluation/evolution environments. Worker behavior and shared Protocol remain unchanged. See [release notes](docs/RELEASE_0.1.53.md).

## Release 0.1.52 — Agent CLI 0.84.6 alignment

AI Workers, Evals and Evolution now lock Agent CLI **0.84.6** revision `0f14d68b5fbdd6848660f68707230d7d6c3db584`. This carries the complete Goals/TaskPlan verification-ownership correction into evaluation/evolution environments. Worker behavior and shared Protocol remain unchanged. See [release notes](docs/RELEASE_0.1.52.md).

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

### Release 0.1.76: local multilingual lexical resources

AI Workers 0.1.76 aligns root, Evolution and Evals uv locks with Agent CLI 0.87.30 immutable main SHA 4736660981d3d07f8a29adda4127b652d82e9229. This is a dependency alignment only; offline semantic lexicon is opt-in and does not add a mandatory Ollama, NLP library or corpus dependency. [Release notes](docs/RELEASE_0.1.76.md).
