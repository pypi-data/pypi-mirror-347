import logging
import re
from typing import Dict

import google.generativeai as genai

from agents_for_all.llms.base_model import Model


class GeminiModel(Model):
    """
    Google Gemini model connector using the official Google Generative AI SDK.
    """

    def __init__(
        self, model: str, api_key: str, parameters: Dict | None = None
    ) -> None:
        """
        Initialize the Gemini model.

        Args:
            model (str): Gemini model ID (e.g., "gemini-pro").
            api_key (str): Your Google API key.
            parameters (Dict, optional): Additional generation parameters.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.parameters = parameters or {}

    def get_response(self, query: str) -> str:
        """
        Get response from Gemini model.

        Args:
            query (str): The prompt to send.

        Returns:
            str: The model's response content.
        """
        try:
            response = self.model.generate_content(
                query, generation_config=self.parameters
            )
            content = response.text if hasattr(response, "text") else str(response)
            return re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        except Exception as e:
            logging.error(e)
            raise e
