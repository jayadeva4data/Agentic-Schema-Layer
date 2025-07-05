from agent_base import Agent
from typing import Dict, Any

class DocumentationAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        schema_metadata = input_data.get('schema_metadata', {})
        documentation = {}
        for model, info in schema_metadata.get('models', {}).items():
            model_doc = info.get('description', f"Model {model} with columns: {', '.join(info.get('columns', []))}")
            documentation[model] = model_doc
            for col in info.get('columns', []):
                documentation[f"{model}.{col}"] = f"Column {col} in model {model}."
        input_data['documentation'] = documentation
        return input_data

    def describe(self) -> str:
        return "DocumentationAgent: Generates documentation strings for each model and column from schema metadata." 