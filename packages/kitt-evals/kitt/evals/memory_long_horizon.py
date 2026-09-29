"""Long-horizon context benchmark for structured compaction and progressive recall."""
from __future__ import annotations

from dataclasses import dataclass

from kitt.compaction.service import CompactionService
from kitt.context_filter.prompt_budget import TokenCounter


@dataclass(frozen=True)
class LongMemoryCase:
    name: str
    needle: str
    section: str


CASES = (
    LongMemoryCase("architecture decision", "Use SQLite WAL for the local ledger", "constraints_and_decisions"),
    LongMemoryCase("failure correction", "ERROR migration 6 failed on PRAGMA", "errors_and_corrections"),
    LongMemoryCase("affected file", "src/runtime/router.py", "affected_artifacts"),
    LongMemoryCase("pending work", "TODO add concurrency regression test", "pending_work"),
    LongMemoryCase("validation", "pytest integration suite passed", "validation_state"),
)


def _transcript(noise_lines: int = 800) -> str:
    facts = [
        "Goal: harden the KITT runtime without changing user-facing semantics",
        "Decision: Use SQLite WAL for the local ledger",
        "ERROR migration 6 failed on PRAGMA",
        "Fixed migration by moving the PRAGMA outside the transaction",
        "src/runtime/router.py changed",
        "TODO add concurrency regression test",
        "pytest integration suite passed",
    ]
    noise = [f"routine diagnostic line {index}: no material state change" for index in range(noise_lines)]
    insertion_points = [0, 113, 271, 419, 577, 701, len(noise)]
    out = list(noise)
    for offset, fact in reversed(list(zip(insertion_points, facts))):
        out.insert(min(offset, len(out)), fact)
    return "\n".join(out)


def run_long_memory_eval(noise_lines: int = 800) -> dict:
    raw = _transcript(noise_lines)
    narrative = CompactionService._deterministic_summary(raw)
    state = CompactionService._working_state(raw, narrative, [])
    state_dict = state.to_dict()

    details = []
    hits = 0
    for case in CASES:
        values = state_dict.get(case.section, [])
        haystack = "\n".join(str(value) for value in values)
        ok = case.needle.casefold() in haystack.casefold()
        hits += int(ok)
        details.append(
            {
                "case": case.name,
                "section": case.section,
                "needle": case.needle,
                "ok": ok,
            }
        )

    before = TokenCounter.count_tokens(raw)
    rendered = state.render()
    after = TokenCounter.count_tokens(rendered)
    return {
        "cases": len(CASES),
        "recall": round(hits / max(1, len(CASES)), 4),
        "tokens_before": before,
        "tokens_after": after,
        "retained_ratio": round(after / max(1, before), 4),
        "details": details,
    }


def main() -> int:
    import json

    print(json.dumps(run_long_memory_eval(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
