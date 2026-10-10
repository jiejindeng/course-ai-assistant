from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pathlib import Path
import shutil, pandas as pd
from config import PAPERS_DIR, DATASETS_DIR, REPORTS_DIR
from rag.knowledge import index_file, list_documents, search
from agent.agent import answer_question, create_study_material
from tool_registry.tools import analyze_csv, save_report

router = APIRouter(prefix="/api")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    course: str = "通用课程"
class MaterialRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=300)
    kind: str = "summary"
    level: str = "初学者"
class ReportRequest(BaseModel):
    title: str
    content: str

@router.get("/health")
def health(): return {"status":"ok","app":"Course AI Assistant"}

@router.post("/chat")
async def chat(req: ChatRequest):
    try: return await answer_question(req.message, req.course)
    except Exception as e: raise HTTPException(500, str(e))

@router.post("/papers/upload")
async def upload_paper(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf": raise HTTPException(400,"目前只支持 PDF 课程资料")
    safe = Path(file.filename).name
    if len(safe) > 180: raise HTTPException(400,"文件名过长")
    path = PAPERS_DIR / safe
    with path.open("wb") as out: shutil.copyfileobj(file.file, out)
    try: info = index_file(path)
    except Exception as e:
        path.unlink(missing_ok=True)
        raise HTTPException(400, f"PDF 解析失败：{e}")
    return {"status":"indexed", **info}

@router.get("/papers")
def papers(): return {"items":list_documents()}

@router.post("/knowledge/search")
def knowledge_search(q: str): return {"items":search(q, top_k=6)}

@router.post("/study-material")
async def study_material(req: MaterialRequest):
    if req.kind not in {"summary","quiz","flashcards","plan"}: raise HTTPException(400,"不支持的学习材料类型")
    try: return await create_study_material(req.kind, req.topic, req.level)
    except Exception as e: raise HTTPException(500,str(e))

@router.post("/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".csv": raise HTTPException(400,"目前只支持 CSV 文件")
    path = DATASETS_DIR / Path(file.filename).name
    with path.open("wb") as out: shutil.copyfileobj(file.file,out)
    try:
        df = pd.read_csv(path)
    except Exception as e:
        path.unlink(missing_ok=True); raise HTTPException(400,f"CSV 读取失败：{e}")
    return {"filename":path.name,"rows":len(df),"columns":list(df.columns)}

@router.get("/datasets")
def datasets(): return {"items":[{"filename":p.name,"bytes":p.stat().st_size} for p in sorted(DATASETS_DIR.glob("*.csv"))]}

@router.get("/datasets/{filename}/analyze")
def dataset_analysis(filename: str):
    try: return analyze_csv(filename)
    except FileNotFoundError as e: raise HTTPException(404,str(e))
    except Exception as e: raise HTTPException(400,str(e))

@router.post("/reports")
def create_report(req: ReportRequest): return save_report(req.title, req.content)

@router.get("/reports")
def reports(): return {"items":[{"filename":p.name,"bytes":p.stat().st_size} for p in sorted(REPORTS_DIR.glob("*.md"), key=lambda x:x.stat().st_mtime, reverse=True)]}

@router.get("/reports/{filename}")
def download_report(filename: str):
    path = (REPORTS_DIR / Path(filename).name).resolve()
    if not path.is_relative_to(REPORTS_DIR.resolve()) or not path.exists(): raise HTTPException(404,"报告不存在")
    return FileResponse(path, media_type="text/markdown", filename=path.name)
