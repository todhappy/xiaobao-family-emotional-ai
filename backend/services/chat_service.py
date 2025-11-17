from backend.ai.integrated_ai import generate_family_reply

def handle_chat(user_id, family_id, member_role, content):
    """
    Chat API 统一入口
    使用 integrated_ai 的 RAG + AGNO LLM + 情绪 + 亲密度 + 语气
    """
    return generate_family_reply(
        user_id=user_id,
        family_id=family_id,
        member_role=member_role,
        query=content
    )