from .payload import Payload


def new_sql_payload(sql: str) -> Payload:
    return Payload(
        type="executed_query",
        content={
            "sql": sql,
        }
    )
