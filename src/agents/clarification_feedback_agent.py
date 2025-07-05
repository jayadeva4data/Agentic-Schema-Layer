from agent_base import Agent
from typing import Dict, Any

class ClarificationFeedbackAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_query = input_data.get('user_query', '')
        sampled_values = input_data.get('sampled_values', {})
        clarification = None
        # Simulate: if user_query contains a value not in any sampled_values, suggest clarification
        # For demo, look for a word in quotes in the query
        import re
        match = re.search(r"'([^']+)'", user_query)
        if match:
            value = match.group(1)
            found = any(value in values for values in sampled_values.values())
            if not found:
                clarification = f"Value '{value}' not found in sampled values. Did you mean one of: {set(v for vals in sampled_values.values() for v in vals)}?"
        input_data['clarification'] = clarification
        return input_data

    def describe(self) -> str:
        return "ClarificationFeedbackAgent: Suggests clarification if user query value not found in sampled values." 