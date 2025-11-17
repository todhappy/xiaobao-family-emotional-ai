from flask import Blueprint, request, jsonify
from backend.services.family_service import get_member
from backend.services.graph_service import _nodes_edges
from backend.db.postgres import get_session
from backend.models import MemoryRecord, MemoryEmbedding
from sqlalchemy import text
from backend.ai.integrated_ai import generate_family_reply

mcp_bp = Blueprint("mcp", __name__, url_prefix="/family-mcp")

@mcp_bp.route("/", methods=["POST"])
def mcp_rpc():
    data = request.json
    method = data.get("method")
    params = data.get("params", {})
    rpc_id = params.get("id", 1)
    if method == "family.get_members":
        family_id = params.get("family_id")
        session = next(get_session())
        rows = session.execute(text("SELECT id, name, role FROM family_members WHERE family_id=:fid"), {"fid": family_id})
        members = [{"id": r.id, "name": r.name, "role": r.role} for r in rows]
        return jsonify({"jsonrpc": "2.0", "id": rpc_id, "result": members})
    elif method == "family.get_graph":
        family_id = params.get("family_id")
        graph = _nodes_edges(family_id)
        return jsonify({"jsonrpc": "2.0", "id": rpc_id, "result": graph})
    elif method == "memory.add":
        session = next(get_session())
        memory = MemoryRecord(
            family_id=params["family_id"],
            member_id=params["member_id"],
            content=params["content"],
            tags=params.get("tags", [])
        )
        session.add(memory)
        session.commit()
        embedding_vector = params.get("embedding")
        if embedding_vector:
            mem_vec = MemoryEmbedding(memory_id=memory.id, embedding=embedding_vector)
            session.add(mem_vec)
            session.commit()
        return jsonify({"jsonrpc": "2.0", "id": rpc_id, "result": {"memory_id": memory.id}})
    elif method == "memory.search":
        session = next(get_session())
        family_id = params["family_id"]
        query_vector = params["query_vector"]
        vec_literal = "ARRAY[" + ",".join(str(float(x)) for x in query_vector) + "]::vector"
        sql = f"""
        SELECT me.memory_id AS memory_id, mr.content AS content, (me.embedding <=> {vec_literal}) AS distance
        FROM memory_embeddings me
        JOIN memory_records mr ON me.memory_id = mr.id
        WHERE mr.family_id = :family_id
        ORDER BY distance ASC
        LIMIT 5
        """
        result = session.execute(text(sql), {"family_id": family_id})
        out = [{"memory_id": r.memory_id, "content": r.content, "score": 1 - r.distance} for r in result]
        return jsonify({"jsonrpc": "2.0", "id": rpc_id, "result": out})
    elif method == "chat.reply":
        content = params.get("content", "")
        family_id = params.get("family_id")
        member_role = params.get("member_role", "父亲")
        user_id = params.get("user_id")
        rpc_id = params.get("id", 1)
        result = generate_family_reply(user_id, family_id, member_role, content)
        return jsonify({"jsonrpc": "2.0", "id": rpc_id, "result": result})
    else:
        return jsonify({"jsonrpc": "2.0", "id": rpc_id, "error": "method_not_found"})