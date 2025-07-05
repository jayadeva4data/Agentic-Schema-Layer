# Semantic Layer

This project implements a semantic layer for natural language to database query translation using dbt, FastAPI, and vector search.

## Setup

1. Create and activate the virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Initialize dbt (already scaffolded):
   ```
   dbt init semantic_layer_dbt --skip-profile-setup
   ```
4. Run the FastAPI app:
   ```
   uvicorn src.app:app --reload
   ```
5. Run tests:
   ```
   pytest
   ```

## Project Structure
- src/: Main application code
- tests/: All tests
- semantic_layer_dbt/: dbt project
- docs/: Documentation

## Health Check
Visit `/health` endpoint to verify the API is running.

## Agentic Architecture

This project uses a modular, agentic workflow for NL-to-SQL translation and dbt automation. Key agents include:
- **SchemaIntrospectorAgent**: Extracts models, columns, relationships, and docs from your dbt project.
- **NLToSQLAgentModule**: Uses LangChain and OpenAI (gpt-4o) to generate SQL from natural language queries, using schema metadata.
- **Other agents**: Macro generation, documentation, test generation, value sampling, clarification/feedback, and embedding.

### LangChain v0.3.x and OpenAI Integration
- Uses `langchain`, `langchain-community`, and `langchain-openai` (see requirements.txt).
- All LLM and chat model imports are now from `langchain_openai` (e.g., `from langchain_openai import ChatOpenAI`).
- The NL-to-SQL agent uses the latest `RunnableSequence` pattern (`prompt | llm`) and `.invoke()` for LLM calls.

## Requirements
- See `requirements.txt` for all dependencies, including the latest LangChain packages.

