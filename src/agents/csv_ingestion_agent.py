import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from typing import Dict, Any
from dotenv import load_dotenv

class CSVIngestionAgent:
    """
    Ingests a CSV into PostgreSQL:
      - Infers schema with pandas
      - Creates table in public schema (errors if table exists)
      - Loads data
    Input:
      {
        'csv_path': str,         # Path to CSV file
        'table_name': str         # Target table name (no schema prefix)
      }
    Output:
      {
        'table_name': str,
        'schema': list  # List of dicts: [{'name': col, 'type': pg_type}]
      }
    """
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        load_dotenv()
        csv_path = input_data['csv_path']
        table_name = input_data['table_name']
        # DB connection params from env
        db_params = {
            'host': os.getenv('PGHOST', 'localhost'),
            'port': int(os.getenv('PGPORT', 5432)),
            'user': os.getenv('PGUSER', 'postgres'),
            'password': os.getenv('PGPASSWORD', ''),
            'dbname': os.getenv('PGDATABASE', 'postgres'),
        }
        df = pd.read_csv(csv_path)
        # Infer schema
        def pandas_to_pg_type(dtype):
            if pd.api.types.is_integer_dtype(dtype):
                return 'BIGINT'
            if pd.api.types.is_float_dtype(dtype):
                return 'DOUBLE PRECISION'
            if pd.api.types.is_bool_dtype(dtype):
                return 'BOOLEAN'
            if pd.api.types.is_datetime64_any_dtype(dtype):
                return 'TIMESTAMP'
            return 'TEXT'
        columns = [(col, pandas_to_pg_type(df[col].dtype)) for col in df.columns]
        schema = [{'name': col, 'type': typ} for col, typ in columns]
        # Connect to DB
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        # Check if table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = %s
            )
        """, (table_name,))
        if cur.fetchone()[0]:
            cur.close()
            conn.close()
            raise Exception(f"Table '{table_name}' already exists in public schema.")
        # Create table
        col_defs = ', '.join([f'"{col}" {typ}' for col, typ in columns])
        create_sql = f'CREATE TABLE dbt_db.public."{table_name}" ({col_defs});'
        cur.execute(create_sql)
        # Copy data
        # Write to temp CSV for COPY
        temp_csv = csv_path if csv_path.endswith('.csv') else csv_path + '.tmp.csv'
        if temp_csv != csv_path:
            df.to_csv(temp_csv, index=False)
        with open(temp_csv, 'r') as f:
            next(f)  # skip header
            cur.copy_expert(sql.SQL(f"COPY public.\"{table_name}\" FROM STDIN WITH CSV"), f)
        conn.commit()
        cur.close()
        conn.close()
        return {'table_name': table_name, 'schema': schema} 