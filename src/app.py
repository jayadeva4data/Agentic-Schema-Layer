from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from embedding_service import EmbeddingService
from schema_parser import SchemaParser
import os

app = FastAPI()

class SemanticSearchRequest(BaseModel):
    query: str
    n_results: int = 5

embedding_service = EmbeddingService()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/semantic-search")
def semantic_search(request: SemanticSearchRequest):
    try:
        results = embedding_service.semantic_search(request.query, n_results=request.n_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed-schema")
def embed_schema():
    try:
        dbt_project_path = os.path.join(os.path.dirname(__file__), "..", "semantic_layer_dbt")
        parser = SchemaParser(dbt_project_path=dbt_project_path)
        metadata = parser.extract_metadata()
        embedding_service.embed_schema_metadata(metadata)
        return {"status": "embedded", "num_elements": len(metadata.get("models", {})) + len(metadata.get("docs", {}))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
