余哥，我帮你整理了 **孝宝系统第三步 AI 能力层集成骨架**，直接对接你现有的 Flask 微服务（memory/chat/mcp），覆盖 **Mem0 长期记忆、Agno LLM 编排、家庭情绪推理、亲密度模型、语气模仿**，可直接用于第三步开发。

---

# **1️⃣ 目录结构扩展**

```
backend/
├── ai/
│   ├── __init__.py
│   ├── memory_agent.py      # Mem0 长期记忆调用封装
│   ├── agno_client.py       # Agno LLM 调用封装
│   ├── emotion_model.py     # 家庭成员情绪推理
│   ├── intimacy_model.py    # 关系亲密度计算
│   └── voice_tone.py        # 语气模仿
```

---

# **2️⃣ ai/memory_agent.py（Mem0 长期记忆封装）**

```python
import requests

class Mem0Agent:
    def __init__(self, base_url='http://localhost:8889'):
        self.base = base_url

    def retrieve_context(self, family_id, query_vector):
        """
        向 Mem0 查询长期记忆
        """
        payload = {"family_id": family_id, "query_vector": query_vector}
        r = requests.post(f"{self.base}/memory/search", json=payload)
        if r.status_code == 200:
            return r.json()
        return []

    def store_memory(self, family_id, member_id, content, embedding):
        payload = {
            "family_id": family_id,
            "member_id": member_id,
            "content": content,
            "embedding": embedding
        }
        r = requests.post(f"{self.base}/memory/add", json=payload)
        return r.status_code == 200
```

---

# **3️⃣ ai/agno_client.py（Agno LLM 封装）**

```python
import requests

class AgnoClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base = base_url

    def generate_response(self, prompt, context=[]):
        """
        调用 Agno LLM 生成回答
        """
        payload = {"prompt": prompt, "context": context}
        r = requests.post(f"{self.base}/llm/generate", json=payload)
        if r.status_code == 200:
            return r.json().get("answer", "")
        return "抱歉，无法生成回答"
```

---

# **4️⃣ ai/emotion_model.py（家庭成员情绪推理）**

```python
def infer_emotion(memory_list):
    """
    根据记忆内容推理家庭成员当前情绪
    示例：根据关键词计算正/负/中性情绪
    """
    emotions = []
    for m in memory_list:
        text = m.get("content","")
        if any(k in text for k in ["开心","快乐"]):
            emotions.append("positive")
        elif any(k in text for k in ["伤心","难过","生气"]):
            emotions.append("negative")
        else:
            emotions.append("neutral")
    # 返回统计结果
    from collections import Counter
    return dict(Counter(emotions))
```

---

# **5️⃣ ai/intimacy_model.py（关系亲密度模型）**

```python
def compute_intimacy(memory_list, interaction_count=0):
    """
    简单示例：亲密度分数 0~1
    - 根据记忆数量和互动次数计算
    """
    base_score = len(memory_list) * 0.1
    interaction_score = min(interaction_count * 0.05, 0.5)
    score = min(base_score + interaction_score, 1.0)
    return round(score, 2)
```

---

# **6️⃣ ai/voice_tone.py（语气模仿）**

```python
def apply_tone(text, member_role="父亲"):
    """
    根据家庭成员角色生成语气提示
    - 可用于 TTS 模型生成不同语气
    """
    tone_map = {
        "父亲": "沉稳、温和",
        "母亲": "温柔、关怀",
        "孩子": "活泼、俏皮"
    }
    tone = tone_map.get(member_role, "自然")
    return f"[{tone}] {text}"
```

---

# **7️⃣ 整合示例（在 chat_service.py 中调用）**

