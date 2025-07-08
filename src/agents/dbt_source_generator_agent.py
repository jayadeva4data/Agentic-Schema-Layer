import os
from typing import Dict, Any, List
import yaml

class dbtSourceGeneratorAgent:
    """
    Generates a dbt sources YAML block for a given table and schema.
    Input:
      {
        'table_name': str,
        'schema': list  # List of dicts: [{'name': col, 'type': pg_type}]
      }
    Output:
      {
        'source_yml_path': str,
        'source_yml': str
      }
    """
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        table_name = input_data['table_name']
        schema = input_data['schema']
        source_name = 'public'  # hardcoded for now
        models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "semantic_layer_dbt", "models")
        os.makedirs(models_dir, exist_ok=True)
        yml_path = os.path.join(models_dir, "sources.yml")
        # Build YAML block
        source_block = {
            'version': 2,
            'sources': [
                {
                    'name': source_name,
                    'tables': [
                        {
                            'name': table_name,
                            'columns': [
                                {'name': col['name'], 'description': f"Column of type {col['type']}"} for col in schema
                            ]
                        }
                    ]
                }
            ]
        }
        # If sources.yml exists, append/merge
        if os.path.exists(yml_path):
            with open(yml_path, 'r') as f:
                existing = yaml.safe_load(f) or {}
            # Merge logic: add/replace table in source
            sources = existing.get('sources', [])
            found = False
            for src in sources:
                if src['name'] == source_name:
                    # Replace or add table
                    tables = src.get('tables', [])
                    for i, tbl in enumerate(tables):
                        if tbl['name'] == table_name:
                            tables[i] = source_block['sources'][0]['tables'][0]
                            break
                    else:
                        tables.append(source_block['sources'][0]['tables'][0])
                    src['tables'] = tables
                    found = True
                    break
            if not found:
                sources.append(source_block['sources'][0])
            merged = {'version': 2, 'sources': sources}
        else:
            merged = source_block
        # Write YAML
        with open(yml_path, 'w') as f:
            yaml.dump(merged, f, sort_keys=False)
        yml_str = yaml.dump(merged, sort_keys=False)
        return {'source_yml_path': yml_path, 'source_yml': yml_str} 