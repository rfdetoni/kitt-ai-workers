# Changelog

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
