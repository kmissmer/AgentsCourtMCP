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


class Verdict(BaseModel):
    winner: Literal["FOR", "AGAINST", "DRAW"]
    judge_reasoning: str
    closing_summary: str