import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

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