from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, Field
from embedding_service import EmbeddingService
from schema_parser import SchemaParser
import os
from nl_to_sql_agent import NLToSQLAgent
from dotenv import load_dotenv
from typing import List, Dict, Any
from uuid import uuid4
from agents.schema_introspector_agent import SchemaIntrospectorAgent
from agents.value_sampling_agent import ValueSamplingAgent
from agents.clarification_feedback_agent import ClarificationFeedbackAgent
from agents.nl_to_sql_agent_module import NLToSQLAgentModule
from agents.embedding_agent import EmbeddingAgent
from orchestrator_agent import OrchestratorAgent
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import logging
from datetime import datetime

app = FastAPI()

# CORS setup for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

class SemanticSearchRequest(BaseModel):
    query: str
    n_results: int = 5

class NLToSQLRequest(BaseModel):
    question: str
    openai_api_key: str = None  # Optional, fallback to env var

embedding_service = EmbeddingService()

load_dotenv()

# In-memory stores for demo
DATA_STORE: Dict[str, Dict[str, Any]] = {}
WORKFLOW_STORE: Dict[str, Dict[str, Any]] = {}
WORKFLOW_EXECUTIONS: Dict[str, Dict[str, Any]] = {}

class UploadResponse(BaseModel):
    data_id: str
    status: str

class AnalyzeSchemaResponse(BaseModel):
    schema: Dict[str, Any]
    status: str

class ProfileDataResponse(BaseModel):
    profile: Dict[str, Any]
    status: str

class TransformDataRequest(BaseModel):
    data_id: str
    nl_instruction: str
    preview: bool = True

class TransformDataResponse(BaseModel):
    code: str = ""
    preview: Dict[str, Any] = Field(default_factory=dict)
    status: str

class AgentInfo(BaseModel):
    name: str
    config_schema: Dict[str, Any] = Field(default_factory=dict)

class WorkflowRequest(BaseModel):
    workflow: Dict[str, Any]

class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str

class ExecuteWorkflowRequest(BaseModel):
    workflow_id: str
    input: Dict[str, Any]

class ExecuteWorkflowResponse(BaseModel):
    execution_id: str
    status: str

class WorkflowStatusResponse(BaseModel):
    status: str
    logs: List[str] = Field(default_factory=list)
    result: Dict[str, Any] = Field(default_factory=dict)

class UploadCSVResponse(BaseModel):
    id: str
    name: str
    schema: list
    row_count: int

class AnalyzeSchemaListResponse(BaseModel):
    schema: list

class ProfileSchemaListResponse(BaseModel):
    total_rows: int
    total_columns: int
    missing_values: dict
    schema: list

class DataSourceInfo(BaseModel):
    id: str
    name: str
    row_count: int
    schema: list

class DataSourcesListResponse(BaseModel):
    sources: list

class TransformDataRequestV2(BaseModel):
    source_id: str
    instruction: str

class TransformDataResponseV2(BaseModel):
    generated_code: str
    preview_data: list

class ApplyTransformationRequest(BaseModel):
    source_id: str
    step_id: int
    code: str

class ApplyTransformationResponse(BaseModel):
    success: bool

class RevertTransformationRequest(BaseModel):
    source_id: str
    step_id: int

class RevertTransformationResponse(BaseModel):
    success: bool

class ViewDataResponse(BaseModel):
    data: list
    total_rows: int
    columns: list

def to_python_type(val):
    if isinstance(val, (np.integer, np.int64, np.int32)):
        return int(val)
    if isinstance(val, (np.floating, np.float64, np.float32)):
        return float(val)
    if isinstance(val, np.ndarray):
        return val.tolist()
    return val

def pandas_dtype_to_type(dtype):
    dtype = str(dtype)
    if dtype.startswith('int'):
        return 'integer'
    if dtype.startswith('float'):
        return 'float'
    if dtype.startswith('datetime'):
        return 'datetime'
    return 'string'

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

