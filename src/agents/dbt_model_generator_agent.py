from agent_base import Agent
from typing import Dict, Any

class dbtModelGeneratorAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        schema_metadata = input_data.get('schema_metadata', {})
        dbt_models = {}
        for model, info in schema_metadata.get('models', {}).items():
            columns = info.get('columns', [])
            # Generate SQL: select all columns from the model
            sql = f"select {', '.join(columns) if columns else '*'} from {{ ref('{model}') }}"
            # Generate YAML: minimal dbt model schema
            yml = f"""version: 2
models:
  - name: {model}
    columns:
"""
            for col in columns:
                yml += f"      - name: {col}\n        description: ''\n"
            dbt_models[model] = {'sql': sql, 'yml': yml}
        input_data['dbt_models'] = dbt_models
        return input_data

    def describe(self) -> str:
        return "dbtModelGeneratorAgent: Generates dbt model SQL and YAML from schema metadata." 