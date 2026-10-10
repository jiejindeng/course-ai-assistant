"""Learning tools exposed through a small local registry; see mcp_server/server.py for MCP protocol server."""
from pathlib import Path
import pandas as pd
from config import DATASETS_DIR, REPORTS_DIR
from rag.knowledge import search

def search_knowledge(query: str):
    return search(query)

def analyze_csv(filename: str):
    path = (DATASETS_DIR / Path(filename).name).resolve()
    if not path.is_relative_to(DATASETS_DIR.resolve()) or not path.exists():
        raise FileNotFoundError("未找到数据文件，请先上传 CSV")
    df = pd.read_csv(path)
    return {"filename": path.name, "rows": len(df), "columns": list(df.columns), "missing": df.isna().sum().to_dict(), "describe": df.describe(include="all").fillna("").to_dict()}

def save_report(title: str, body: str):
    safe = "".join(c for c in title if c.isalnum() or c in "-_ ").strip().replace(" ", "_")[:60] or "learning_report"
    path = REPORTS_DIR / f"{safe}.md"
    path.write_text(body, encoding="utf-8")
    return {"filename": path.name, "path": str(path)}

TOOLS = {"search_knowledge": search_knowledge, "analyze_csv": analyze_csv, "save_report": save_report}
