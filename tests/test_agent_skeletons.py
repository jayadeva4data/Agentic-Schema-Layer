from agents.schema_introspector_agent import SchemaIntrospectorAgent
from agents.dbt_model_generator_agent import dbtModelGeneratorAgent
from agents.macro_generator_agent import MacroGeneratorAgent
from agents.documentation_agent import DocumentationAgent
from agents.test_generator_agent import TestGeneratorAgent
from agents.value_sampling_agent import ValueSamplingAgent
from agents.clarification_feedback_agent import ClarificationFeedbackAgent
from agents.nl_to_sql_agent_module import NLToSQLAgentModule
from agents.embedding_agent import EmbeddingAgent

import pytest
import os

def test_agent_skeletons():
    agents = [
        SchemaIntrospectorAgent(),
        dbtModelGeneratorAgent(),
        MacroGeneratorAgent(),
        DocumentationAgent(),
        TestGeneratorAgent(),
        ValueSamplingAgent(),
        ClarificationFeedbackAgent(),
        NLToSQLAgentModule(),
        EmbeddingAgent(),
    ]
    context = {}
    for agent in agents:
        context = agent.run(context)
        desc = agent.describe()
        assert isinstance(desc, str)
    # Check that all expected keys are present in context
    expected_keys = [
        'schema_metadata', 'dbt_models', 'macros', 'documentation', 'dbt_tests',
        'sampled_values', 'clarification', 'sql', 'embeddings'
    ]
    for key in expected_keys:
        assert key in context

def test_dbt_model_generator_agent():
    # Use real schema metadata from SchemaIntrospectorAgent
    agent = dbtModelGeneratorAgent()
    dbt_project_path = os.path.join(os.path.dirname(__file__), '../semantic_layer_dbt')
    schema_agent = SchemaIntrospectorAgent()
    context = {'dbt_project_path': dbt_project_path}
    context = schema_agent.run(context)
    result = agent.run(context)
    assert 'dbt_models' in result
    dbt_models = result['dbt_models']
    assert isinstance(dbt_models, dict)
    assert len(dbt_models) > 0
    for model, files in dbt_models.items():
        assert 'sql' in files and 'yml' in files
        assert files['sql'].startswith('select')
        assert 'version: 2' in files['yml'] 

def test_macro_generator_agent():
    agent = MacroGeneratorAgent()
    dbt_project_path = os.path.join(os.path.dirname(__file__), '../semantic_layer_dbt')
    schema_agent = SchemaIntrospectorAgent()
    context = {'dbt_project_path': dbt_project_path}
    context = schema_agent.run(context)
    result = agent.run(context)
    assert 'macros' in result
    macros = result['macros']
    assert isinstance(macros, list)
    assert len(macros) > 0
    for macro in macros:
        assert macro.startswith('{% macro')
        assert 'select' in macro 

def test_documentation_agent():
    agent = DocumentationAgent()
    dbt_project_path = os.path.join(os.path.dirname(__file__), '../semantic_layer_dbt')
    schema_agent = SchemaIntrospectorAgent()
    context = {'dbt_project_path': dbt_project_path}
    context = schema_agent.run(context)
    result = agent.run(context)
    assert 'documentation' in result
    documentation = result['documentation']
    assert isinstance(documentation, dict)
    assert len(documentation) > 0
    # Check at least one model and one column doc
    has_model_doc = any('.' not in k for k in documentation)
    has_col_doc = any('.' in k for k in documentation)
    assert has_model_doc and has_col_doc 

def test_test_generator_agent():
    from agents.test_generator_agent import TestGeneratorAgent
    from agents.schema_introspector_agent import SchemaIntrospectorAgent
    import os
    agent = TestGeneratorAgent()
    dbt_project_path = os.path.join(os.path.dirname(__file__), '../semantic_layer_dbt')
    schema_agent = SchemaIntrospectorAgent()
    context = {'dbt_project_path': dbt_project_path}
    context = schema_agent.run(context)
    result = agent.run(context)
    assert 'dbt_tests' in result
    dbt_tests = result['dbt_tests']
    assert isinstance(dbt_tests, dict)
    assert len(dbt_tests) > 0
    for key, yml in dbt_tests.items():
        assert 'not_null' in yml and 'unique' in yml 

def test_value_sampling_agent():
    from agents.value_sampling_agent import ValueSamplingAgent
    from agents.schema_introspector_agent import SchemaIntrospectorAgent
    import os
    agent = ValueSamplingAgent()
    dbt_project_path = os.path.join(os.path.dirname(__file__), '../semantic_layer_dbt')
    schema_agent = SchemaIntrospectorAgent()
    context = {'dbt_project_path': dbt_project_path}
    context = schema_agent.run(context)
    result = agent.run(context)
    assert 'sampled_values' in result
    sampled_values = result['sampled_values']
    assert isinstance(sampled_values, dict)
    assert len(sampled_values) > 0
    for key, values in sampled_values.items():
        assert isinstance(values, list)
        assert values == ['A', 'B', 'C'] 

def test_nl_to_sql_agent_module():
    import os
    from agents.nl_to_sql_agent_module import NLToSQLAgentModule
    agent = NLToSQLAgentModule()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        import pytest
        pytest.skip('No OpenAI API key set')
    context = {
        'user_query': "Show all customers with status 'A'",
        'schema_metadata': {'models': {'customers': {'columns': ['status']}}},
        'sampled_values': {'customers.status': ['A', 'B', 'C']}
    }
    result = agent.run(context)
    assert 'sql' in result
    assert 'select' in result['sql'].lower() or 'SELECT' in result['sql']

def test_embedding_agent():
    from agents.embedding_agent import EmbeddingAgent
    agent = EmbeddingAgent()
    context = {
        'user_query': "Show all customers with status 'A'",
        'schema_metadata': {'models': {'customers': {'columns': ['status']}}}
    }
    result = agent.run(context)
    assert 'embeddings' in result
    assert isinstance(result['embeddings'], list)
    assert result['embeddings'] == [0.1, 0.2, 0.3] 