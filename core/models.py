"""
Pydantic models for Agent Court.
"""

from pydantic import BaseModel
from typing import Literal


class Source(BaseModel):
    title: str
    url: str
    snippet: str
    domain: str


class Argument(BaseModel):
    side: Literal["FOR", "AGAINST"]
    headline_claim: str
    key_points: list[str]
    sources: list[Source]
    full_report: str


class RubricScore(BaseModel):
    evidence_quality: int
    logical_coherence: int
    argument_completeness: int
    rebuttal_strength: int

    @property
    def total(self) -> int:
        return (
            self.evidence_quality +
            self.logical_coherence +
            self.argument_completeness +
            self.rebuttal_strength
        )


class Verdict(BaseModel):
    winner: Literal["FOR", "AGAINST", "DRAW"]
    for_scores: RubricScore
    against_scores: RubricScore
    judge_reasoning: str
    closing_summary: str