# 后续升级路线

1. 将 TF-IDF 检索升级为 sentence-transformers embedding + FAISS，并为每个 chunk 保存页码与元数据。
2. 增加 PPTX、DOCX、TXT、图片 OCR 等课程资料解析器。
3. 使用真正的 LLM tool-calling 规划工具调用，并由 Web Agent 通过 MCP Client 连接独立 MCP Server。
4. 加入账号、课程/班级、学生学习档案、教师管理端与数据隔离。
5. 加入题库、自动/人工评分、错题本、学习进度图表。
6. 为耗时任务加入 SSE 状态流、任务队列、超时控制与取消操作。
7. 添加单元测试、文件大小限制、恶意文件防护、日志、数据库迁移和部署配置。
