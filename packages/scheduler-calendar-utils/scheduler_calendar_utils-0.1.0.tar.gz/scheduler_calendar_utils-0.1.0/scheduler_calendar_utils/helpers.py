# helpers.py

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from flask import jsonify

def query_db(pool: Engine, query: str, params: dict = None, is_select: bool = True):
    """
    Execute a query on the MySQL database using SQLAlchemy Engine.

    Parameters:
        pool (Engine): SQLAlchemy Engine for database connection.
        query (str): SQL query to be executed.
        params (dict, optional): Query parameters. Defaults to None.
        is_select (bool): Whether the query is a SELECT. Defaults to True.

    Returns:
        list[dict] if SELECT query; bool for modification queries.
    """
    compiled_query = text(query)
    with pool.connect() as connection:
        result = connection.execute(compiled_query, params or {})
        if is_select:
            results = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in results]
        else:
            connection.commit()
            return result.rowcount > 0  # Return True if any row was affected


def generate_response(trace_id: str, status_code: int, response_body: dict, additional_heads: dict = None):
    """
    Generate a structured HTTP response with trace ID header.

    Parameters:
        trace_id (str): Unique identifier for tracing.
        status_code (int): HTTP status code.
        response_body (dict): Body of the response.
        additional_heads (dict, optional): Any additional headers to include.

    Returns:
        Flask Response: JSON response with headers.
    """
    response = jsonify(response_body)
    response.status_code = status_code
    response.headers['X-Trace-ID'] = trace_id

    if additional_heads:
        for k, v in additional_heads.items():
            response.headers[k] = v

    return response