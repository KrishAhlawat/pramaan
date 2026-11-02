# pramaan

RAG over your own documents with **citations** and **evals**. Ask in English or Hinglish
("refund kitne din mein?"), get an answer grounded in retrieved chunks, each claim tagged
like `[policy.pdf p4]`. If nothing relevant is found, it says "I don't know".

Everything runs free: local bge-m3 embeddings + reranker, pgvector, Groq free tier for the LLM.

## Pipeline

docs -> chunks -> embeddings (pgvector) -> retrieve top-20 -> rerank -> generate with citations

## Quick start

```bash
cp .env.example .env              # add your Groq key later (needed for generation step)
docker compose up -d              # Postgres + pgvector, schema auto-applied
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# drop .pdf / .md / .txt files into data/docs/
python -m scripts.ingest
```

## Roadmap

- [x] Ingestion: chunk -> embed -> store
- [ ] Retrieval + answer (no citations)
- [ ] Citations + "I don't know" fallback
- [ ] Eval set (50-100 Qs) + baseline recall@5
- [ ] Hybrid search (BM25 + vectors) + reranking, log metric gains
- [ ] UI with clickable citations

## Results

| Version | recall@5 | faithfulness |
|---|---|---|
| baseline | - | - |