```python
from ai.memory_agent import Mem0Agent
from ai.agno_client import AgnoClient
from ai.emotion_model import infer_emotion
from ai.intimacy_model import compute_intimacy
from ai.voice_tone import apply_tone

mem_agent = Mem0Agent()
agno = AgnoClient()

def generate_family_reply(user_id, family_id, member_role, query):
    # 1. 生成 query 向量（可用 embedding API）
    query_vector = [0.1]*1536

    # 2. 查询长期记忆
    memories = mem_agent.retrieve_context(family_id, query_vector)

    # 3. 推理情绪
    emotions = infer_emotion(memories)

    # 4. 计算亲密度
    intimacy = compute_intimacy(memories, interaction_count=len(memories))

    # 5. 调用 LLM 生成回答
    context_texts = [m["content"] for m in memories]
    answer = agno.generate_response(query, context_texts)

    # 6. 语气模仿
    answer_with_tone = apply_tone(answer, member_role)

    return {
        "answer": answer_with_tone,
        "memories": memories,
        "emotions": emotions,
        "intimacy": intimacy
    }
```

---

# ✅ **说明**

1. Mem0Agent：处理长期记忆查询和存储
2. AgnoClient：调用 LLM 生成回答
3. EmotionModel：推理家庭成员情绪
4. IntimacyModel：计算亲密度分数
5. VoiceTone：为不同角色生成语气提示
6. ChatService 可直接调用 `generate_family_reply()` 替换原来的 RAG 逻辑
7. 可配合 MCP JSON-RPC 接口使用，实现设备端 AI 对话

---

我们把第三步后的三件事整合成一个完整的开发推进计划。我帮你生成：

1. **AI 能力整合到 chat_service.py + MCP API**
2. **前端 / 全息仓调用示例**（Web + WebSocket + 语音/图谱渲染）
3. **端到端测试脚本**（Mem0 + Agno + Flask + MCP 流程验证）

我会分模块给你生成代码骨架和示例。

---

# **1️⃣ AI 能力整合到 chat_service.py + MCP API**

更新 `chat_service.py`，使用你第三步的 `generate_family_reply` 逻辑：

```python
from flask import Blueprint, request, jsonify
from ai.integrated_ai import generate_family_reply  # 第三步 AI 整合

chat_bp = Blueprint("chat", __name__, url_prefix="/api/v1/chat")

@chat_bp.route("/send", methods=["POST"])
def send_chat():
    data = request.json
    user_id = data["user_id"]
    family_id = data["family_id"]
    member_role = data.get("member_role", "父亲")
    content = data["content"]

    reply = generate_family_reply(user_id, family_id, member_role, content)
    return jsonify(reply)
```

更新 `mcp_service.py` 对应方法调用：

```python
@mcp_bp.route("/", methods=["POST"])
def mcp_rpc():
    data = request.json
    method = data.get("method")
    params = data.get("params", {})

    if method == "chat.reply":
        family_id = params.get("family_id")
        user_id = params.get("user_id", 1)
        member_role = params.get("member_role", "父亲")
        content = params.get("content", "")
        reply = generate_family_reply(user_id, family_id, member_role, content)
        return jsonify({"id": params.get("id", 1), "result": reply})
```

✅ 完成后，MCP 与 chat API 将直接调用 **Mem0 + Agno + 情绪/亲密度/语气模仿**。

---

# **2️⃣ 前端 / 全息仓调用示例**

假设你使用 Next.js + React + WebSocket + Three.js 进行全息展示：

### **前端调用 Flask Chat API**

```javascript
// pages/api/chat.js
export async function sendChat(userId, familyId, content, memberRole) {
  const res = await fetch('http://localhost:5001/api/v1/chat/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, family_id: familyId, content, member_role: memberRole }),
  });
  return res.json();
}
```

### **WebSocket 实时同步（全息仓）**

```javascript
// frontend/utils/socket.js
import { io } from "socket.io-client";
const socket = io("http://localhost:5001");

export function sendMessage(msg) {
  socket.emit("chat_message", msg);
}

export function subscribe(callback) {
  socket.on("chat_reply", callback);
}
```

### **Three.js 全息家庭图谱渲染示例**

```javascript
import * as THREE from 'three';

function renderFamilyGraph(nodes, edges) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  // 节点
  nodes.forEach(n => {
    const geometry = new THREE.SphereGeometry(0.2, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(n.x, n.y, n.z);
    scene.add(sphere);
  });

  // 边
  edges.forEach(e => {
    const material = new THREE.LineBasicMaterial({ color: 0xffffff });
    const points = [new THREE.Vector3(e.from.x, e.from.y, e.from.z), new THREE.Vector3(e.to.x, e.to.y, e.to.z)];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, material);
    scene.add(line);
  });

  camera.position.z = 5;
  const animate = function () {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };
  animate();
}
```

