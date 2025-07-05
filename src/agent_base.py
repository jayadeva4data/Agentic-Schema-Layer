from abc import ABC, abstractmethod
from typing import Any, Dict

class Agent(ABC):
    """
    Base interface for all agents in the multi-agent system.
    """
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main logic.
        Args:
            input_data: Input context or data for the agent.
        Returns:
            Output data or context after agent processing.
        """
        pass

    @abstractmethod
    def describe(self) -> str:
        """
        Return a human-readable description of the agent's purpose and capabilities.
        """
        pass 