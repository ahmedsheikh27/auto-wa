from sqlalchemy import inspect, text
from app.db.session import engine


def get_schema_description() -> str:
    """
    Introspects the connected database and returns a plain-text
    description of all tables, columns, types, and foreign keys.
    This is injected into the agent's instructions at startup.
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    if not table_names:
        return "No tables found in the connected database."

    lines = []
    lines.append("=== Database Schema ===\n")

    for table_name in table_names:
        lines.append(f"TABLE: {table_name}")

        columns = inspector.get_columns(table_name)
        for col in columns:
            col_type = str(col["type"])
            nullable = "nullable" if col.get("nullable", True) else "required"
            pk = " [PRIMARY KEY]" if col.get("primary_key") else ""
            lines.append(f"  - {col['name']} ({col_type}, {nullable}){pk}")

        fks = inspector.get_foreign_keys(table_name)
        if fks:
            for fk in fks:
                local_col = fk["constrained_columns"][0]
                ref_table = fk["referred_table"]
                ref_col = fk["referred_columns"][0]
                lines.append(f"  - FK: {local_col} → {ref_table}.{ref_col}")

        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 2"))
                rows = result.fetchall()
                if rows:
                    lines.append(f"  Sample rows ({len(rows)}):")
                    for row in rows:
                        lines.append(f"    {dict(row._mapping)}")
        except Exception:
            pass

        lines.append("") 

    lines.append("=== END SCHEMA ===")
    return "\n".join(lines)


def get_table_names() -> list[str]:
    inspector = inspect(engine)
    return inspector.get_table_names()