from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from embedding_service import EmbeddingService
from schema_parser import SchemaParser
import os
from nl_to_sql_agent import NLToSQLAgent
from dotenv import load_dotenv

app = FastAPI()

class SemanticSearchRequest(BaseModel):
    query: str
    n_results: int = 5

class NLToSQLRequest(BaseModel):
    question: str
    openai_api_key: str = None  # Optional, fallback to env var

embedding_service = EmbeddingService()

load_dotenv()

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

def get_schema_metadata():
    dbt_project_path = os.path.join(os.path.dirname(__file__), "..", "semantic_layer_dbt")
    parser = SchemaParser(dbt_project_path=dbt_project_path)
    return parser.extract_metadata()

def get_nl_to_sql_agent(
    metadata=Depends(get_schema_metadata),
    openai_api_key: str = None
):
    return NLToSQLAgent(schema_metadata=metadata, openai_api_key=openai_api_key)

@app.post("/nl-to-sql")
def nl_to_sql(
    request: NLToSQLRequest,
    agent: NLToSQLAgent = Depends(get_nl_to_sql_agent)
):
    try:
        sql = agent.translate(request.question)
        return {"sql": sql}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
