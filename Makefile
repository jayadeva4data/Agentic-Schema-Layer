# Makefile for Agentic Schema Layer

.PHONY: help setup venv install run test lint dbt-init dbt-run dbt-clean clean

help:
	@echo "Available targets:"
	@echo "  setup      - Create venv, install dependencies, and setup dbt"
	@echo "  venv       - Create Python virtual environment (venv/)"
	@echo "  install    - Install Python dependencies from requirements.txt"
	@echo "  run        - Run FastAPI app with Uvicorn"
	@echo "  test       - Run all tests with pytest"
	@echo "  lint       - Lint Python code with flake8 (install if needed)"
	@echo "  dbt-init   - Initialize dbt project (if not already)"
	@echo "  dbt-run    - Run dbt models"
	@echo "  dbt-clean  - Clean dbt artifacts"
	@echo "  clean      - Remove venv, __pycache__, and dbt artifacts"

setup: venv install dbt-init

venv:
	python3 -m venv venv

install:
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. venv/bin/activate && uvicorn src.app:app --reload

test:
	PYTHONPATH=src . venv/bin/activate && pytest

lint:
	. venv/bin/activate && pip install flake8 && flake8 src tests

dbt-init:
	. venv/bin/activate && dbt init semantic_layer_dbt --skip-profile-setup || true

dbt-run:
	. venv/bin/activate && cd semantic_layer_dbt && dbt run

dbt-clean:
	. venv/bin/activate && cd semantic_layer_dbt && dbt clean

clean:
	rm -rf venv __pycache__ semantic_layer_dbt/dbt_modules semantic_layer_dbt/target *.pyc 