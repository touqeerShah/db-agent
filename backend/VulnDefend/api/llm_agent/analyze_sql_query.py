import re
from typing import Tuple, List

def analyze_sql_query(sql: str) -> Tuple[str, List[str]]:
    """
    Returns the operation type (select, insert, update, delete) and list of table names.
    """
    sql_lower = sql.lower().strip()
    operation = "unknown"
    if sql_lower.startswith("select"):
        operation = "select"
    elif sql_lower.startswith("insert"):
        operation = "insert"
    elif sql_lower.startswith("update"):
        operation = "update"
    elif sql_lower.startswith("delete"):
        operation = "delete"

    tables = set()

    if operation == "select":
        tables.update(re.findall(r'\bfrom\s+(\w+)', sql_lower))
        tables.update(re.findall(r'\bjoin\s+(\w+)', sql_lower))
    elif operation == "insert":
        match = re.search(r'\binsert\s+into\s+(\w+)', sql_lower)
        if match:
            tables.add(match.group(1))
    elif operation == "update":
        match = re.search(r'\bupdate\s+(\w+)', sql_lower)
        if match:
            tables.add(match.group(1))
    elif operation == "delete":
        match = re.search(r'\bfrom\s+(\w+)', sql_lower)
        if match:
            tables.add(match.group(1))

    return operation, list(tables)
