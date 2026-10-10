"""Optional real MCP server exposing course-learning tools over stdio.
Run from backend directory with: python ../mcp_server/server.py
Install optional dependency: pip install 'mcp[cli]'
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from rag.knowledge import search, list_documents
from tool_registry.tools import analyze_csv, save_report

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("缺少 MCP SDK，请执行 pip install 'mcp[cli]'") from exc

server = FastMCP("course-learning-tools")
@server.tool()
def search_course_knowledge(query: str) -> list[dict]:
    """Search indexed PDF course materials and return relevant chunks with source names."""
    return search(query, top_k=5)
@server.tool()
def list_course_documents() -> list[dict]:
    """List course PDF files indexed in the local knowledge base."""
    return list_documents()
@server.tool()
def analyze_uploaded_csv(filename: str) -> dict:
    """Analyze an uploaded course/exercise CSV file: dimensions, missing values and descriptive statistics."""
    return analyze_csv(filename)
@server.tool()
def save_learning_report(title: str, markdown_content: str) -> dict:
    """Save a Markdown study report in the reports directory."""
    return save_report(title, markdown_content)
if __name__ == "__main__": server.run(transport="stdio")
