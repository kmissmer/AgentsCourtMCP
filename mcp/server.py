"""
MCP server registration (tool registry).

This module exposes:
  - ToolRegistry: used internally by agents for function calling
  - mcp: a FastMCP server that wraps the same tools for real MCP protocol support (WIP for after the hackathon lol)
"""

from typing import Any, Dict, List, Optional

#from mcp.server.fastmcp import FastMCP

from mcp.tools.search_reddit import SearchRedditTool
from mcp.tools.search_wikipedia import SearchWikipediaTool


# ---------------------------------------------------------------------------
# Internal tool registry (used by agents via Azure OpenAI function calling)
# ---------------------------------------------------------------------------

class ToolRegistry:
    """Simple registry for MCP tools."""

    def __init__(self) -> None:
        self._tools: Dict[str, Any] = {}

    def register(self, tool: Any) -> None:
        if not getattr(tool, "name", None):
            raise ValueError("Tool must define a 'name' attribute.")
        self._tools[tool.name] = tool

    def list_tools(self) -> List[str]:
        return sorted(self._tools.keys())

    def get_schemas(self) -> List[Dict[str, Any]]:
        return [tool.schema for tool in self._tools.values()]

    def execute(self, name: str, **kwargs: Any) -> Any:
        tool = self._tools.get(name)
        if not tool:
            raise KeyError(f"Unknown tool: {name}")
        if not hasattr(tool, "execute"):
            raise AttributeError(f"Tool '{name}' has no execute method.")
        return tool.execute(**kwargs)


def build_registry() -> ToolRegistry:
    """Create and populate the tool registry."""
    registry = ToolRegistry()
    registry.register(SearchRedditTool())
    registry.register(SearchWikipediaTool())
    return registry


registry: ToolRegistry = build_registry()


# ---------------------------------------------------------------------------
# FastMCP server (real MCP protocol — run with `python server.py`)
# Wraps the same tool classes so logic lives in exactly one place.
# This is the stuff that wont be officially done until after the hackathon
# ---------------------------------------------------------------------------

'''
mcp = FastMCP("agents-court")

# Instantiate tools once and reuse for both the registry and MCP server
_reddit = SearchRedditTool()
_wikipedia = SearchWikipediaTool()


@mcp.tool()
def search_reddit(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search Reddit for community opinions, anecdotal experiences,
    and discussions about a topic. Use this when you need real-world
    user perspectives, common objections, or community wisdom."""
    return _reddit.execute(query=query, max_results=max_results)


@mcp.tool()
def search_wikipedia(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search Wikipedia for information, articles, and references about a topic.
    Use this when you need reliable, encyclopedic knowledge and factual content."""
    return _wikipedia.execute(query=query, max_results=max_results)



if __name__ == "__main__":
    # Run as a MCP server over stdio
    mcp.run()
    
'''