# 知学 AI：课程学习助手 Web 项目

根据提供的《AI科研助手 Web 平台》文档架构改造为面向课程学习的项目。前端 Vue 3 + Vite，后端 FastAPI，包含课程 PDF 上传与 RAG 检索、AI 课程问答、知识点总结、练习题、复习卡片、7 天学习计划、CSV 描述统计、Markdown 报告，以及可选的 MCP stdio 工具服务器。

> **运行说明：** 默认 `LLM_PROVIDER=mock`，不需要 API Key 即可启动并测试上传、检索和界面流程；Mock 模式不是实际大模型，生成内容会提示其演示属性。配置兼容 OpenAI Chat Completions API 的服务后才会启用真实 LLM。RAG 当前采用 TF-IDF 字符 n-gram，轻量、无需下载嵌入模型；后续可替换为 sentence-transformers + FAISS。当前没有登录/多用户隔离，建议仅在本机或可信开发环境运行。

## 1. 项目结构

```text
course-ai-assistant/
├── backend/
│   ├── main.py                 # FastAPI 应用
│   ├── config.py               # 配置与存储路径
│   ├── llm.py                  # Mock / OpenAI-compatible LLM
│   ├── api/routes.py           # API：聊天、PDF、学习材料、CSV、报告
│   ├── agent/agent.py          # 学习 Agent
│   ├── rag/knowledge.py        # PDF解析、切块、TF-IDF检索
│   ├── tool_registry/tools.py  # 学习工具注册表
│   ├── storage/papers/         # PDF与索引
│   ├── storage/datasets/       # CSV
│   └── storage/reports/        # Markdown报告
├── frontend/                   # Vue 3 + Vite
├── mcp_server/server.py        # 可选的真实 MCP stdio server
├── scripts/start.sh            # 同时启动前后端
└── docs/ROADMAP.md
```

## 2. 环境要求

- Python 3.11（推荐）
- Node.js 20+ 与 npm
- macOS、Linux 或 Windows（Windows 建议使用 WSL）

## 3. 启动后端

```bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env   # Windows 可手动复制
uvicorn main:app --reload --port 8000
```

后端地址：`http://localhost:8000`，交互式 API 文档：`http://localhost:8000/docs`。

## 4. 启动前端

另开终端：

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。Vite 会将 `/api` 请求代理到 `http://127.0.0.1:8000`。

也可以在项目根目录运行 `bash scripts/start.sh`（需要后端依赖和前端 npm 依赖已安装）。

## 5. 启用真实 LLM

编辑 `backend/.env`：

```env
LLM_PROVIDER=openai
LLM_API_KEY=在本机填写你的API密钥
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=填写你账户实际可用的模型名
```

重启后端生效。若使用其他兼容 OpenAI API 的服务，请修改 `LLM_BASE_URL`。不要将真实 API Key 上传到代码仓库或发送到聊天窗口。

## 6. 主要功能

1. **AI 学习问答**：输入问题，优先从已索引的 PDF 资料检索相关片段，并展示来源文件及片段编号。
2. **课程知识库**：上传 PDF，解析文本并建立本地检索索引。文本型 PDF 支持较好；扫描件需要先 OCR。
3. **学习材料生成**：知识点总结、5 道练习题（含答案解析）、复习卡片、7 天学习计划。
4. **数据练习分析**：上传 CSV，查看行数、列名、缺失值与描述性统计。
5. **学习报告**：保存 Markdown 报告并查看/下载。
6. **MCP 工具**：可选启动 `mcp_server/server.py`，提供课程知识搜索、文档列表、CSV 分析、报告保存工具。

## 7. 启动 MCP Server（可选）

在已安装后端依赖的环境中执行：

```bash
pip install "mcp[cli]"
cd backend
python ../mcp_server/server.py
```

这是独立的 stdio MCP 服务，供兼容 MCP 的客户端配置调用。Web Agent 当前直接调用内部学习逻辑；并未声称已把 Web Agent 自动连接到该 MCP Server。

## 8. 重要边界

- 项目是可运行的教学 MVP，不是生产级 LMS。
- 没有用户登录、权限体系、云端部署或多用户数据隔离。
- 当前 RAG 为 TF-IDF 检索，不是语义向量检索；答案质量依赖 PDF 文本质量及检索相关性。
- Mock 模式主要用于验证流程，不能把它的输出当成真实 LLM 结果。
- CSV 只做通用描述统计，不会自动推断所有课程指标的专业含义。
