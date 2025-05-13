from typing import Dict

import requests

from agents_for_all.tools.base_tool import Tool


class WebFetcher(Tool):
    """
    A tool that fetches the content of a web page.

    Accepts a URL and returns the first 2000 characters of its response body.

    Example:
        {"url": "https://example.com"}
    """

    @property
    def name(self) -> str:
        """
        WebFetcher
        """
        return "WebFetcher"

    @property
    def description(self) -> str:
        """
        Fetches a webpage using HTTP GET.

        Input format:
        {"url": "<https-url>"}
        """
        return (
            "Fetches the HTML/text content of a given URL. "
            "Returns the first 2000 characters to avoid overload."
        )

    def execute(self, input_json: Dict) -> str:
        url = input_json.get("url")
        if not url:
            return "Error: 'url' key missing from input_json."
        try:
            response = requests.get(url)
            return response.text[:2000]
        except Exception as e:
            return f"Web error: {str(e)}"
