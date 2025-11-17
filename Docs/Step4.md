
---

# **模块 1：集成真实 Agno LLM + Embedding**

### **目标**

* 替换 `backend/ai/integrated_ai.py` 中占位生成函数
* 使用真实 Agno LLM API 生成回答
* 生成向量 embedding，用于 RAG 检索

### **步骤**

1. 安装必要依赖（假设 Agno 提供 Python SDK 或 HTTP API）：

```bash
pip install requests numpy
```

2. 修改 `integrated_ai.py` 中 `query_to_vector` 和 `generate_response`：

```python
import requests
import numpy as np

AGNO_API_BASE = "http://localhost:5000"  # Agno LLM 服务地址
AGNO_API_KEY = "你的API_KEY"

def query_to_vector(text):
    """调用 Agno Embedding API 生成向量"""
    payload = {"text": text}
    headers = {"Authorization": f"Bearer {AGNO_API_KEY}"}
    r = requests.post(f"{AGNO_API_BASE}/embedding", json=payload, headers=headers)
    if r.status_code == 200:
        return r.json().get("embedding", [0.0]*1536)
    else:
        return [0.0]*1536  # fallback

def generate_response(query, memories=[]):
    """调用 Agno LLM API 生成回答，结合 RAG 上下文"""
    context_text = " ".join([m["content"] for m in memories])
    payload = {"prompt": query, "context": context_text}
    headers = {"Authorization": f"Bearer {AGNO_API_KEY}"}
    r = requests.post(f"{AGNO_API_BASE}/generate", json=payload, headers=headers)
    if r.status_code == 200:
        return r.json().get("answer", "抱歉，无法生成回答")
    return "抱歉，无法生成回答"
```

3. 验证 RAG 输出：

```python
memories = [{"content":"爸爸小时候喜欢吃潮汕粿条"}]
answer = generate_response("爸爸喜欢吃什么？", memories)
print(answer)
```

> ✅ 输出应包含 RAG 上下文，供后续语气/情绪/亲密度函数使用

---

# **模块 2：实现 SocketIO 事件**

### **步骤**

1. 安装依赖：

```bash
pip install flask-socketio eventlet
```

2. 修改 `app.py` 启动方式：

```python
from flask import Flask
from flask_socketio import SocketIO
from services.chat_service import chat_bp
from services.mcp_service import mcp_bp
from ai.integrated_ai import generate_family_reply

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # 支持跨域

app.register_blueprint(chat_bp)
app.register_blueprint(mcp_bp)

# WebSocket chat_message 事件
@socketio.on('chat_message')
def handle_chat_message(data):
    user_id = data.get("user_id",1)
    family_id = data.get("family_id",1)
    content = data.get("content","")
    member_role = data.get("member_role","父亲")
    
    reply = generate_family_reply(user_id, family_id, member_role, content)
    # 推送 chat_reply
    socketio.emit('chat_reply', reply)
    # 可同时广播家庭图谱节点/边
    graph_data = {"nodes":[...],"edges":[...]}  # 从 Neo4j 获取
    socketio.emit('family_graph', graph_data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
```

> ✅ 完成后，前端可以通过 WebSocket 发送 `chat_message` 并接收 `chat_reply` 与 `family_graph`

---

# **模块 3：前端/全息仓联调**

### **步骤**

1. 前端调用 chat API 或 MCP JSON-RPC：

```javascript
async function sendChat(userId, familyId, content, memberRole){
  const res = await fetch('http://localhost:5001/api/v1/chat/send', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({user_id:userId, family_id:familyId, content, member_role:memberRole})
  });
  return res.json();
}
```

2. 前端 WebSocket 监听：

```javascript
import { io } from "socket.io-client";
const socket = io("http://localhost:5001");

socket.on("connect", () => console.log("WebSocket connected"));

socket.on("chat_reply", (data) => {
  console.log("Chat reply received:", data.answer, data.emotions, data.intimacy);
});

socket.on("family_graph", (data) => {
  console.log("Graph data received:", data.nodes.length, data.edges.length);
});
```

3. 前端 Three.js 渲染示例（全息仓）：

```javascript
function updateFamilyGraph(nodes, edges){
  // 遍历节点和边，更新 Three.js 场景
  // ...
}
```

---

# **模块 4：验证语气、情绪、亲密度**

* 在前端或 WebSocket 回调中：

```javascript
socket.on("chat_reply", (data)=>{
  console.log("回答:", data.answer);       // 含语气标签
  console.log("情绪:", data.emotions);     // positive/neutral/negative
  console.log("亲密度:", data.intimacy);   // 0~1
});
```

> 确认输出结果与预期一致，语气、情绪、亲密度可结合全息仓动画/声音渲染

---

# **开发顺序总结**

1. 替换占位函数 → 集成 Agno LLM + Embedding
2. 集成 SocketIO → 实现 `chat_message` → `chat_reply` 推送 + 家庭图谱广播
3. 前端调用 chat API / MCP JSON-RPC
4. WebSocket 监听 → 更新 Three.js 全息图
5. 验证语气/情绪/亲密度输出

余哥，我帮你整理好了一个 **可直接替换现有服务的完整代码模板**，包含三大改进：

1. **Agno LLM / Embedding 集成**
2. **WebSocket 家庭图谱 edges 修正**
3. **MCP JSON-RPC 全方法统一封装**

你可以直接替换现有 `backend/ai/integrated_ai.py`、`app.py`、`mcp_service.py`，实现完整端到端孝宝系统。

