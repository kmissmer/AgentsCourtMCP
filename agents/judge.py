"""
Judge agent: weighs arguments and renders a verdict.
"""

import json
from config import client, AZURE_OPENAI_DEPLOYMENT as deployment
from core.models import Argument, Verdict
from core.prompts import JUDGE_PROMPT


def judge_agent(topic: str, marcus_arg: Argument, colton_arg: Argument) -> Verdict:
    print("\n" + "=" * 80)
    print("PIERCE (JUDGE) - Weighing Arguments and Rendering Judgment")
    print("=" * 80)

    messages = [
        {
            "role": "system",
            "content": JUDGE_PROMPT,
        },
        {
            "role": "user",
            "content": f"""Topic: {topic}

MARCUS'S ARGUMENT:
{marcus_arg.full_report}

Their key points:
{chr(10).join(f"- {p}" for p in marcus_arg.key_points)}

---

COLTON'S ARGUMENT:
{colton_arg.full_report}

Their key points:
{chr(10).join(f"- {p}" for p in colton_arg.key_points)}

Please evaluate both arguments and return your verdict as JSON in this exact format:
{{
    "winner": "Marcus", "Colton", or "DRAW",
    "judge_reasoning": "your detailed analysis",
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

    print("\n[JUDGE PIERCE's VERDICT]")
    print(f"Winner: {verdict.winner}")
    print(f"Reasoning: {verdict.judge_reasoning}")

    return verdict