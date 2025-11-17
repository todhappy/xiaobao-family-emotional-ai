from flask import Blueprint, request, jsonify
from sqlalchemy import text
from backend.db.postgres import get_session
from backend.models import MemoryRecord, MemoryEmbedding

memory_bp = Blueprint("memory", __name__, url_prefix="/api/v1/memory")

@memory_bp.route("/add", methods=["POST"])
def add_memory():
    data = request.json
    session = next(get_session())
    memory = MemoryRecord(
        family_id=data["family_id"],
        member_id=data["member_id"],
        content=data["content"],
        tags=data.get("tags", [])
    )
    session.add(memory)
    session.commit()
    embedding_vector = data.get("embedding")
    if embedding_vector:
        mem_vec = MemoryEmbedding(memory_id=memory.id, embedding=embedding_vector)
        session.add(mem_vec)
        session.commit()
    return jsonify({"memory_id": memory.id})

@memory_bp.route("/search", methods=["POST"])
def search_memory():
    data = request.json
    query_vector = data["query_vector"]
    session = next(get_session())
    vec_literal = "ARRAY[" + ",".join(str(float(x)) for x in query_vector) + "]::vector"
    sql = f"""
    SELECT me.memory_id AS memory_id, mr.content AS content, (me.embedding <=> {vec_literal}) AS distance
    FROM memory_embeddings me
    JOIN memory_records mr ON me.memory_id = mr.id
    WHERE mr.family_id = :family_id
    ORDER BY distance ASC
    LIMIT 5
    """
    result = session.execute(text(sql), {"family_id": data["family_id"]})
    out = [{"memory_id": r.memory_id, "content": r.content, "score": 1 - r.distance} for r in result]
    return jsonify(out)