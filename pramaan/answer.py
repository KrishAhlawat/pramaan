"""Retrieve -> generate an answer grounded in the chunks, with [file pN] citations."""
from .llm import chat
from .retrieve import dense_search

IDK = "I don't know based on the provided documents."

SYSTEM = f"""You answer questions using ONLY the numbered context chunks provided.
Rules:
- After every claim, cite its source in the form [file pN] exactly as shown in the chunk header.
- Do not use outside knowledge. Do not guess.
- If the context does not contain the answer, reply exactly: {IDK}
- Reply in the same language/style as the question (English, Hindi, or Hinglish).
- Be concise."""


def label(chunk: dict) -> str:
    return f"[{chunk['source']} p{chunk['page']}]"


def build_context(chunks: list[dict]) -> str:
    return "\n\n".join(f"{label(c)}\n{c['content']}" for c in chunks)


def answer(question: str, k: int = 5) -> dict:
    chunks = dense_search(question, k=k)
    if not chunks:
        return {"answer": IDK, "chunks": []}
    user = f"Context:\n{build_context(chunks)}\n\nQuestion: {question}"
    text = chat([{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}])
    return {"answer": text, "chunks": chunks}
