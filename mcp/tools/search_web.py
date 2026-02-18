"""
searches the web for the researcher and skeptic agents through tavily
"""

from tavily import TavilyClient
from typing import Dict, List, Any
import os

class SearchWebTool:
    """
    MCP tool for searching the web using Tavily's include_domains filter.
    """
    
    def __init__(self):
        self.name = "search_web"
        self.description = (
            "Search the web for information, articles, and references about a topic. "
            "Use this when you need reliable, factual content from various sources."
        )
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    @property
    def schema(self) -> Dict[str, Any]:
        """
        Returns the tool schema for Azure OpenAI function calling.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to find web articles and information"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    
    def execute(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Execute the web search using Tavily.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, url, snippet, and domain
        """
        try:
            # Call Tavily with web search domain filter
            response = self.client.search(
                query=query,
                search_depth="basic",  # basic search
                include_domains=["google.com"],  # Web results from Google 
                max_results=max_results,
                include_answer=False,  # We don't need Tavily's summary
                include_raw_content=False  # Snippet is enough
            )
            
            # Parse and return results
            results = []
            for result in response.get("results", []):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("content", ""),
                    "domain": "google.com",
                    "score": result.get("score", 0.0)
                })
            
            return results
            
        except Exception as e:
            # Return error information
            return [{
                "error": str(e),
                "query": query
            }]