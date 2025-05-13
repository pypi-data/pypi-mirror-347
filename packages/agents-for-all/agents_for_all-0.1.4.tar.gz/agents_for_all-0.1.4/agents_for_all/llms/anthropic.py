import logging
import re
from typing import Dict

from anthropic import Anthropic

from agents_for_all.llms.base_model import Model


class AnthropicModel(Model):
    """
    Anthropic Claude model connector using the official SDK.
    """

    def __init__(
        self, model: str, api_key: str, parameters: Dict | None = None
    ) -> None:
        """
        Initialize the Anthropic model.

        Args:
            model (str): The model name (e.g., "claude-3-sonnet-20240229").
            api_key (str): Your Anthropic API key.
            parameters (Dict, optional): Additional parameters (e.g., temperature).
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.parameters = {"max_tokens": 1024}
        self.parameters.update(parameters)

    def get_response(self, query: str) -> str:
        """
        Get response from Anthropic model.

        Args:
            query (str): The query the model should respond to.

        Returns:
            str: The model's response content.
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": query}],
                **self.parameters,
            )
            content = (
                response.content[0].text
                if hasattr(response, "content")
                else str(response)
            )
            return re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        except Exception as e:
            logging.error(e)
            raise e
