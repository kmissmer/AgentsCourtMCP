"""
experimentation script to test out how the search_reddit tool works in practice, and how the assistant can summarize the results.
"""

from openai import AzureOpenAI
from dotenv import load_dotenv
import os

from mcp.tools.search_reddit import SearchRedditTool

load_dotenv()
subscription_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

deployment = "gpt-4o-mini"


client = AzureOpenAI(
    api_version="2025-01-01-preview",
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


def format_search_results(results):
    parts = []
    for i, r in enumerate(results):
        if r.get("error"):
            parts.append(f"Result {i+1}: ERROR: {r.get('error')}")
        else:
            title = r.get("title") or "(no title)"
            url = r.get("url") or "(no url)"
            snippet = r.get("snippet") or ""
            parts.append(f"{i+1}. {title}\n{url}\n{snippet}\n")
    return "\n".join(parts)


def main():
    # Use the SearchRedditTool to gather Reddit opinions about Shedeur Sanders
    query = "Shedeur Sanders opinions"
    tool = SearchRedditTool()
    results = tool.execute(query=query, max_results=5)

    # If the tool returned an error structure, print and exit
    if results and isinstance(results, list) and results[0].get("error"):
        print("Search tool error:", results[0].get("error"))
        return

    formatted = format_search_results(results)

    # Send the search results to the assistant to summarize community opinions
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes community opinions from Reddit search results."},
        {"role": "user", "content": f"I searched Reddit for '{query}' and found these results:\n\n{formatted}\nPlease summarize the common opinions, notable arguments, and overall sentiment."}
    ]

    response = client.chat.completions.create(
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=1.0,
        model=deployment
    )

    assistant_reply = response.choices[0].message.content
    print("--- Search Results ---")
    print(formatted)
    print("--- Asistant Summary ---")
    print(assistant_reply)


if __name__ == "__main__":
    main()