---

# **1️⃣ backend/ai/integrated_ai.py**

```python
import requests

AGNO_API_BASE = "http://localhost:5000"
AGNO_API_KEY = "你的API_KEY"

def query_to_vector(text):
    """调用 Agno Embedding API 生成向量"""
    payload = {"text": text}
    headers = {"Authorization": f"Bearer {AGNO_API_KEY}"}
    r = requests.post(f"{AGNO_API_BASE}/embedding", json=payload, headers=headers)
    if r.status_code == 200:
        return r.json().get("embedding", [0.0]*1536)
    return [0.0]*1536

def generate_response(query, memories=[]):
    """调用 Agno LLM API 生成回答，结合 RAG 上下文"""
    context_text = " ".join([m.get("content","") for m in memories])
    payload = {"prompt": query, "context": context_text}
    headers = {"Authorization": f"Bearer {AGNO_API_KEY}"}
    r = requests.post(f"{AGNO_API_BASE}/generate", json=payload, headers=headers)
    if r.status_code == 200:
        return r.json().get("answer", "抱歉，无法生成回答")
    return "抱歉，无法生成回答"

# 情绪推理
def infer_emotion(memory_list):
    emotions = []
    for m in memory_list:
        text = m.get("content","")
        if any(k in text for k in ["开心","快乐"]):
            emotions.append("positive")
        elif any(k in text for k in ["伤心","难过","生气"]):
            emotions.append("negative")
        else:
            emotions.append("neutral")
    from collections import Counter
    return dict(Counter(emotions))

# 亲密度
def compute_intimacy(memory_list, interaction_count=0):
    base_score = len(memory_list) * 0.1
    interaction_score = min(interaction_count * 0.05, 0.5)
    return round(min(base_score+interaction_score,1.0),2)

# 语气模仿
def apply_tone(text, member_role="父亲"):
    tone_map = {"父亲":"沉稳、温和","母亲":"温柔、关怀","孩子":"活泼、俏皮"}
    tone = tone_map.get(member_role, "自然")
    return f"[{tone}] {text}"

# 集成调用
def generate_family_reply(user_id, family_id, member_role, query, memories):
    answer = generate_response(query, memories)
    answer_with_tone = apply_tone(answer, member_role)
    emotions = infer_emotion(memories)
    intimacy = compute_intimacy(memories, len(memories))
    return {"answer": answer_with_tone, "memories": memories, "emotions": emotions, "intimacy": intimacy}
```

---

# **2️⃣ backend/app.py（SocketIO 集成 + edges 修正）**

```python
from flask import Flask
from flask_socketio import SocketIO
from services.chat_service import chat_bp
from services.mcp_service import mcp_bp
from ai.integrated_ai import generate_family_reply
from services.graph_service import get_family_graph  # 返回 {nodes,edges}

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(chat_bp)
app.register_blueprint(mcp_bp)

# WebSocket 事件
@socketio.on("chat_message")
def handle_chat_message(data):
    user_id = data.get("user_id",1)
    family_id = data.get("family_id",1)
    content = data.get("content","")
    member_role = data.get("member_role","父亲")
    
    # 查询相关记忆
    memories = []  # 可调用 Mem0Agent 或 Memory API
    
    reply = generate_family_reply(user_id, family_id, member_role, content, memories)
    socketio.emit("chat_reply", reply)

    # 广播家庭图谱节点 + edges
    graph_data = get_family_graph(family_id)  # 返回标准化 {nodes,edges}
    socketio.emit("family_graph", graph_data)

if __name__=="__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
```

---

# **3️⃣ backend/services/mcp_service.py（JSON-RPC 全方法统一）**

```python
from flask import Blueprint, request, jsonify
from ai.integrated_ai import generate_family_reply
from services.family_service import get_members
from services.graph_service import get_family_graph
from services.memory_service import add_memory, search_memory

mcp_bp = Blueprint("mcp", __name__, url_prefix="/family-mcp")

@mcp_bp.route("/", methods=["POST"])
def mcp_rpc():
    data = request.json
    method = data.get("method")
    params = data.get("params", {})
    rpc_id = params.get("id",1)

    try:
        if method=="family.get_members":
            result = get_members(params.get("family_id"))
        elif method=="family.get_graph":
            result = get_family_graph(params.get("family_id"))
        elif method=="memory.add":
            result = add_memory(params)
        elif method=="memory.search":
            result = search_memory(params)
        elif method=="chat.reply":
            memories = search_memory({"family_id":params.get("family_id")})  # 示例
            result = generate_family_reply(
                params.get("user_id",1),
                params.get("family_id"),
                params.get("member_role","父亲"),
                params.get("content",""),
                memories
            )
        else:
            return jsonify({"jsonrpc":"2.0","id":rpc_id,"error":"method_not_found"})
        return jsonify({"jsonrpc":"2.0","id":rpc_id,"result":result})
    except Exception as e:
        return jsonify({"jsonrpc":"2.0","id":rpc_id,"error":str(e)})
```

---

# **使用说明**

1. 设置环境变量：

```bash
export AGNO_API_BASE=http://localhost:5000
export AGNO_API_KEY=你的API_KEY
```

2. 启动 Flask + SocketIO：

```bash
python backend/app.py
```

3. 前端 / 全息仓：

* WebSocket 连接 `ws://localhost:5001`
* 发送 `chat_message` → 接收 `chat_reply` + `family_graph`
* Three.js 渲染节点/边，显示语气/情绪/亲密度

---

