CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id           BIGSERIAL PRIMARY KEY,
    source       TEXT    NOT NULL,          -- file name, e.g. policy.pdf
    page         INTEGER NOT NULL DEFAULT 1,
    chunk_index  INTEGER NOT NULL,
    content      TEXT    NOT NULL,
    embedding    vector(1024) NOT NULL,     -- bge-m3 dimension
    tsv          tsvector GENERATED ALWAYS AS (to_tsvector('simple', content)) STORED,
    UNIQUE (source, page, chunk_index)
);

-- dense retrieval (cosine)
CREATE INDEX IF NOT EXISTS chunks_embedding_idx
    ON chunks USING hnsw (embedding vector_cosine_ops);

-- keyword retrieval (used later for hybrid search)
CREATE INDEX IF NOT EXISTS chunks_tsv_idx
    ON chunks USING gin (tsv);
