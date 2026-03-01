"""
Marcus agent: argues for the first option in a two-choice debate.
"""

import json
from config import client, AZURE_OPENAI_DEPLOYMENT as deployment
from mcp.server import registry
from core.models import Argument, Source
from core.prompts import MARCUS_PROMPT


def marcus_agent(topic: str, context: str = "") -> Argument:
    print("\n" + "=" * 80)
    print("MARCUS - Building the case for the first option listed in the topic")
    print("=" * 80)

    messages = [
        {
            "role": "system",
            "content": MARCUS_PROMPT,
        },
        {
            "role": "user",
            "content": f"""Topic: {topic}
{f"Additional context: {context}" if context else ""}

Please research and present your strongest argument for your assigned side.
Return your response as JSON in this exact format:
{{
    "headline_claim": "one sentence summary of your main argument",
    "key_points": ["point 1", "point 2", "point 3"],
    "sources": [
        {{"title": "...", "url": "...", "snippet": "...", "domain": "..."}}
    ],
    "full_report": "your full argument in prose (300-500 words)"
}}""",
        },
    ]

    # Tool calling loop
    while True:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            tools=registry.get_schemas(),
            tool_choice="auto",
            max_tokens=1000,
            temperature=0.7,
        )

        response_message = response.choices[0].message
        if not response_message.tool_calls:
            break
        messages.append(response_message)
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print(f"\n[TOOL CALL] {tool_name}({tool_args})")
            result = registry.execute(tool_name, **tool_args)
            print(f"[TOOL RESULT] {str(result)[:200]}...")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    # Parse the final response into an Argument model
    try:
        if not response_message.content or not response_message.content.strip():
            print("Error: Empty response from API")
            return {"error": "Empty response from Marcus"}
        raw = json.loads(response_message.content)
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Response content: {response_message.content[:200]}")
        return {"error": f"Failed to parse response: {str(e)}"}

    argument = Argument(
        side="Marcus",
        headline_claim=raw["headline_claim"],
        key_points=raw["key_points"],
        sources=[Source(**s) for s in raw.get("sources", [])],
        full_report=raw["full_report"]
    )

    print("\n[MARCUS'S ARGUMENT]")
    print(argument.full_report)

    return argument
