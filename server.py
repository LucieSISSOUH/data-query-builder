from mcp.server.fastmcp import FastMCP
from db_helper import create_db, load_csv_to_table
import sqlite3

mcp = FastMCP("data-query-builder")
conn = create_db()

# Historique des requêtes exécutées pendant la session
query_history = []

# Mots SQL interdits pour éviter les requêtes dangereuses
FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "ALTER", "INSERT", "UPDATE"]


@mcp.tool()
def load_csv(file_path: str, table_name: str) -> dict:
    """Load a CSV file into a SQLite table with auto-detected column types.
    Use this tool first before running any queries.
    file_path must be the absolute path to the CSV file.
    Returns the table name, columns with types, and row count.
    """
    try:
        result = load_csv_to_table(conn, file_path, table_name)
        return {"success": True, "details": result}
    except FileNotFoundError:
        return {"success": False, "error": f"File not found: {file_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def list_tables() -> dict:
    """List all tables currently loaded in the database with their row counts.
    Use this to check what data is available before running queries.
    """
    try:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = []
        for row in cursor.fetchall():
            table_name = row[0]
            count = conn.execute(f'SELECT COUNT(*) FROM "{table_name}"').fetchone()[0]
            tables.append({"table": table_name, "row_count": count})
        return {"tables": tables}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def describe_schema() -> dict:
    """Describe all tables and their columns in the database."""
    try:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        schema = {}

        for table_name in tables:
            pragma_cursor = conn.execute(f'PRAGMA table_info("{table_name}")')
            columns = []

            for col in pragma_cursor.fetchall():
                columns.append({
                    "column": col[1],
                    "type": col[2]
                })

            schema[table_name] = columns

        return {"schema": schema}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def run_query(sql: str, limit: int = 50) -> dict:
    """Run a safe SQL query with a row limit."""
    try:
        sql_upper = sql.upper()

        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in sql_upper:
                return {
                    "success": False,
                    "error": f"Forbidden SQL keyword detected: {keyword}"
                }

        sql_clean = sql.strip().rstrip(";")

        # Ajoute LIMIT seulement si la requête n'en contient pas déjà un
        if "LIMIT" not in sql_upper:
            sql_clean = f"{sql_clean} LIMIT {limit}"

        cursor = conn.execute(sql_clean)
        rows = [dict(row) for row in cursor.fetchall()]

        query_history.append(sql)

        return {
            "success": True,
            "row_count": len(rows),
            "rows": rows
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_statistics(table_name: str, column: str) -> dict:
    """Return count, min, max, average and null count for a column."""
    try:
        query = f"""
        SELECT
            COUNT("{column}") AS count,
            MIN("{column}") AS min,
            MAX("{column}") AS max,
            AVG("{column}") AS avg,
            SUM(CASE WHEN "{column}" IS NULL THEN 1 ELSE 0 END) AS nulls
        FROM "{table_name}"
        """

        cursor = conn.execute(query)
        result = cursor.fetchone()

        return {
            "table": table_name,
            "column": column,
            "count": result["count"],
            "min": result["min"],
            "max": result["max"],
            "avg": result["avg"],
            "nulls": result["nulls"]
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.resource("db://schema")
def get_schema_resource():
    """Schéma actuel de la base de données."""
    return describe_schema()


@mcp.resource("db://query-history")
def get_query_history_resource():
    """Historique des requêtes exécutées cette session."""
    return {"queries": query_history}


@mcp.tool()
def query_data(sql: str) -> dict:
    """Execute a SQL SELECT query on the loaded data.
    Returns the query results as a list of dictionaries."""
    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        return {"results": [dict(row) for row in rows]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()

