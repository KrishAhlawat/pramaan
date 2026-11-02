"""Ingest every doc in data/docs: chunk -> embed -> store in pgvector.

Usage:  python -m scripts.ingest [docs_dir]
Re-running replaces existing chunks for each file (idempotent).
"""
import sys
from pathlib import Path

from tqdm import tqdm

from pramaan.chunking import SUPPORTED, chunk_file
from pramaan.db import connect
from pramaan.embed import embed

BATCH = 32


def main(docs_dir: Path) -> None:
    files = sorted(p for p in docs_dir.rglob("*") if p.suffix.lower() in SUPPORTED)
    if not files:
        print(f"No .pdf/.md/.txt files found in {docs_dir}")
        return

    with connect() as conn:
        for path in files:
            chunks = chunk_file(path)
            if not chunks:
                print(f"skip {path.name}: no extractable text")
                continue

            conn.execute("DELETE FROM chunks WHERE source = %s", (path.name,))
            for i in tqdm(range(0, len(chunks), BATCH), desc=path.name):
                batch = chunks[i : i + BATCH]
                vectors = embed([c.content for c in batch])
                with conn.cursor() as cur:
                    cur.executemany(
                        "INSERT INTO chunks (source, page, chunk_index, content, embedding) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        [
                            (c.source, c.page, c.chunk_index, c.content, v)
                            for c, v in zip(batch, vectors)
                        ],
                    )
            conn.commit()
            print(f"{path.name}: {len(chunks)} chunks")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/docs"))
