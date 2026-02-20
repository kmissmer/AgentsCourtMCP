"""
Researcher agent: argues in favor.
"""

import json
from config import client, AZURE_OPENAI_DEPLOYMENT as deployment
from mcp.server import registry
from core.models import Argument, Source
from core.prompts import RESEARCHER_PROMPT


def researcher_agent(topic: str, context: str = "") -> Argument:
    print("\n" + "=" * 80)
    print("RESEARCHER AGENT - Building the case IN FAVOR")
    print("=" * 80)

    messages = [
        {
            "role": "system",
            "content": RESEARCHER_PROMPT,
        },
        {
            "role": "user",
            "content": f"""Topic: {topic}
{f"Additional context: {context}" if context else ""}

Please research and present your strongest argument IN FAVOR of this position.
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

        # If no tool calls, the model is done researching
        if not response_message.tool_calls:
            break

        # Add the model's response to message history
        messages.append(response_message)

        # Execute each tool call and feed results back
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
        # Check if response is empty
        if not response_message.content or not response_message.content.strip():
            print("Error: Empty response from API")
            return {"error": "Empty response from researcher agent"}
        
        raw = json.loads(response_message.content)
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Response content: {response_message.content[:200]}")  # Print first 200 chars
        return {"error": f"Failed to parse response: {str(e)}"}

    argument = Argument(
        side="FOR",
        headline_claim=raw["headline_claim"],
        key_points=raw["key_points"],
        sources=[Source(**s) for s in raw.get("sources", [])],
        full_report=raw["full_report"]
    )

    print("\n[RESEARCHER'S ARGUMENT]")
    print(argument.full_report)

    return argument