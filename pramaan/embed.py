"""Local multilingual embeddings (bge-m3, 1024-dim, handles Hinglish)."""
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from .config import EMBED_MODEL


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    return SentenceTransformer(EMBED_MODEL)


def embed(texts: list[str], batch_size: int = 16):
    return _model().encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,  # cosine similarity == dot product
        show_progress_bar=False,
    )
