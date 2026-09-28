"""Evidence-backed generalization of repeated task episodes into reusable experiences."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any, Iterable


_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]{2,}")


@dataclass(frozen=True)
class EpisodeTrace:
    id: str
    objective: str
    outcome: str
    actions: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    failure_signals: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReusableExperience:
    id: str
    signature: str
    objective_pattern: str
    successful_actions: tuple[str, ...]
    failure_signals: tuple[str, ...]
    supporting_episode_ids: tuple[str, ...]
    support_count: int
    success_count: int
    success_rate: float
    evidence_coverage: float
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "signature": self.signature,
            "objective_pattern": self.objective_pattern,
            "successful_actions": list(self.successful_actions),
            "failure_signals": list(self.failure_signals),
            "supporting_episode_ids": list(self.supporting_episode_ids),
            "support_count": self.support_count,
            "success_count": self.success_count,
            "success_rate": self.success_rate,
            "evidence_coverage": self.evidence_coverage,
            "confidence": self.confidence,
        }


class ExperienceGeneralizer:
    """Deterministic first-stage generalizer.

    It deliberately does not call an LLM. A model/worker can refine the bounded
    candidate later, but promotion decisions retain episode/evidence lineage.
    """

    SUCCESS_OUTCOMES = frozenset({"SUCCESS", "SUCCEEDED", "COMPLETED", "PASSED", "OUTCOME_SUPPORTED"})

    @staticmethod
    def _tokens(value: str) -> tuple[str, ...]:
        tokens = {
            token.casefold()
            for token in _WORD.findall(str(value or ""))
            if not token.isdigit()
        }
        return tuple(sorted(tokens))

    @classmethod
    def signature(cls, objective: str) -> str:
        tokens = cls._tokens(objective)
        stable = " ".join(tokens[:24])
        return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:20]

    @staticmethod
    def _rank(values: Iterable[str], limit: int) -> tuple[str, ...]:
        counts: dict[str, int] = {}
        originals: dict[str, str] = {}
        for value in values:
            clean = " ".join(str(value or "").split()).strip()
            if not clean:
                continue
            key = clean.casefold()
            counts[key] = counts.get(key, 0) + 1
            originals.setdefault(key, clean)
        ordered = sorted(counts, key=lambda key: (-counts[key], key))
        return tuple(originals[key] for key in ordered[:limit])

    @classmethod
    def generalize(
        cls,
        episodes: Iterable[EpisodeTrace],
        *,
        min_support: int = 2,
        min_success_rate: float = 0.60,
    ) -> list[ReusableExperience]:
        groups: dict[str, list[EpisodeTrace]] = {}
        for episode in episodes:
            signature = cls.signature(episode.objective)
            groups.setdefault(signature, []).append(episode)

        result: list[ReusableExperience] = []
        for signature, group in groups.items():
            if len(group) < max(2, int(min_support)):
                continue
            successful = [
                episode
                for episode in group
                if str(episode.outcome or "").upper() in cls.SUCCESS_OUTCOMES
            ]
            success_rate = len(successful) / len(group)
            if success_rate < max(0.0, min(float(min_success_rate), 1.0)):
                continue
            evidence_count = sum(bool(episode.evidence) for episode in group)
            evidence_coverage = evidence_count / len(group)
            support_factor = min(1.0, len(group) / 5.0)
            confidence = round(
                max(0.0, min(1.0, success_rate * 0.65 + evidence_coverage * 0.20 + support_factor * 0.15)),
                4,
            )
            objective_pattern = min(
                (" ".join(episode.objective.split()) for episode in group if episode.objective.strip()),
                key=lambda value: (len(value), value.casefold()),
                default="",
            )
            actions = cls._rank(
                action
                for episode in successful
                for action in episode.actions
            , 12)
            failures = cls._rank(
                signal
                for episode in group
                for signal in episode.failure_signals
            , 8)
            result.append(
                ReusableExperience(
                    id=f"exp_{signature}",
                    signature=signature,
                    objective_pattern=objective_pattern,
                    successful_actions=actions,
                    failure_signals=failures,
                    supporting_episode_ids=tuple(sorted(episode.id for episode in group)),
                    support_count=len(group),
                    success_count=len(successful),
                    success_rate=round(success_rate, 4),
                    evidence_coverage=round(evidence_coverage, 4),
                    confidence=confidence,
                )
            )
        return sorted(result, key=lambda item: (-item.confidence, -item.support_count, item.id))
