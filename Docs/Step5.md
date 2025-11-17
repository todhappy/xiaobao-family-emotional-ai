 **完整更新代码**，整合了：

1. **Graph API edges 修复**（Neo4j 查询正确构建 edges）
2. **SocketIO 家庭图谱广播更新**
3. **Agno LLM / Embedding 集成**（可使用本地部署或 API Key 调用 Qwen2.5 / DeepSeek / OpAI）

可以直接替换你现有的 `integrated_ai.py`、`graph_service.py` 和 `app.py`。

---

# **1️⃣ backend/ai/integrated_ai.py**

```python
import requests
import os

# 配置 LLM 与 Embedding
AGNO_API_BASE = os.getenv("AGNO_API_BASE", "http://localhost:5000")
AGNO_API_KEY = os.getenv("AGNO_API_KEY", "sk-e12c8b93c72442a59fbb6e6e660162af")  # 可替换 Qwen2.5 / DeepSeek / OpAI

# 生成向量
def query_to_vector(text):
    payload = {"text": text}
    headers = {"Authorization": f"Bearer {AGNO_API_KEY}"}
    try:
        r = requests.post(f"{AGNO_API_BASE}/embedding", json=payload, headers=headers)
        if r.status_code == 200:
            return r.json().get("embedding", [0.0]*1536)
    except:
        pass
    return [0.0]*1536

# 生成回答（RAG + LLM）
def generate_response(query, memories=[]):
    context_text = " ".join([m.get("content","") for m in memories])
    payload = {"prompt": query, "context": context_text}
    headers = {"Authorization": f"Bearer {AGNO_API_KEY}"}
    try:
        r = requests.post(f"{AGNO_API_BASE}/generate", json=payload, headers=headers)
        if r.status_code == 200:
            return r.json().get("answer", "抱歉，无法生成回答")
    except:
        pass
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

# **2️⃣ backend/services/graph_service.py（edges 修复）**

```python
from neo4j import GraphDatabase
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "Family@123")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def get_family_graph(family_id):
    nodes = []
    edges = []
    with driver.session() as session:
        # 查询所有成员节点
        node_query = "MATCH (m:FamilyMember {family_id:$fid}) RETURN m.id AS id, m.name AS name, m.role AS role"
        for record in session.run(node_query, fid=family_id):
            nodes.append({"id":record["id"],"name":record["name"],"role":record["role"]})
        
        # 查询关系 edges
        edge_query = """
        MATCH (a:FamilyMember {family_id:$fid})-[r]->(b:FamilyMember {family_id:$fid})
        RETURN a.id AS from, b.id AS to, type(r) AS type
        """
        for record in session.run(edge_query, fid=family_id):
            edges.append({"from":record["from"],"to":record["to"],"type":record["type"]})
    return {"nodes":nodes, "edges":edges}
```

---

# **3️⃣ backend/app.py（SocketIO 广播更新）**

```python
from flask import Flask
from flask_socketio import SocketIO
from services.chat_service import chat_bp
from services.mcp_service import mcp_bp
from ai.integrated_ai import generate_family_reply
from services.graph_service import get_family_graph

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(chat_bp)
app.register_blueprint(mcp_bp)

@socketio.on("chat_message")
def handle_chat_message(data):
    user_id = data.get("user_id",1)
    family_id = data.get("family_id",1)
    content = data.get("content","")
    member_role = data.get("member_role","父亲")

    # 查询相关记忆
    memories = []  # 可调用 Mem0Agent 或 Memory API

    # 生成回答
    reply = generate_family_reply(user_id, family_id, member_role, content, memories)
    socketio.emit("chat_reply", reply)

    # 广播家庭图谱节点 + edges
    graph_data = get_family_graph(family_id)
    socketio.emit("family_graph", graph_data)

if __name__=="__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
```

---

# **使用说明**

1. **本地部署 Agno**

```bash
git clone https://github.com/agno-agi/agno.git
cd agno
# 按 README 部署 API 服务
```

2. **设置环境变量**

```bash
export AGNO_API_BASE=http://localhost:5000
export AGNO_API_KEY=sk-e12c8b93c72442a59fbb6e6e660162af  # 或使用 deepseek / opai
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASS=Family@123
```

3. **启动 Flask + SocketIO**

```bash
python backend/app.py
```

4. **前端 / 全息仓**

* WebSocket 连接 `ws://localhost:5001`
* 发送 `chat_message` → 接收 `chat_reply` + `family_graph`
* Three.js 渲染节点/边，并显示语气/情绪/亲密度

