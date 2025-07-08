import os
import psycopg2
from typing import Dict, Any
from dotenv import load_dotenv

class DDLExtractionAgent:
    """
    Extracts the CREATE TABLE DDL for a given table in PostgreSQL (public schema).
    Input:
      {
        'table_name': str  # Table name (no schema prefix)
      }
    Output:
      {
        'table_name': str,
        'ddl': str
      }
    """
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        load_dotenv()
        table_name = input_data['table_name']
        db_params = {
            'host': os.getenv('PGHOST', 'localhost'),
            'port': int(os.getenv('PGPORT', 5432)),
            'user': os.getenv('PGUSER', 'postgres'),
            'password': os.getenv('PGPASSWORD', ''),
            'dbname': os.getenv('PGDATABASE', 'postgres'),
        }
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        # Use pg_get_tabledef or pg_dump to get DDL. We'll use pg_get_tabledef if available, else reconstruct.
        # Standard way: use pg_get_tabledef (Postgres 15+), else use pg_get_tabledef from extension, else fallback.
        try:
            cur.execute("SELECT pg_get_tabledef(%s::regclass)", (f'public.{table_name}',))
            ddl = cur.fetchone()[0]
        except Exception:
            conn.rollback()
            # Fallback: reconstruct DDL from information_schema
            cur.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            cols = cur.fetchall()
            col_defs = []
            for name, typ, nullable in cols:
                null_str = '' if nullable == 'NO' else ' NULL'
                col_defs.append(f'"{name}" {typ.upper()}{null_str}')
            ddl = f'CREATE TABLE public."{table_name}" (\n    ' + ',\n    '.join(col_defs) + '\n);'
        cur.close()
        conn.close()
        return {'table_name': table_name, 'ddl': ddl} 