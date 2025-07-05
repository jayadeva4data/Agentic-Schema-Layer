import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from embedding_service import EmbeddingService

def test_embedding_service_add_and_search():
    service = EmbeddingService(collection_name="test_schema_elements")
    docs = [
        {"id": "model_1", "text": "sales table with columns date, amount, region"},
        {"id": "model_2", "text": "customer table with columns id, name, email"},
        {"id": "model_3", "text": "orders table with columns order_id, customer_id, total"},
    ]
    service.add_documents(docs)
    result = service.semantic_search("customer information", n_results=2)
    assert "ids" in result
    assert len(result["ids"][0]) > 0
    # The most relevant result should be the customer table
    assert "model_2" in result["ids"][0] 