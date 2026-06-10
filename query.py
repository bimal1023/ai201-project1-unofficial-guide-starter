"""
Retrieval and grounded generation.
Provides:
  retrieve(query, k=5)  → list of chunk dicts with text + metadata
  ask(question)         → {"answer": str, "sources": list[str], "chunks": list}
"""

import os
from typing import Optional
import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "unofficial_guide"
GROQ_MODEL = "llama-3.3-70b-versatile"

_model: Optional[SentenceTransformer] = None
_collection: Optional[chromadb.Collection] = None
_groq: Optional[Groq] = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection


def _get_groq() -> Groq:
    global _groq
    if _groq is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment or .env file")
        _groq = Groq(api_key=api_key)
    return _groq


def retrieve(query: str, k: int = 5) -> list[dict]:
    """
    Embed the query and return the top-k most relevant chunks with metadata.
    Each returned dict has keys: text, source_file, source_desc, source_url,
    source_date, distance.
    """
    model = _get_model()
    collection = _get_collection()

    query_embedding = model.encode([query], convert_to_list=True)[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source_file": meta.get("source_file", ""),
            "source_desc": meta.get("source_desc", ""),
            "source_url": meta.get("source_url", ""),
            "source_date": meta.get("source_date", ""),
            "distance": round(dist, 4),
        })
    return chunks


SYSTEM_PROMPT = """\
You are a knowledgeable guide helping students break into AI/ML careers.
You MUST answer ONLY using the information in the document excerpts provided below.
Do NOT use any knowledge from your training data — if the excerpts don't contain
enough information to answer the question, say exactly:
"I don't have enough information in my documents to answer that question."

Rules:
1. Every factual claim must be supported by at least one of the provided excerpts.
2. Cite your sources inline using the format [Source: <source description>] immediately
   after each claim.
3. If multiple excerpts support a claim, cite all of them.
4. Do NOT speculate, extrapolate, or add context beyond what the excerpts contain.
5. Keep answers focused and concrete — students need actionable advice, not vague platitudes.
"""


def build_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        date_note = f" (published {c['source_date']})" if c["source_date"] else ""
        header = f"[Excerpt {i}] {c['source_desc']}{date_note}"
        parts.append(f"{header}\n{c['text']}")
    return "\n\n---\n\n".join(parts)


def ask(question: str, k: int = 5) -> dict:
    """
    Full RAG pipeline: retrieve relevant chunks, then generate a grounded answer.
    Returns {"answer": str, "sources": list[str], "chunks": list[dict]}.
    """
    chunks = retrieve(question, k=k)

    if not chunks:
        return {
            "answer": "No documents are loaded. Please run python embed.py first.",
            "sources": [],
            "chunks": [],
        }

    context = build_context(chunks)
    user_message = f"""Document excerpts:

{context}

---

Question: {question}

Answer (cite sources inline, use only the excerpts above):"""

    groq_client = _get_groq()
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    answer = response.choices[0].message.content.strip()

    # Deduplicated source list (description + URL)
    seen = set()
    sources = []
    for c in chunks:
        key = c["source_url"] or c["source_desc"]
        if key not in seen:
            seen.add(key)
            label = c["source_desc"]
            if c["source_url"]:
                label += f" — {c['source_url']}"
            if c["source_date"]:
                label += f" ({c['source_date']})"
            sources.append(label)

    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Do I need a Master's degree to get an ML engineering role at a top company?"
    )
    print(f"\nQuestion: {question}\n")
    result = ask(question)
    print("Answer:")
    print(result["answer"])
    print("\nSources:")
    for s in result["sources"]:
        print(f"  • {s}")
    print("\nRetrieved chunks (distances):")
    for c in result["chunks"]:
        print(f"  [{c['distance']:.4f}] {c['source_desc'][:60]}")
