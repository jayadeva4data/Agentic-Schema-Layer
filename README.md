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

