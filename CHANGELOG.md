# Changelog — K.I.T.T. AI Workers

## Notas de versão migradas do README

## AI Workers 0.1.80 — Clean-Room Agent dependency alignment

Evals/Evolution locks pin Agent 0.88.10 and Protocol 0.14.1. [Release notes](docs/RELEASE_0.1.80.md).

## AI Workers 0.1.79 — Clean-Room ecosystem alignment

Locks Agent 0.88.9 and Protocol 0.14.1 for the Evals/Evolution consumers without adding new worker execution authority. [Release notes](docs/RELEASE_0.1.79.md).

## AI Workers / Evals / Evolution 0.1.78 — bounded Agent planning

Refresh the Evals and Evolution Agent locks to CLI 0.88.1. Consumers use one plan generation with local structural validation and retain post-execution verification. No worker protocol or third-party dependency change.

[Release details](docs/RELEASE_0.1.78.md).

## AI Workers / Evals / Evolution 0.1.77 — JSON ecosystem

Align Protocol and Agent locks with the JSON-only model wire migration. Workers continue to use typed host contracts; model-generated plans, validation, review and tool requests use the Agent CLI JSON pipeline. No KAP parser is imported by the application.


[Release details](docs/RELEASE_0.1.77.md).

## AI Workers v0.1.75 — Agent CLI v0.87.29 semantic integration

Pin shared Agent CLI revision `cb530c2ecddaafa1241e957c3d379ea853f43863` (v0.87.29) in Evolution/Evals locks, and validate all uv locks in CI. No new runtime or generative-model dependency. [Release notes](docs/RELEASE_0.1.75.md).

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

## Release 0.1.57 — Structured Agent result composition

Workers, Evals and Evolution locks align Agent 0.85.0 and Protocol 0.10.0. No worker execution behavior or new dependency is introduced. See [release notes](docs/RELEASE_0.1.57.md).

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

## Release 0.1.76: local multilingual lexical resources

AI Workers 0.1.76 aligns root, Evolution and Evals uv locks with Agent CLI 0.87.30 immutable main SHA 4736660981d3d07f8a29adda4127b652d82e9229. This is a dependency alignment only; offline semantic lexicon is opt-in and does not add a mandatory Ollama, NLP library or corpus dependency. [Release notes](docs/RELEASE_0.1.76.md).

---

## Histórico anterior do CHANGELOG

# AI Workers / Evals / Evolution 0.1.78 — bounded Agent planning

Refresh the Evals and Evolution Agent locks to CLI 0.88.1. Consumers use one plan generation with local structural validation and retain post-execution verification. No worker protocol or third-party dependency change.

[Release details](docs/RELEASE_0.1.78.md).

# AI Workers / Evals / Evolution 0.1.77 — JSON ecosystem

Align Protocol and Agent locks with the JSON-only model wire migration. Workers continue to use typed host contracts; model-generated plans, validation, review and tool requests use the Agent CLI JSON pipeline. No KAP parser is imported by the application.

## 0.1.65 — Agent performance consumer pins

- Align Evals/Evolution Agent CLI locks with 0.87.18 (`7d8e821352964addb9ab25acef8aa9f96f3461f6`).
- Bump workers and optional packages to 0.1.65; preserve existing Protocol, evaluation and worker behavior.

# Changelog

## 0.1.56 — 2026-10-08

Align Evals and Evolution locks with Agent CLI 0.84.10 for WebChat token ownership.

## 0.1.55 — 2026-10-07

The openai-whisper fallback resolves an existing checkpoint path when local_files_only is enabled and fails before invoking its download-capable loader when absent. CPU retries preserve the faster-whisper local-only and worker/thread options. Workers, Evals and Evolution align their Agent and Protocol locks with this ecosystem release.

## 0.1.43 — 2026-10-06

- Make retrieval ablations exercise graph-disabled, graph-enabled and lexical feature reranking stages before selection. Add a real indexed dependency-neighbor case, per-case latency/token costs and stage diagnostics. Replace misleading small-model/large-direct labels with `hybrid_graph_lexical_rerank` and `single_lexical_hit`. Synthetic lexical embeddings do not represent model quality. The fixture shows 5/6 structural versus 6/6 graph recall@5; lexical reranking remains optional and is not promoted.

## 0.1.42 — 2026-10-02

- Always release the STT transcription lock and clean up a created temporary file when file creation/write fails.
- Use Agent CLI's processing-locality predicate in Evolution: a loopback web proxy does not bypass local-only privacy policy.
- Align worker packages and Protocol/Agent consumers with the bounded gateway lifecycle release.

## 0.1.40 - 2026-09-30

- Follow KITT Protocol `main` for the base worker package instead of embedding a stale protocol commit SHA.
- Align base workers, Evolution and Evals on version 0.1.40 for the Agent CLI 0.80 / Protocol 0.5 ecosystem contract.
- Preserve the existing ownership boundary: workers provide isolated execution/evaluation while durable run coordination, memory and approval authority stay in their owning KITT components.

