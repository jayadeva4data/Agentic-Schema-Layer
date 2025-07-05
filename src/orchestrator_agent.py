from typing import List, Dict, Any
from agent_base import Agent

class OrchestratorAgent:
    """
    Coordinates the execution of multiple agents in a sequential workflow.
    Pass a list of agents at initialization, or register dynamically.
    """
    def __init__(self, agents: List[Agent] = None):
        self.agents: List[Agent] = agents or []

    def register_agent(self, agent: Agent):
        self.agents.append(agent)

    def run(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        context = initial_context.copy()
        for agent in self.agents:
            context = agent.run(context)
        return context

    def describe_workflow(self) -> str:
        return " -> ".join([agent.describe() for agent in self.agents]) 