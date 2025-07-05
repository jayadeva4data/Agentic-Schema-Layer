from agents.schema_introspector_agent import SchemaIntrospectorAgent
import os

def test_schema_introspector_agent_extracts_schema():
    agent = SchemaIntrospectorAgent()
    dbt_project_path = os.path.join(os.path.dirname(__file__), '../semantic_layer_dbt')
    context = {'dbt_project_path': dbt_project_path}
    result = agent.run(context)
    assert 'schema_metadata' in result
    metadata = result['schema_metadata']
    assert isinstance(metadata, dict)
    assert 'models' in metadata
    assert isinstance(metadata['models'], dict)
    # Check at least one model exists
    assert len(metadata['models']) > 0
    # Check describe returns a string
    assert isinstance(agent.describe(), str) 