## 0.1.36 - 2026-09-29

- Pin Evolution/Evals to Agent CLI 0.78.6 (`24c104f76d1e2f10055c616bc8f34ad8776d3cd3`).
- Consume structural reverse-proxy tool schemas independently from prompt compaction.


## 0.1.35 - 2026-09-29

- Pin Evolution/Evals to Agent CLI 0.78.5 (`5315847b09dbe6d0ebbf3f7b714a1b6ceb1469b3`).
- Consume the compact staged reverse-proxy execution contract without duplicating prompt orchestration.


## 0.1.34 - 2026-09-29

- Pin Evolution/Evals to Agent CLI 0.78.4 (`7d56faec43fa6f5c0e4b1f63c0c18e269a0eb9d8`).
- Preserve the staged execution contract used by the promoted ecosystem snapshot.


## 0.1.33 - 2026-09-29

- Pin Evolution/Evals to Agent CLI 0.78.3 (`89a63da16368a59eac5eee185373bfbf89f516b1`).
- Keep the strict unused-symbol CI gate introduced in 0.1.32.
- Preserve the implemented worker surface without unsupported vision/OCR claims.


## 0.1.32 - 2026-09-28

- Pin Evolution/Evals to Agent CLI 0.78.2.
- Remove unsupported vision/OCR claims from worker documentation.
- Add Python unused-symbol/static checks to CI.
- Keep the base runner intentionally limited to implemented capabilities.

## 0.1.31 - 2026-09-28

- Pin Evolution and Evals to promoted KITT Agent CLI 0.78.1 (`fbc64cdd90d476773f1af081f864572a4cc72b7b`).
- Preserve Protocol 0.4.0 and existing worker/memory ownership boundaries.
- Keep the change dependency-only; no evaluation/evolution runtime contract is changed.

## 0.1.30 - 2026-09-28

- Pin Evolution and Evals to promoted KITT Agent CLI 0.78.0 (`f51dbba8a0506e90366ddb4e95026dc6c6614699`).
- Preserve Protocol 0.4.0 and worker/memory ownership boundaries.
- Keep the change dependency-only; no evaluation/evolution runtime contract is changed.

## 0.1.26 - 2026-09-28

- Pin base workers to KITT Protocol 0.4.0.
- Align Evolution/Evals with Agent CLI 0.76.0 and standalone kitt-memory authority.
- Keep workers free of direct durable-memory ownership.

## 0.1.25 - 2026-09-28

- Add evidence-backed reusable-experience generalization with episode lineage, success-rate and evidence-coverage metrics.
- Add long-horizon structured-compaction evaluation for decisions, corrections, artifacts, pending work and validation evidence.
- Pin base workers to KITT Protocol 0.3.0.
- Pin Evolution/Evals to KITT Agent CLI 0.75.1 portable-audio validation snapshot (`aee552caf0ef4fd7bd44b12a85e15e7df1febed4`).

## 0.1.24 - 2026-09-28

- Pin Evolution/Evals to the final KITT Agent CLI 0.74.6 revision after its Python 3.14 container and release-action alignment.
- Keep the Python 3.14+ support floor and KITT Protocol 0.2.1 base-worker pin unchanged.


## 0.1.23 - 2026-09-27

- Require Python 3.14+ across base workers, Evolution and Evals.
- Pin base workers to kitt-protocol 0.2.1.
- Pin Evolution/Evals to the final Agent CLI 0.74.5 dependency-alignment snapshot.


## 0.1.22 - 2026-09-27

- Align Evolution/Evals with the final KITT Agent CLI 0.74.4 consistency-hardening revision.
- Preserve the protocol 0.2.0 contract while consuming the Agent memory/approval fixes and Assistant 0.1.5 runtime pin.
- Keep the worker base decoupled from kitt-memory; shared-memory behavior remains owned by Agent/Assistant integrations.


## 0.1.21 - 2026-09-27

- Align Evolution/Evals with the validated kitt-agent-cli 0.74.3 Assistant/runtime pin.
- Keep kitt-protocol 0.2.0 aligned with the shared-memory schema-v4 ecosystem snapshot.

## 0.1.20 - 2026-09-27

- Align base workers with kitt-protocol 0.2.0.
- Align Evolution/Evals with kitt-agent-cli 0.74.2.
- Keep workers free of direct kitt-memory coupling while maintaining ecosystem pin coherence.

## 0.1.17 - 2026-09-25

- Pin Evolution and Evals to the final KITT Agent CLI 0.72.1 ecosystem-compatible revision.
- Keep immutable dependency metadata coherent with the frozen KITT ecosystem lock.


## 0.1.16 - 2026-09-25

- Align `kitt-evolution` and `kitt-evals` with the validated Agent CLI 0.72.0 revision.
- Keep worker/evaluation packages compatible with the ecosystem's current Agent control-plane snapshot.


## 0.1.0 - Unreleased

- Initial KITT ecosystem foundation.
