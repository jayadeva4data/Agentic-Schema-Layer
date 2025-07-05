from agent_base import Agent
from typing import Dict, Any

class EmbeddingAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_query = input_data.get('user_query', '')
        schema_metadata = input_data.get('schema_metadata', {})
        # Dummy embedding: just a list of numbers
        embedding = [0.1, 0.2, 0.3]
        input_data['embeddings'] = embedding
        return input_data

    def describe(self) -> str:
        return "EmbeddingAgent: Simulates embedding generation for user query and schema (dummy vector)." 