"""Dense (vector) retrieval from pgvector. Baseline for the evals; hybrid + rerank come later."""
from .db import connect
from .embed import embed


def dense_search(query: str, k: int = 5) -> list[dict]:
    qvec = embed([query])[0]
    with connect() as conn:
        rows = conn.execute(
            "SELECT source, page, chunk_index, content, 1 - (embedding <=> %s) AS score "
            "FROM chunks ORDER BY embedding <=> %s LIMIT %s",
            (qvec, qvec, k),
        ).fetchall()
    return [
        {"source": r[0], "page": r[1], "chunk_index": r[2], "content": r[3], "score": float(r[4])}
        for r in rows
    ]
