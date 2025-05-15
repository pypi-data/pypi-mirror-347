import logging
import re
from typing import Dict

import openai

from agents_for_all.llms.base_model import Model


class OpenAIModel(Model):
    """
    OpenAI model connector using the official OpenAI SDK.
    """

    def __init__(
        self, model: str, api_key: str, parameters: Dict | None = None
    ) -> None:
        """
        Initialize the OpenAI model.

        Args:
            model (str): The model name (e.g., "gpt-4", "gpt-3.5-turbo").
            api_key (str): Your OpenAI API key.
            parameters (Dict, optional): Additional parameters (e.g., temperature).
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.parameters = parameters or {}

    def get_response(self, query: str) -> str:
        """
        Get response from OpenAI chat model.

        Args:
            query (str): The query the model should respond to.

        Returns:
            str: The LLM's text response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": query}],
                **self.parameters,
            )
            content = response.choices[0].message.content
            return re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        except Exception as e:
            logging.error(e)
            raise e
