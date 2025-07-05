from agent_base import Agent
from typing import Dict, Any
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from schema_parser import SchemaParser

class SchemaIntrospectorAgent(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        dbt_project_path = input_data.get('dbt_project_path', os.path.join(os.path.dirname(__file__), '../../semantic_layer_dbt'))
        parser = SchemaParser(dbt_project_path=dbt_project_path)
        schema_metadata = parser.extract_metadata()
        # Ensure relationships and docs are present in the output
        models = schema_metadata.get('models', {})
        for model, info in models.items():
            if 'relationships' not in info:
                info['relationships'] = []
            if 'description' not in info:
                info['description'] = ''
        input_data['schema_metadata'] = schema_metadata
        return input_data

    def describe(self) -> str:
        return "SchemaIntrospectorAgent: Extracts models, columns, relationships, and docs from the dbt project using SchemaParser." 