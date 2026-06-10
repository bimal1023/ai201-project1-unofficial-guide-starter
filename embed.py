"""
Embedding and vector store pipeline.
Reads all .txt files from documents/, chunks them, embeds with all-MiniLM-L6-v2,
and stores in a local ChromaDB collection.
Run:  python embed.py
"""

import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "unofficial_guide"

# ~400 tokens * ~4 chars/token = 1600 chars; overlap 50 tokens * 4 = 200 chars
CHUNK_CHARS = 1600
OVERLAP_CHARS = 200


def chunk_text(text: str, chunk_chars: int = CHUNK_CHARS, overlap_chars: int = OVERLAP_CHARS) -> "list[str]":
    """
    Recursively split text at paragraph → sentence → word boundaries.
    Returns a list of non-empty string chunks.
    """
    paragraphs = re.split(r"\n\n+", text.strip())
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)

        if current and current_len + para_len + 2 > chunk_chars:
            chunk = "\n\n".join(current)
            chunks.append(chunk)

            # Build overlap window from tail of the current chunk
            overlap_paras: list[str] = []
            overlap_len = 0
            for p in reversed(current):
                if overlap_len + len(p) + 2 <= overlap_chars:
                    overlap_paras.insert(0, p)
                    overlap_len += len(p) + 2
                else:
                    break
            current = overlap_paras
            current_len = overlap_len

        current.append(para)
        current_len += para_len + 2

    if current:
        chunks.append("\n\n".join(current))

    # Sub-split any chunk that is still > 2× the target (edge case: one giant paragraph)
    result = []
    for chunk in chunks:
        if len(chunk) > chunk_chars * 2:
            # Hard split on sentences
            sentences = re.split(r"(?<=[.!?])\s+", chunk)
            sub, sub_len = [], 0
            for sent in sentences:
                if sub and sub_len + len(sent) > chunk_chars:
                    result.append(" ".join(sub))
                    sub = sub[-3:]  # keep last 3 sentences as overlap
                    sub_len = sum(len(s) for s in sub)
                sub.append(sent)
                sub_len += len(sent)
            if sub:
                result.append(" ".join(sub))
        else:
            result.append(chunk)

    return [c for c in result if len(c.split()) >= 15]


def parse_source_header(text: str) -> tuple[str, str, str, str]:
    """Return (description, url, date, body) parsed from the file header."""
    lines = text.split("\n")
    description = url = date = ""
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("SOURCE:"):
            description = line[len("SOURCE:"):].strip()
        elif line.startswith("URL:"):
            url = line[len("URL:"):].strip()
        elif line.startswith("DATE:"):
            date = line[len("DATE:"):].strip()
        elif line.startswith("=" * 10):
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:]).strip()
    return description, url, date, body


def load_documents(docs_dir: str) -> list[dict]:
    """Load all .txt files from docs_dir (skipping stubs with < 100 words of body)."""
    docs = []
    for fname in sorted(os.listdir(docs_dir)):
        if not fname.endswith(".txt") or fname == ".gitkeep":
            continue
        path = os.path.join(docs_dir, fname)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        description, url, date, body = parse_source_header(raw)
        word_count = len(body.split())
        if word_count < 100:
            print(f"  [skip stub] {fname} — only {word_count} words in body")
            continue
        docs.append({
            "filename": fname,
            "description": description,
            "url": url,
            "date": date,
            "body": body,
        })
    return docs


def build_collection(force_rebuild: bool = False) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    if force_rebuild:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection, client


def main(force_rebuild: bool = False):
    print("Loading embedding model (all-MiniLM-L6-v2)…")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"\nLoading documents from {DOCS_DIR}/…")
    docs = load_documents(DOCS_DIR)
    print(f"  Loaded {len(docs)} documents")

    if not docs:
        print("ERROR: No documents found. Run python ingest.py first.")
        return

    collection, _ = build_collection(force_rebuild=force_rebuild)

    # Skip rebuild if already populated and not forced
    if collection.count() > 0 and not force_rebuild:
        print(f"\nCollection '{COLLECTION_NAME}' already has {collection.count()} chunks.")
        print("Use force_rebuild=True or delete chroma_db/ to re-embed.")
        return

    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc["body"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc['filename']}__chunk_{i:04d}",
                "text": chunk,
                "source_file": doc["filename"],
                "source_desc": doc["description"],
                "source_url": doc["url"],
                "source_date": doc["date"],
            })
        print(f"  {doc['filename']}: {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")

    print("\nEmbedding chunks…")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True, convert_to_list=True)

    print("\nStoring in ChromaDB…")
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            embeddings=embeddings[i : i + batch_size],
            metadatas=[
                {
                    "source_file": c["source_file"],
                    "source_desc": c["source_desc"],
                    "source_url": c["source_url"],
                    "source_date": c["source_date"],
                }
                for c in batch
            ],
        )

    print(f"\nDone. Collection '{COLLECTION_NAME}' now has {collection.count()} chunks.")

    # Print 5 sample chunks for verification
    print("\n--- 5 sample chunks ---")
    sample = all_chunks[:5]
    for s in sample:
        preview = s["text"][:200].replace("\n", " ")
        print(f"[{s['id']}]\n  {preview}…\n")


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    main(force_rebuild=force)
