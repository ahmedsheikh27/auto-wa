from agents import function_tool
from sqlalchemy import text
from app.db.session import engine


@function_tool(
    name_override="read_db",
    description_override=(
        "Execute a SELECT query on the database. "
        "Use this to fetch products, users, orders, collections, or any data. "
        "Always use parameterized queries for safety. "
        "Returns rows as a list of dicts."
    ),
)
async def read_db(query: str) -> str:
    """
    Execute a read-only SELECT query.

    Args:
        query: A valid SQL SELECT statement based on the schema provided.

    Returns:
        Query results as formatted text, or an error message.
    """
    print(f"\n[read_db] Executing: {query}")

    stripped = query.strip().upper()
    if not stripped.startswith("SELECT"):
        return "Error: read_db only allows SELECT queries. Use write_db for INSERT/UPDATE."

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()

            if not rows:
                return "No results found."

            output = []
            for i, row in enumerate(rows, start=1):
                row_dict = dict(row._mapping)
                output.append(f"{i}. {row_dict}")

            print(f"[read_db] Returned {len(rows)} rows")
            return "\n".join(output)

    except Exception as e:
        print(f"[read_db] Error: {e}")
        return f"Query error: {str(e)}"


@function_tool(
    name_override="write_db",
    description_override=(
        "Execute an INSERT or UPDATE query on the database. "
        "Use this to create orders, update statuses, add users, or any write operation. "
        "Only call this AFTER collecting all required info from the user and user has confirmed. "
        "Returns success status and affected row details."
    ),
)
async def write_db(query: str) -> str:
    """
    Execute a write query (INSERT or UPDATE).

    Args:
        query: A valid SQL INSERT or UPDATE statement based on the schema provided.

    Returns:
        Success message with result, or error message.
    """
    print(f"\n[write_db] Executing: {query}")

    stripped = query.strip().upper()
    if not (stripped.startswith("INSERT") or stripped.startswith("UPDATE")):
        return "Error: write_db only allows INSERT or UPDATE queries. Use read_db for SELECT."

    dangerous = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE"]
    for word in dangerous:
        if word in stripped:
            return f"Error: {word} operations are not allowed."

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            conn.commit()

            affected = result.rowcount
            lastrow_id = result.lastrowid if hasattr(result, "lastrowid") else None

            print(f"[write_db] Success. Rows affected: {affected}, Last ID: {lastrow_id}")

            response = f"Success. Rows affected: {affected}."
            if lastrow_id:
                response += f" New record ID: {lastrow_id}."

            return response

    except Exception as e:
        print(f"[write_db] Error: {e}")
        return f"Query error: {str(e)}"