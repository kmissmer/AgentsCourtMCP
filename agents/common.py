"""
Shared utilities for agent behavior.
"""

from config import client, AZURE_OPENAI_DEPLOYMENT as deployment
from mcp.tools.search_reddit import SearchRedditTool
from mcp.tools.search_wikipedia import SearchWikipediaTool


def format_search_results(results):
    """Format search results for display and agent context, including source."""
    parts = []
    for i, r in enumerate(results):
        if r.get("error"):
            parts.append(f"Result {i+1}: ERROR: {r.get('error')}")
        else:
            title = r.get("title") or "(no title)"
            url = r.get("url") or "(no url)"
            snippet = r.get("snippet") or ""
            domain = r.get("domain") or "unknown"
            parts.append(f"{i+1}. [{domain.upper()}] {title}\n{url}\n{snippet}\n")
    return "\n".join(parts)


def search_for_information(query: str, max_results: int = 5, source: str = "both") -> str:
    """Search for information on a topic.
    
    Args:
        query: Search query
        max_results: Maximum results per source
        source: "reddit", "wikipedia", or "both" (default)
    """
    all_results = []
    
    if source in ("reddit", "both"):
        try:
            reddit_tool = SearchRedditTool()
            reddit_results = reddit_tool.execute(query=query, max_results=max_results)
            if reddit_results and not reddit_results[0].get("error"):
                all_results.extend(reddit_results)
        except Exception as e:
            print(f"Reddit search error: {e}")
    
    if source in ("wikipedia", "both"):
        try:
            wiki_tool = SearchWikipediaTool()
            wiki_results = wiki_tool.execute(query=query, max_results=max_results)
            if wiki_results and not wiki_results[0].get("error"):
                all_results.extend(wiki_results)
        except Exception as e:
            print(f"Wikipedia search error: {e}")
    
    if not all_results:
        return "No search results found."
    
    return format_search_results(all_results)
