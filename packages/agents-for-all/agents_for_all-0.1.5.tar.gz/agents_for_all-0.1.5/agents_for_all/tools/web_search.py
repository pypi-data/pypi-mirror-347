from typing import Dict, Literal

import requests

from agents_for_all.tools.base_tool import Tool


class WebSearch(Tool):
    """
    A tool that performs a web search using Google or Bing API.

    Requires API keys during initialization.

    """

    def __init__(self, provider: Literal["google", "bing"], api_key: str, cx: str = ""):
        """
        Initialize the WebSearch tool.

        Args:
            provider (str): Either "google" or "bing".
            api_key (str): API key for the selected provider.
            cx (str): Custom Search Engine ID (only for Google).

        Returns:
            None
        """
        self.provider = provider
        self.api_key = api_key
        self.cx = cx

    @property
    def name(self) -> str:
        """
        WebSearch
        """
        return "WebSearch"

    @property
    def description(self) -> str:
        """
        Performs web search using Google or Bing.
        """
        return (
            "Searches the web using either Google or Bing API. "
            'Requires provider and API key during init. Input: {"query": "..."}.'
        )

    def execute(self, input_json: Dict) -> str:
        query = input_json.get("query")
        if not query:
            return "Error: 'query' key missing"

        try:
            if self.provider == "google":
                return self._google_search(query)
            elif self.provider == "bing":
                return self._bing_search(query)
            else:
                return f"Unsupported provider: {self.provider}"
        except Exception as e:
            return f"WebSearch error: {str(e)}"

    def _google_search(self, query: str) -> str:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": self.api_key,
            "cx": self.cx,
        }
        res = requests.get(url, params=params)
        data = res.json()
        items = data.get("items", [])
        return (
            "\n".join([f"{item['title']}: {item['link']}" for item in items[:3]])
            or "No results found."
        )

    def _bing_search(self, query: str) -> str:
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": query}
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        web_pages = data.get("webPages", {}).get("value", [])
        return (
            "\n".join([f"{item['name']}: {item['url']}" for item in web_pages[:3]])
            or "No results found."
        )
