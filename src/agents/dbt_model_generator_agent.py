from agent_base import Agent
from typing import Dict, Any
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

class dbtModelGeneratorAgent(Agent):
    """
    Input required:
        input_data = {
            'schema_text': str,  # DDL or schema info as plain text (e.g., CREATE TABLE ... or column list)
            'model_name': str,   # Name for the dbt model (used for file names, should be different from raw table)
            'source_schema': str (optional, default 'public'),
            'source_table': str (optional, default model_name + '_raw'),
            'openai_api_key': str (optional)  # If not set, will use env var
        }
    Output:
        {
            'model_sql_path': str,
            'model_yml_path': str,
            'model_sql': str,
            'model_yml': str
        }
    Note: The dbt model name should be different from the raw source table name to avoid conflicts. If the raw table is 'beneficiaries_raw', the dbt model should be 'beneficiaries'.
    """
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        load_dotenv()
        schema_text = input_data['schema_text']
        model_name = input_data['model_name']
        source_schema = input_data.get('source_schema', 'public')
        source_table = input_data.get('source_table', model_name + '_raw')
        openai_api_key = input_data.get('openai_api_key')
        llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=openai_api_key)

        # Prompt for SQL
        sql_prompt = PromptTemplate(
            input_variables=["schema_text", "model_name", "source_schema", "source_table"],
            template=(
                """
                You are a data engineer. Given the following table schema or DDL:\n\n{schema_text}\n\nGenerate a detailed dbt model SQL file for a model named '{model_name}'.\n- The dbt model name should be different from the raw source table name to avoid conflicts. If the raw table is named '{source_table}', the dbt model should be named '{model_name}'.\n- Use best practices for formatting and comments.\n- Do not include any explanations, only output the SQL code.\n- The source table is in schema '{source_schema}' and named '{source_table}'.\n- Use dbt's source() macro: {{ source('{source_schema}', '{source_table}') }}\n- The target database is PostgreSQL. Use only PostgreSQL-compatible SQL functions.\n- The source table columns are case-sensitive and must be referenced with double quotes, e.g., \"District_Name\". When renaming columns, always use the correct quoted column name from the source.\n- Do not end the SQL with a semicolon.\n"""
            )
        )
        sql_code = (sql_prompt | llm).invoke({
            "schema_text": schema_text,
            "model_name": model_name,
            "source_schema": source_schema,
            "source_table": source_table
        })
        if hasattr(sql_code, "content"):
            sql_code = sql_code.content
        sql_code = sql_code.strip().strip("`")
        if sql_code.startswith("sql"):
            sql_code = sql_code[len("sql"):].lstrip()

        # Prompt for YAML
        yml_prompt = PromptTemplate(
            input_variables=["schema_text", "model_name"],
            template=(
                """
                You are a data engineer. Given the following table schema or DDL:\n\n{schema_text}\n\nGenerate a detailed dbt schema YAML file for a model named '{model_name}'.\n- Include rich descriptions for each column.\n- Use best practices for dbt schema.yml.\n- Do not include any explanations, only output the YAML.\n"""
            )
        )
        yml_code = (yml_prompt | llm).invoke({"schema_text": schema_text, "model_name": model_name})
        if hasattr(yml_code, "content"):
            yml_code = yml_code.content
        yml_code = yml_code.strip().strip("`")
        if yml_code.startswith("yaml"):
            yml_code = yml_code[len("yaml"):].lstrip()

        # Write files
        models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "semantic_layer_dbt", "models")
        os.makedirs(models_dir, exist_ok=True)
        sql_path = os.path.join(models_dir, f"{model_name}.sql")
        yml_path = os.path.join(models_dir, f"{model_name}.yml")
        with open(sql_path, "w") as f:
            f.write(sql_code)
        with open(yml_path, "w") as f:
            f.write(yml_code)

        return {
            "model_sql_path": sql_path,
            "model_yml_path": yml_path,
            "model_sql": sql_code,
            "model_yml": yml_code
        }

    def describe(self) -> str:
        return "dbtModelGeneratorAgent: Uses LLM to generate detailed dbt model SQL and YAML from schema text input, with source table control." 