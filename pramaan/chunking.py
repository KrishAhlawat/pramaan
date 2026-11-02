"""Load documents and split them into overlapping chunks, keeping (source, page)."""
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from .config import CHUNK_OVERLAP, CHUNK_WORDS

SUPPORTED = {".pdf", ".md", ".txt"}


@dataclass
class Chunk:
    source: str
    page: int
    chunk_index: int
    content: str


def load_pages(path: Path) -> list[tuple[int, str]]:
    """Return [(page_number, text)]. Non-PDF files are treated as one page."""
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    return [(1, path.read_text(encoding="utf-8", errors="ignore"))]


def split_words(text: str, size: int = CHUNK_WORDS, overlap: int = CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    if not words:
        return []
    step = max(size - overlap, 1)
    chunks = []
    for start in range(0, len(words), step):
        piece = words[start : start + size]
        chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks


def chunk_file(path: Path) -> list[Chunk]:
    out: list[Chunk] = []
    for page, text in load_pages(path):
        for idx, piece in enumerate(split_words(text)):
            out.append(Chunk(source=path.name, page=page, chunk_index=idx, content=piece))
    return out
