from fastapi import APIRouter
from ..db import get_conn

router = APIRouter()

@router.get("")
def people():
    with get_conn() as conn:
        rows = conn.execute("""
        SELECT p.name, COUNT(s.id)
        FROM people p
        LEFT JOIN samples s ON s.person_id = p.id
        GROUP BY p.id
        """).fetchall()

    return [{"name": r[0], "samples": r[1]} for r in rows]