> 结合 MCP / Chat API 可实现：
>
> * 用户发消息 → Chat API 返回 → WebSocket 推送 → Three.js 全息渲染
> * 语气模仿可在 TTS 播放时加语音参数

---

# **3️⃣ 端到端测试脚本**

```python
import requests
import numpy as np

BASE = 'http://127.0.0.1:5001'

# 1. 新增家庭成员
r = requests.post(f'{BASE}/api/v1/family/member/add', json={'family_id':1,'name':'测试成员','role':'子女'})
mid = r.json().get('member_id')

# 2. 添加记忆
embedding = [0.1]*1536
r = requests.post(f'{BASE}/api/v1/memory/add', json={'family_id':1,'member_id':mid,'content':'示例记忆-端到端','embedding':embedding})

# 3. 向量检索
r = requests.post(f'{BASE}/api/v1/memory/search', json={'family_id':1,'query_vector':embedding})
print("Memory Search:", r.json())

# 4. Chat AI 调用
r = requests.post(f'{BASE}/api/v1/chat/send', json={'user_id':1,'family_id':1,'content':'爸爸小时候的爱好','member_role':'父亲'})
print("Chat Reply:", r.json())

# 5. MCP RPC 调用
def rpc(method, params):
    return requests.post(f'{BASE}/family-mcp/', json={'method':method, 'params':params})

print("MCP chat.reply:", rpc('chat.reply', {'family_id':1,'content':'妈妈小时候的爱好','member_role':'母亲'}).json())
```

> 脚本验证完整流程：
>
> * Mem0 存储与检索
> * Agno LLM 回答生成
> * 情绪 / 亲密度 / 语气应用
> * MCP JSON-RPC 调用
> * 可结合 WebSocket / 全息图前端展示

---

请帮我验证孝宝系统第三步 AI 能力层集成及端到端功能是否正常，包括 Flask 微服务、Mem0 长期记忆、Agno LLM、情绪推理、亲密度模型、语气模仿、MCP JSON-RPC 接口，以及 WebSocket/全息仓调用。具体检查如下：

1️⃣ 基础服务
- Flask 服务端口 5001 是否可访问
- 蓝图注册：family, graph, memory, chat, mcp

2️⃣ Family API
- POST /api/v1/family/member/add: 新增成员，返回 member_id
- GET /api/v1/family/member/{id}: 返回成员信息

3️⃣ Graph API
- GET /api/v1/graph/family/{family_id}: 返回家庭图谱 JSON，节点和关系正确

4️⃣ Memory API
- POST /api/v1/memory/add: 添加记忆记录，支持 embedding 长度 1536
- POST /api/v1/memory/search: 向量检索返回 top 5 相关记忆，cosine similarity

5️⃣ Chat API
- POST /api/v1/chat/send: 输入 user_id, family_id, content, member_role，返回：
  - answer（包含 RAG 回答）
  - memories（相关记忆）
  - emotions（情绪推理结果）
  - intimacy（亲密度分数）
  - answer 带语气模仿标签

6️⃣ MCP JSON-RPC API
- POST /family-mcp/ 方法：
  - family.get_members
  - family.get_graph
  - memory.add
  - memory.search
  - chat.reply
- 返回 200，内容正确，chat.reply 包含 answer + memories + emotions + intimacy

7️⃣ WebSocket / 全息仓
- 连接 WebSocket（假设 ws://localhost:5001）
- 发送 chat_message，确认可接收 chat_reply 事件
- Three.js / 全息图数据能接收节点/边信息

8️⃣ 端到端流程
- 新增家庭成员
- 添加记忆记录
- 向量检索
- Chat 调用（包含 RAG + 情绪 + 亲密度 + 语气模仿）
- MCP chat.reply 调用
- WebSocket 推送消息接收

请输出每项检查点：
- 检查点
- 通过/失败状态
- 返回示例或响应长度
- 说明或错误信息
- 修复建议（如失败）
