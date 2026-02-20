"""
Judge agent: weighs arguments and renders a verdict.
"""

import json
from config import client, AZURE_OPENAI_DEPLOYMENT as deployment
from core.models import Argument, Verdict
from core.prompts import JUDGE_PROMPT


def judge_agent(topic: str, researcher_arg: Argument, skeptic_arg: Argument) -> Verdict:
    print("\n" + "=" * 80)
    print("JUDGE AGENT - Weighing Arguments and Rendering Judgment")
    print("=" * 80)

    messages = [
        {
            "role": "system",
            "content": JUDGE_PROMPT,
        },
        {
            "role": "user",
            "content": f"""Topic: {topic}

RESEARCHER'S ARGUMENT (FOR):
{researcher_arg.full_report}

Their key points:
{chr(10).join(f"- {p}" for p in researcher_arg.key_points)}

---

SKEPTIC'S ARGUMENT (AGAINST):
{skeptic_arg.full_report}

Their key points:
{chr(10).join(f"- {p}" for p in skeptic_arg.key_points)}

Please evaluate both arguments and return your verdict as JSON in this exact format:
{{
    "for_scores": {{
        "evidence_quality": int,
        "logical_coherence": int,
        "argument_completeness": int,
        "rebuttal_strength": int
    }},
    "against_scores": {{
        "evidence_quality": int,
        "logical_coherence": int,
        "argument_completeness": int,
        "rebuttal_strength": int
    }},
    "winner": "FOR" or "AGAINST" or "DRAW",
    "judge_reasoning": "detailed explanation of why you ruled this way",
    "closing_summary": "2-3 sentence plain English verdict"
}}""",
        },
    ]

    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=1500,
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    raw = json.loads(response.choices[0].message.content)

    verdict = Verdict(
        winner=raw["winner"],
        judge_reasoning=raw["judge_reasoning"],
        closing_summary=raw["closing_summary"],
    )

    print("\n[JUDGE'S VERDICT]")
    print(f"Winner: {verdict.winner}")
    print(f"Reasoning: {verdict.judge_reasoning}")

    return verdict