# AI Workers v0.1.75 — Agent CLI lock alignment

- Bump root worker and Evolution/Evals Python package versions to `0.1.75`.
- Refresh Evolution/Evals uv locks to Agent CLI `0.87.29` at exact main SHA `cb530c2ecddaafa1241e957c3d379ea853f43863`.
- Root uv lock tracks worker dependencies only and its editable package version; Agent is not a root direct dependency.
- Enforce `uv lock --check` in CI for all three files. Python 3.14 regression gates remain.
- Protocol, toolbox, memory, and reverse-proxy are not changed because no public consumer contract was added.
