from llm import generate
from rag.knowledge import search

SYSTEM = "你是一名耐心、严谨的课程学习助手。优先依据给出的课程资料回答；资料不足时明确说明，不要编造教材出处。用中文回答，结构清楚，适合初学者。解释概念时尽量包含定义、直观理解、例子和常见误区。"

async def answer_question(question: str, course: str = "通用课程"):
    hits = search(question, top_k=4)
    if hits:
        context = "\n\n".join(f"[资料：{h['filename']}，片段 {h['chunk_id']}，相关度 {h['score']}]\n{h['text']}" for h in hits)
    else:
        context = "当前知识库没有检索到明显相关的课程资料。请明确告知学生这一点。"
    prompt = f"课程：{course}\n学生问题：{question}\n\n检索到的课程资料：\n{context}\n\n请先依据资料回答，区分资料中的事实与补充解释。"
    result = await generate(SYSTEM, prompt)
    return {"answer": result, "sources": [{"filename":h["filename"],"chunk_id":h["chunk_id"],"score":h["score"],"excerpt":h["text"][:240]} for h in hits], "mode":"rag" if hits else "general"}

async def create_study_material(kind: str, topic: str, level: str = "初学者"):
    hits = search(topic, top_k=5)
    context = "\n\n".join(f"[{x['filename']}] {x['text']}" for x in hits) or "暂无相关课程资料，请说明内容可能不是来自用户上传的教材。"
    task = {
        "summary":"请生成课程知识点总结，包含核心概念、知识结构、关键术语、例子、常见误区和自测问题。",
        "quiz":"请生成 5 道练习题，混合选择题和简答题，先给题目，再给答案与解析，并标记考查知识点。",
        "flashcards":"请生成 8 张复习卡片，每张包含正面问题和背面答案。",
        "plan":"请制定一个 7 天学习计划，按每天的目标、学习任务、练习和复盘安排。",
    }.get(kind, "请帮助学生学习这个主题，给出结构化讲解和练习。")
    prompt = f"学习主题：{topic}\n学生水平：{level}\n任务：{task}\n课程资料：\n{context}\n请使用中文，并明确指出资料不足之处。"
    result = await generate(SYSTEM, prompt)
    return {"kind":kind,"topic":topic,"content":result,"sources":[{"filename":h["filename"],"chunk_id":h["chunk_id"]} for h in hits]}
