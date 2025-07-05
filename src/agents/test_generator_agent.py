from agent_base import Agent
from typing import Dict, Any

class TestGeneratorAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        schema_metadata = input_data.get('schema_metadata', {})
        dbt_tests = {}
        for model, info in schema_metadata.get('models', {}).items():
            for col in info.get('columns', []):
                # Example: not null and unique tests
                yml = f"""version: 2
models:
  - name: {model}
    columns:
      - name: {col}
        tests:
          - not_null
          - unique
"""
                dbt_tests[f"{model}.{col}"] = yml
        input_data['dbt_tests'] = dbt_tests
        return input_data

    def describe(self) -> str:
        return "TestGeneratorAgent: Generates dbt test YAML for each model/column from schema metadata." 