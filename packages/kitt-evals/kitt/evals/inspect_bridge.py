from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from kitt.evals.corpus import EvalTestCase


@dataclass(frozen=True)
class InspectEvalRecord:
    """Dependency-free representation that maps directly to Inspect samples."""

    id: str
    input: str
    target: str
    metadata: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def to_inspect_records(cases: Iterable[EvalTestCase]) -> list[InspectEvalRecord]:
    """Convert KITT corpus cases without importing Inspect AI."""
    records: list[InspectEvalRecord] = []
    for case in cases:
        records.append(
            InspectEvalRecord(
                id=case.id,
                input=case.prompt,
                target=case.expected_route,
                metadata={
                    "language": case.language,
                    "expected_intent": case.expected_intent,
                    "expected_complexity": case.expected_complexity,
                    "expected_risk": case.expected_risk,
                    "expected_paths": list(case.expected_paths),
                },
            )
        )
    return records


def inspect_available() -> bool:
    try:
        import inspect_ai  # type: ignore  # noqa: F401
        return True
    except (ImportError, ModuleNotFoundError):
        return False
