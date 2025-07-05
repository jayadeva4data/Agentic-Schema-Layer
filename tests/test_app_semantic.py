import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fastapi.testclient import TestClient
from app import app, get_nl_to_sql_agent

client = TestClient(app)

class DummyAgent:
    def translate(self, question):
        return "SELECT * FROM customer_orders;"

def dummy_agent_dependency(metadata=None, openai_api_key=None):
    return DummyAgent()

app.dependency_overrides[get_nl_to_sql_agent] = dummy_agent_dependency

def test_embed_schema_and_semantic_search():
    # Embed the schema
    response = client.post("/embed-schema")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "embedded"
    assert data["num_elements"] > 0

    # Perform a semantic search
    response = client.post("/semantic-search", json={"query": "customer information", "n_results": 2})
    assert response.status_code == 200
    results = response.json()
    assert "ids" in results 

def test_nl_to_sql():
    response = client.post("/nl-to-sql", json={"question": "Show all customer orders"})
    assert response.status_code == 200
    data = response.json()
    assert "sql" in data
    assert data["sql"].lower().startswith("select") 