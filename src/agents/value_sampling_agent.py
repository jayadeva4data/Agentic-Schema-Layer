from agent_base import Agent
from typing import Dict, Any

class ValueSamplingAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        schema_metadata = input_data.get('schema_metadata', {})
        sampled_values = {}
        for model, info in schema_metadata.get('models', {}).items():
            for col in info.get('columns', []):
                # Simulate sampling: in real use, query DB for top N values
                sampled_values[f"{model}.{col}"] = ['A', 'B', 'C']
        input_data['sampled_values'] = sampled_values
        return input_data

    def describe(self) -> str:
        return "ValueSamplingAgent: Simulates sampling values for each model/column (would query DB in production)." 