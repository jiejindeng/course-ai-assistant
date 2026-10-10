from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS
from api.routes import router

app = FastAPI(title="AI 课程学习助手", description="课程资料 RAG、AI 问答、学习材料生成与 CSV 分析", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
@app.get("/")
def root(): return {"message":"AI 课程学习助手 API", "docs":"/docs", "health":"/api/health"}
