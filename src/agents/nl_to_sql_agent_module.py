from agent_base import Agent
from typing import Dict, Any
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from nl_to_sql_agent import NLToSQLAgent
from dotenv import load_dotenv

class NLToSQLAgentModule(Agent):
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        load_dotenv()
        user_query = input_data.get('user_query', '')
        schema_metadata = input_data.get('schema_metadata', {})
        api_key = os.getenv('OPENAI_API_KEY')
        agent = NLToSQLAgent(schema_metadata, openai_api_key=api_key, model_name="gpt-4o")
        sql = agent.translate(user_query)
        input_data['sql'] = sql
        return input_data

    def describe(self) -> str:
        return "NLToSQLAgentModule: Uses LangChain and OpenAI (gpt-4o) to generate SQL from user query and schema metadata." 