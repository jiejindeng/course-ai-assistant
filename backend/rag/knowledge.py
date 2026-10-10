"""Small, persistent course-document RAG store using TF-IDF (no model download)."""
from pathlib import Path
import json, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
from config import PAPERS_DIR

INDEX_FILE = PAPERS_DIR / "knowledge_index.json"

def split_text(text: str, size: int = 900, overlap: int = 120):
    text = re.sub(r"\s+", " ", text).strip()
    if not text: return []
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text): break
        start = max(start + 1, end - overlap)
    return chunks

def read_index():
    if INDEX_FILE.exists():
        try: return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except Exception: pass
    return []

def write_index(items):
    INDEX_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

def extract_pdf(path: Path):
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)

def index_file(path: Path):
    text = extract_pdf(path)
    chunks = split_text(text)
    items = read_index()
    items = [x for x in items if x.get("filename") != path.name]
    items.extend({"filename": path.name, "chunk_id": i + 1, "text": chunk} for i, chunk in enumerate(chunks))
    write_index(items)
    return {"filename": path.name, "chunks": len(chunks), "characters": len(text)}

def search(query: str, top_k: int = 4):
    items = read_index()
    if not items: return []
    docs = [x["text"] for x in items]
    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4), max_features=60000)
    try:
        matrix = vectorizer.fit_transform(docs + [query])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    except ValueError: return []
    ids = scores.argsort()[::-1][:top_k]
    return [{**items[i], "score": round(float(scores[i]), 4)} for i in ids if scores[i] > 0]

def list_documents():
    seen = {}
    for item in read_index():
        seen[item["filename"]] = seen.get(item["filename"], 0) + 1
    return [{"filename": name, "chunks": count} for name, count in sorted(seen.items())]
