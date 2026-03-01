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
    # Name of the side/agent that produced this argument.  Marcus always
    # argues for the first option mentioned in the topic; Colton takes the
    # second.  This used to be "FOR"/"AGAINST" but has since been
    # generalized.
    side: Literal["Marcus", "Colton"]
    headline_claim: str
    key_points: list[str]
    sources: list[Source]
    full_report: str


class Verdict(BaseModel):
    # The winning side: "Marcus" or "Colton" (or "DRAW").
    winner: Literal["Marcus", "Colton", "DRAW"]
    judge_reasoning: str
    closing_summary: str