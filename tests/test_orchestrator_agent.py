from orchestrator_agent import OrchestratorAgent
from agent_base import Agent

class DummyAgentA(Agent):
    def run(self, input_data):
        input_data['a'] = 'A was here'
        return input_data
    def describe(self):
        return "DummyAgentA"

class DummyAgentB(Agent):
    def run(self, input_data):
        input_data['b'] = 'B was here'
        return input_data
    def describe(self):
        return "DummyAgentB"

def test_orchestrator_agent():
    orchestrator = OrchestratorAgent()
    orchestrator.register_agent(DummyAgentA())
    orchestrator.register_agent(DummyAgentB())
    initial_context = {'start': True}
    result = orchestrator.run(initial_context)
    assert result['a'] == 'A was here'
    assert result['b'] == 'B was here'
    assert orchestrator.describe_workflow() == "DummyAgentA -> DummyAgentB"

def test_full_agent_workflow():
    from agents.schema_introspector_agent import SchemaIntrospectorAgent
    from agents.value_sampling_agent import ValueSamplingAgent
    from agents.clarification_feedback_agent import ClarificationFeedbackAgent
    from agents.nl_to_sql_agent_module import NLToSQLAgentModule
    from agents.embedding_agent import EmbeddingAgent
    import os
    dbt_project_path = os.path.join(os.path.dirname(__file__), '../semantic_layer_dbt')
    workflow = [
        SchemaIntrospectorAgent(),
        ValueSamplingAgent(),
        ClarificationFeedbackAgent(),
        NLToSQLAgentModule(),
        EmbeddingAgent(),
    ]
    orchestrator = OrchestratorAgent(workflow)
    context = {
        'dbt_project_path': dbt_project_path,
        'user_query': "Show all customers with status 'A'"
    }
    result = orchestrator.run(context)
    # Check that all expected keys are present
    for key in ['schema_metadata', 'sampled_values', 'clarification', 'sql', 'embeddings']:
        assert key in result
    # If clarification is needed, sql may be empty
    if result['clarification']:
        assert result['sql'] 