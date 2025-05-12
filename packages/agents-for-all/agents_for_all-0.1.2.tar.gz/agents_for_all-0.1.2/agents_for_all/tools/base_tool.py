from abc import ABC, abstractmethod
from typing import Dict


class Tool(ABC):
    """
    Abstract base class for tools that can be used by agents.

    Tools perform tasks or operations when invoked with structured input.
    Each subclass must implement the `execute` method and define a `description`
    for the LLM or agent to understand the capability of the tool.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the tool.
        Should help the Agent run the appropriate tool.

        Returns:
            str: Name of the tool.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """
        A human-readable description of what the tool does.
        Should help the LLM choose the appropriate tool.

        Returns:
            str: Description of the tool's purpose and capabilities.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, input_json: Dict) -> str:
        """
        Execute the tool's functionality based on input JSON.

        Args:
            input_json (Dict): Input parameters to guide tool behavior.

        Returns:
            str: Output string describing the result of execution.
        """
        raise NotImplementedError
