from abc import ABC, abstractmethod


class Model(ABC):
    """
    Abstract base class for models or model connectors to be exact.
    The models are initalized using its subclasses and can be used in agents.
    Some models are:
    - DirectModel (with api_endpoint, query_parameter_name, and other_parameters)
    - OpenAIModel
    - AntropicModel
    - GeminiModel
    """

    @abstractmethod
    def get_response(self, query: str) -> str:
        """
        Get response from the LLM based on the given query.

        Args:
            query (str): The query the LLM should respond to.

        Returns:
            str: The response to the query from the LLM.
        """
        raise NotImplementedError
