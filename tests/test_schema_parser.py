import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from schema_parser import SchemaParser

def test_schema_parser_extract_metadata_returns_dict(tmp_path):
    parser = SchemaParser(dbt_project_path="semantic_layer_dbt")
    metadata = parser.extract_metadata()
    assert isinstance(metadata, dict)

def test_schema_parser_extracts_models_and_columns():
    parser = SchemaParser(dbt_project_path="semantic_layer_dbt")
    metadata = parser.extract_metadata()
    # Check that example models are found
    assert "my_first_dbt_model" in metadata["models"]
    assert "my_second_dbt_model" in metadata["models"]
    # Columns should be a list
    assert isinstance(metadata["models"]["my_first_dbt_model"]["columns"], list)

def test_schema_parser_extracts_docs():
    parser = SchemaParser(dbt_project_path="semantic_layer_dbt")
    metadata = parser.extract_metadata()
    # Should extract docs for models with descriptions
    assert "my_first_dbt_model" in metadata["docs"] 