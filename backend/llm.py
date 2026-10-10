from config import LLM_PROVIDER, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

async def generate(system: str, user: str) -> str:
    if LLM_PROVIDER == "openai":
        if not (LLM_API_KEY and LLM_MODEL):
            raise RuntimeError("LLM_PROVIDER=openai 时，请在 backend/.env 中配置 LLM_API_KEY 和 LLM_MODEL")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            temperature=0.4,
        )
        return response.choices[0].message.content or "模型没有返回文本。"
    # A predictable offline mode so students can run the project before configuring a model.
    return "【本地演示模式】\n\n" + user[:5000] + "\n\n当前使用本地演示模式，尚未连接真实大语言模型。配置 backend/.env 中的 LLM_PROVIDER、LLM_API_KEY 和 LLM_MODEL 后即可启用模型生成。请结合课程资料核对答案。"