@app.post("/upload-csv/", response_model=UploadCSVResponse)
def upload_csv(file: UploadFile = File(...)):
    data_id = str(uuid4())
    upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploaded_data")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{data_id}.csv")
    try:
        with open(file_path, "wb") as f:
            content = file.file.read()
            f.write(content)
        df = pd.read_csv(file_path, low_memory=False)  # Use full CSV for stats
        schema = []
        for col in df.columns:
            col_data = df[col]
            col_type = pandas_dtype_to_type(col_data.dtype)
            null_count = int(col_data.isnull().sum())
            unique_count = int(col_data.nunique())
            sample_values = [to_python_type(x) for x in col_data.dropna().unique()[:5]]
            nullable = bool(null_count > 0)
            schema.append({
                "name": col,
                "type": col_type,
                "nullable": nullable,
                "sample_values": sample_values,
                "unique_count": unique_count,
                "null_count": null_count
            })
        row_count = int(len(df))
        DATA_STORE[data_id] = {
            "filename": file.filename,
            "path": file_path,
            "status": "uploaded",
            "schema": schema,
            "row_count": row_count
        }
        return UploadCSVResponse(id=data_id, name=file.filename, schema=schema, row_count=row_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/analyze-schema/{source_id}", response_model=AnalyzeSchemaListResponse)
def analyze_schema(source_id: str):
    data_info = DATA_STORE.get(source_id)
    if not data_info or "path" not in data_info:
        raise HTTPException(status_code=404, detail="Data not found")
    schema = data_info.get("schema")
    if not schema:
        try:
            df = pd.read_csv(data_info["path"], low_memory=False)  # Use full CSV for stats
            schema = []
            for col in df.columns:
                col_data = df[col]
                col_type = pandas_dtype_to_type(col_data.dtype)
                null_count = int(col_data.isnull().sum())
                unique_count = int(col_data.nunique())
                sample_values = [to_python_type(x) for x in col_data.dropna().unique()[:5]]
                nullable = bool(null_count > 0)
                schema.append({
                    "name": col,
                    "type": col_type,
                    "nullable": nullable,
                    "sample_values": sample_values,
                    "unique_count": unique_count,
                    "null_count": null_count
                })
            DATA_STORE[source_id]["schema"] = schema
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Schema analysis failed: {str(e)}")
    return AnalyzeSchemaListResponse(schema=schema)

@app.post("/profile-data/{source_id}", response_model=ProfileSchemaListResponse)
def profile_data(source_id: str):
    data_info = DATA_STORE.get(source_id)
    if not data_info or "path" not in data_info:
        raise HTTPException(status_code=404, detail="Data not found")
    file_path = data_info["path"]
    try:
        df = pd.read_csv(file_path, low_memory=False)  # Use full CSV for stats
        schema = data_info.get("schema")
        if not schema:
            schema = []
            for col in df.columns:
                col_data = df[col]
                col_type = pandas_dtype_to_type(col_data.dtype)
                null_count = int(col_data.isnull().sum())
                unique_count = int(col_data.nunique())
                sample_values = [to_python_type(x) for x in col_data.dropna().unique()[:5]]
                nullable = bool(null_count > 0)
                schema.append({
                    "name": col,
                    "type": col_type,
                    "nullable": nullable,
                    "sample_values": sample_values,
                    "unique_count": unique_count,
                    "null_count": null_count
                })
        total_rows = int(len(df))
        total_columns = int(len(df.columns))
        missing_values = {col: int(df[col].isnull().sum()) for col in df.columns}
        DATA_STORE[source_id]["profiled_schema"] = schema
        return ProfileSchemaListResponse(
            total_rows=total_rows,
            total_columns=total_columns,
            missing_values=missing_values,
            schema=schema
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profiling failed: {str(e)}")

@app.post("/transform-data/", response_model=TransformDataResponseV2)
def transform_data_v2(request: TransformDataRequestV2):
    data_info = DATA_STORE.get(request.source_id)
    if not data_info or "path" not in data_info:
        raise HTTPException(status_code=404, detail="Data not found")
    file_path = data_info["path"]
    try:
        df = pd.read_csv(file_path, low_memory=False)  # Use full CSV for preview
        # Use LLM to generate pandas code for the transformation
        prompt = PromptTemplate(
            input_variables=["instruction", "columns"],
            template=(
                "You are a Python data analyst. Given the following columns: {columns}, "
                "write a single pandas code snippet to perform this transformation: {instruction}. "
                "Assume the DataFrame is named df. Only output the code, no explanation."
            )
        )
        columns = ", ".join(df.columns)
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        chain = prompt | llm
        code = chain.invoke({"instruction": request.instruction, "columns": columns})
        # Extract code from LLM output
        if hasattr(code, "content"):
            code = code.content
        elif isinstance(code, dict) and "text" in code:
            code = code["text"]
        code = code.strip().strip("`")
        if code.startswith("python"):
            code = code[len("python"):].lstrip()
        # Execute the code in a safe namespace
        exec_globals = {"pd": pd, "datetime": datetime, "df": df.copy()}
        try:
            exec(code, exec_globals)
            df_transformed = exec_globals.get("df", df)
        except Exception as e:
            logging.exception("Error executing transformation code")
            return TransformDataResponseV2(generated_code=code, preview_data=[])
        # Return preview (first 5 rows as dict, ensure all values are serializable)
        preview = df_transformed.head().replace({np.nan: None}).to_dict(orient="records")
        # Store transformation history
        history = data_info.get("transformation_history", [])
        history.append({"instruction": request.instruction, "code": code})
        DATA_STORE[request.source_id]["transformation_history"] = history
        return TransformDataResponseV2(generated_code=code, preview_data=preview)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")

@app.get("/agents/", response_model=List[AgentInfo])
def get_agents():
    # Return available agents and their config schemas
    agents = [
        AgentInfo(name="SchemaIntrospectorAgent"),
        AgentInfo(name="ValueSamplingAgent"),
        AgentInfo(name="ClarificationFeedbackAgent"),
        AgentInfo(name="NLToSQLAgentModule"),
        AgentInfo(name="EmbeddingAgent"),
    ]
    return agents

@app.post("/workflows/", response_model=WorkflowResponse)
def save_workflow(request: WorkflowRequest):
    workflow_id = str(uuid4())
    WORKFLOW_STORE[workflow_id] = request.workflow
    return WorkflowResponse(workflow_id=workflow_id, status="saved")

@app.post("/execute-workflow/", response_model=ExecuteWorkflowResponse)
def execute_workflow(request: ExecuteWorkflowRequest):
    execution_id = str(uuid4())
    # For demo, just store input and workflow
    WORKFLOW_EXECUTIONS[execution_id] = {"workflow_id": request.workflow_id, "input": request.input, "status": "started", "logs": [], "result": {}}
    # TODO: Actually run the workflow using OrchestratorAgent
    WORKFLOW_EXECUTIONS[execution_id]["status"] = "complete"
    WORKFLOW_EXECUTIONS[execution_id]["result"] = {"message": "Workflow executed (stub)"}
    return ExecuteWorkflowResponse(execution_id=execution_id, status="started")

@app.get("/workflow-status/{execution_id}", response_model=WorkflowStatusResponse)
def workflow_status(execution_id: str):
    exec_info = WORKFLOW_EXECUTIONS.get(execution_id, None)
    if not exec_info:
        raise HTTPException(status_code=404, detail="Execution not found")
    return WorkflowStatusResponse(status=exec_info["status"], logs=exec_info["logs"], result=exec_info["result"])

@app.get("/data-sources/", response_model=DataSourcesListResponse)
def list_data_sources():
    sources = []
    for data_id, info in DATA_STORE.items():
        sources.append({
            "id": data_id,
            "name": info.get("filename", ""),
            "row_count": info.get("row_count", 0),
            "schema": info.get("schema", [])
        })
    return DataSourcesListResponse(sources=sources)

@app.post("/apply-transformation/", response_model=ApplyTransformationResponse)
def apply_transformation(request: ApplyTransformationRequest):
    data_info = DATA_STORE.get(request.source_id)
    if not data_info or "path" not in data_info:
        raise HTTPException(status_code=404, detail="Data not found")
    file_path = data_info["path"]
    try:
        df = pd.read_csv(file_path, low_memory=False)
        # Replay all transformations up to and including step_id
        history = data_info.get("transformation_history", [])
        if request.step_id >= len(history):
            raise HTTPException(status_code=400, detail="Invalid step_id")
        for i in range(request.step_id + 1):
            code = history[i]["code"] if i != request.step_id else request.code
            local_vars = {"df": df}
            try:
                exec(code, {}, local_vars)
                df = local_vars["df"]
            except Exception as e:
                logging.exception("Error executing transformation code in apply-transformation")
                raise HTTPException(status_code=500, detail=f"Apply transformation code error: {str(e)}")
        # Save the new state to disk
        df.to_csv(file_path, index=False)
        # Truncate history to this step
        DATA_STORE[request.source_id]["transformation_history"] = history[:request.step_id + 1]
        return ApplyTransformationResponse(success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Apply transformation failed: {str(e)}")

@app.post("/revert-transformation/", response_model=RevertTransformationResponse)
def revert_transformation(request: RevertTransformationRequest):
    data_info = DATA_STORE.get(request.source_id)
    if not data_info or "path" not in data_info:
        raise HTTPException(status_code=404, detail="Data not found")
    file_path = data_info["path"]
    try:
        df = pd.read_csv(file_path, low_memory=False)
        history = data_info.get("transformation_history", [])
        if request.step_id >= len(history):
            raise HTTPException(status_code=400, detail="Invalid step_id")
        # Replay all transformations up to (but not including) step_id
        df_orig = pd.read_csv(file_path, low_memory=False)
        for i in range(request.step_id):
            code = history[i]["code"]
            local_vars = {"df": df_orig}
            try:
                exec(code, {}, local_vars)
                df_orig = local_vars["df"]
            except Exception as e:
                logging.exception("Error executing transformation code in revert-transformation")
                raise HTTPException(status_code=500, detail=f"Revert transformation code error: {str(e)}")
        # Save the reverted state to disk
        df_orig.to_csv(file_path, index=False)
        # Truncate history to this step
        DATA_STORE[request.source_id]["transformation_history"] = history[:request.step_id]
        return RevertTransformationResponse(success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Revert transformation failed: {str(e)}")

@app.get("/view-data/{source_id}", response_model=ViewDataResponse)
def view_data(source_id: str, n_rows: int = 20):
    data_info = DATA_STORE.get(source_id)
    if not data_info or "path" not in data_info:
        raise HTTPException(status_code=404, detail="Data not found")
    file_path = data_info["path"]
    try:
        df = pd.read_csv(file_path, low_memory=False)
        preview = df.head(n_rows).replace({np.nan: None}).to_dict(orient="records")
        # Convert all numpy types to Python types
        preview = [
            {k: to_python_type(v) for k, v in row.items()} for row in preview
        ]
        return ViewDataResponse(data=preview, total_rows=int(len(df)), columns=list(df.columns))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"View data failed: {str(e)}")
