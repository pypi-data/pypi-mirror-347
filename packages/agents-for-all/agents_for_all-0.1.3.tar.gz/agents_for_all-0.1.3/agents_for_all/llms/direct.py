import logging
import re
from typing import Dict

import requests

from agents_for_all.llms.base_model import Model


class DirectModel(Model):
    """
    Direct model (or model connector to be exact) which connects to an LLM
    by using api_endpoint and parameters using OpenAI format (as done by LLMStudio).
    """

    def __init__(
        self, api_endpoint: str, model: str, parameters: Dict | None = None
    ) -> None:
        """
        Initialize the Direct model.

        Args:
            api_endpoint (str): The api endpoint to call to get the response.
            model (str): The name of model.
            parameters: (Dict, optional): Other parameters to be used while getting responses. Optional.

        Returns:
            None
        """
        self.api_endpoint = api_endpoint
        self.model = model
        self.parameters = parameters

    def get_response(self, query: str):
        """
        Get response from the LLM based on the given query.

        Args:
            query (str): The query the LLM should respond to.

        Returns:
            str: The response to the query from the LLM.
        """
        json = {
            "messages": [{"role": "user", "content": query}],
            "model": self.model,
        }
        if self.parameters:
            json.update(self.parameters)
        response = requests.post(self.api_endpoint, json=json)
        try:
            response_json = response.json()
            llm_response = response_json["choices"][0]["message"]["content"]
            return re.sub(r"<think>.*?</think>", "", llm_response, flags=re.DOTALL)

        except Exception as e:
            logging.error(e)
            raise e
