from sqlalchemy import text
import requests
import os
from backend.db.postgres import get_session
from backend.ai.memory_agent import Mem0Agent
from backend.ai.emotion_model import infer_emotion
from backend.ai.intimacy_model import compute_intimacy
from backend.ai.voice_tone import apply_tone
from backend.config import AGNO_API_BASE, AGNO_API_KEY

mem_agent = Mem0Agent()

def _local_vector_search(family_id, vector):
    session = next(get_session())
    vec_literal = "ARRAY[" + ",".join(str(float(x)) for x in vector) + "]::vector"
    sql = f"""
    SELECT me.memory_id AS memory_id, mr.content AS content, (me.embedding <=> {vec_literal}) AS distance
    FROM memory_embeddings me
    JOIN memory_records mr ON me.memory_id = mr.id
    WHERE mr.family_id = :family_id
    ORDER BY distance ASC
    LIMIT 5
    """
    result = session.execute(text(sql), {"family_id": family_id})
    return [{"memory_id": r.memory_id, "content": r.content, "score": 1 - r.distance} for r in result]

def generate_family_reply(user_id, family_id, member_role, query):
    query_vector = query_to_vector(query)
    memories = mem_agent.retrieve_context(family_id, query_vector)
    if not memories:
        memories = _local_vector_search(family_id, query_vector)
    emotions = infer_emotion(memories)
    intimacy = compute_intimacy(memories, interaction_count=len(memories))
    answer = generate_response(query, memories)
    answer_with_tone = apply_tone(answer, member_role)
    tone = member_role
    return {"answer": answer_with_tone, "memories": memories, "emotions": emotions, "intimacy": intimacy, "tone": tone}

def query_to_vector(text):
    return generate_embedding(text)

def build_rag_prompt(query: str, memories: list, tone: str):
    context = "\n".join([f"- {m['content']}" for m in memories])
    keywords = ",".join({w for m in memories for w in m.get("content", "").split() if len(w) > 1})
    prompt = f"""
你是用户的家庭成员（角色：{tone}）。
以下是与问题高度相关的家庭记忆，请务必在回答中引用：

【家庭记忆】
{context}

【关键词要求】
你的回答中必须出现家庭记忆相关的词语（例如：{keywords}）。
如果你发现记忆中有关于“潮汕”、“粿条”、“沙茶”、“童年爱吃的食物”等内容，你必须结合这些内容来构造回答。

【回答要求】
1. 必须引用家庭记忆
2. 必须引用关键词
3. 必须像真实的{tone}口吻（沉稳、温和、亲切）
4. 回答必须完整，不允许说“我不知道”

【用户问题】
{query}

请生成最终回答：
"""
    return prompt

def generate_response(query, memories=[], tone: str = "父亲"):
    prompt = build_rag_prompt(query, memories, tone)
    result = generate_llm(prompt)
    flat_mem = " ".join([m.get("content", "") for m in memories])
    mem_keywords = [w for w in flat_mem.split() if len(w) > 1]
    if mem_keywords and not any(k in result for k in mem_keywords):
        retry_prompt = f"""
你的上一轮回答未引用家庭记忆。
请重新生成，并强制引用以下关键内容：
{flat_mem}

用户问题：{query}
角色：{tone}
"""
        result = generate_llm(retry_prompt)
    return result

def generate_embedding(text: str) -> list:
    try:
        r = requests.post(
            f"{AGNO_API_BASE}/embedding",
            json={"text": text},
            timeout=15,
        )
        r.raise_for_status()
        return r.json().get("embedding", [])
    except Exception as e:
        raise RuntimeError(f"Embedding 调用失败（AGNO）: {e}")

def generate_llm(prompt: str) -> str:
    try:
        r = requests.post(
            f"{AGNO_API_BASE}/generate",
            json={"prompt": prompt},
            timeout=15,
        )
        r.raise_for_status()
        body = r.json()
        return body.get("text") or body.get("answer", "")
    except Exception as e:
        raise RuntimeError(f"LLM 调用失败（AGNO）: {e}")