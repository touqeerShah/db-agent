from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
import psycopg2

def execute_query(query: str) -> List[Dict[str, Any]]:
    try:
        conn = psycopg2.connect(
            dbname="ai",
            user="ai",
            password="YWkxMjM0NTY3ODk=",  # Decoded from base64: YWkxMjM0NTY3ODk=
            host="localhost",
            port="5432"
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            if cursor.description:
                result = [dict(row) for row in cursor.fetchall()]  # <-- FIX HERE
            else:
                result = []
            conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return []




def get_role_permissions(role: str) -> List[Dict[str, Any]]:
    try:
        conn = psycopg2.connect(
            dbname="ai",
            user="ai",
            password="YWkxMjM0NTY3ODk=",
            host="localhost",
            port="5432"
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT table_name, can_select, can_insert, can_update, can_delete
                FROM permissions
                WHERE role = %s
            """, (role,))
            permissions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return permissions
    except Exception as e:
        print(f"Error fetching role permissions: {e}")
        return []