import eventlet
eventlet.monkey_patch()
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from backend.services.family_service import family_bp
from backend.services.graph_service import graph_bp, _nodes_edges
from backend.services.memory_service import memory_bp
from backend.services.chat_service import handle_chat
from backend.services.mcp_service import mcp_bp
from backend.config import FLASK_PORT

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# 健康检查
@app.route("/ping", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "xiaobao-backend"})

app.register_blueprint(family_bp)
app.register_blueprint(graph_bp)
app.register_blueprint(memory_bp)
# Chat route moved here using handle_chat
@app.route("/api/v1/chat/send", methods=["POST"])
def chat_send():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    family_id = data.get("family_id")
    member_role = data.get("member_role", "父亲")
    content = data.get("content", "")
    result = handle_chat(
        user_id=user_id,
        family_id=family_id,
        member_role=member_role,
        content=content
    )
    return jsonify(result)
app.register_blueprint(mcp_bp)

@socketio.on('chat_message')
def handle_chat_message(data):
    user_id = data.get("user_id", 1)
    family_id = data.get("family_id", 1)
    content = data.get("content", "")
    member_role = data.get("member_role", "父亲")
    try:
        reply = handle_chat(user_id=user_id, family_id=family_id, member_role=member_role, content=content)
        emit('chat_reply', reply, broadcast=True)
        graph_data = _nodes_edges(family_id)
        emit('family_graph', graph_data, broadcast=True)
        LOG_ITEMS.append({"module": "chat", "message": f"chat_message handled for family {family_id}", "time": time.time()})
        emit('notice_message', {"type": "chat", "message": "新的聊天回复已生成"}, broadcast=True)
    except Exception as e:
        emit('chat_reply', {"error": str(e)}, broadcast=True)

# 简易日志与指标
LOG_ITEMS = []
import time

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({"items": LOG_ITEMS[-100:]})

@app.route('/metrics/traffic', methods=['GET'])
def metrics_traffic():
    return jsonify([5,8,12,9,7,10,13,12,11,9])

@app.route('/metrics/latency', methods=['GET'])
def metrics_latency():
    return jsonify([120,110,130,100,95,140])

@app.route('/metrics/errors', methods=['GET'])
def metrics_errors():
    return jsonify([0,1,0,2,0,1])

@app.route('/metrics/resources', methods=['GET'])
def metrics_resources():
    return jsonify([50,48,55,60,57,53])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=FLASK_PORT)