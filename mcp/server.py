"""
MCP server registration (tool registry).

This module exposes a minimal tool registry for MCP-style tool usage.
"""

from typing import Any, Dict, List, Optional

from mcp.tools.search_reddit import SearchRedditTool

from mcp.tools.search_wikipedia import SearchWikipediaTool

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
	"""Create and populate the MCP tool registry."""
	registry = ToolRegistry()

	if SearchRedditTool is not None:
		registry.register(SearchRedditTool())

	if SearchWikipediaTool is not None:
		registry.register(SearchWikipediaTool())

	return registry


registry: Optional[ToolRegistry]
registry = build_registry()
