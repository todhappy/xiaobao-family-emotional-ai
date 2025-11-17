 **Agno** 部署到本地，并和你的孝宝系统完美集成，让 Chat API / MCP / RAG 能调用真实 LLM 和 Embedding。以下是完整操作方案和步骤：

---

## 1️⃣ 准备环境

1. **系统要求**

   * Python 3.10+
   * Docker & Docker Compose（可选，用于容器化部署）
   * Git
   * 网络畅通，能访问外部模型 API（如 Qwen2.5、DeepSeek、OpAI）

2. **安装依赖**

```bash
# 克隆孝宝项目并进入 backend
cd /path/to/xiaobaomcp/backend
pip install -r requirements.txt

# 安装 socketio client/server
pip install "python-socketio[client]" "flask-socketio"

# 安装 Agno 依赖
pip install requests transformers
```

---

## 2️⃣ 获取 Agno 源码

```bash
git clone https://github.com/agno-agi/agno.git
cd agno
```

* 可以选择 **本地运行** 或 **Docker 容器**：

```bash
# Docker 方式（推荐隔离）
docker build -t agno:latest .
docker run -d -p 5000:5000 --name agno agno:latest
```

* 如果本地直接运行：

```bash
# 假设 agno 提供 flask/gunicorn 服务
python agno/app.py
# 默认端口 5000
```

---

## 3️⃣ 配置 Agno 服务

1. **启动 Agno API**

   * 默认端口：`http://localhost:5000`
   * 提供 Embedding / LLM 接口

2. **设置孝宝系统调用环境变量**

```bash
export AGNO_API_BASE="http://localhost:5000"
export AGNO_API_KEY="你的API密钥"  # 如果你用 Qwen2.5/DeepSeek/OpAI 的 API
```

* 或在 `.env` 文件中：

```ini
AGNO_API_BASE=http://localhost:5000
AGNO_API_KEY=sk-e12c8b93c72442a59fbb6e6e660162af
```

---

## 4️⃣ 更新孝宝系统配置

1. **修改 `backend/ai/integrated_ai.py`**

   * 使用环境变量调用 Agno Embedding / LLM
   * 示例：

```python
import os
import requests

AGNO_BASE = os.getenv("AGNO_API_BASE")
AGNO_KEY = os.getenv("AGNO_API_KEY")

def generate_embedding(text):
    resp = requests.post(f"{AGNO_BASE}/embedding", json={"text": text}, headers={"Authorization": f"Bearer {AGNO_KEY}"})
    return resp.json()["embedding"]

def generate_llm(prompt, context=None):
    payload = {"prompt": prompt, "context": context or []}
    resp = requests.post(f"{AGNO_BASE}/llm", json=payload, headers={"Authorization": f"Bearer {AGNO_KEY}"})
    return resp.json()["answer"]
```

2. **确保 Chat API / MCP 调用** `integrated_ai.generate_llm()` 和 `generate_embedding()` 替换占位函数。

---

## 5️⃣ 测试 LLM + Embedding 调用

```python
from backend.ai import integrated_ai as ai

text = "爸爸小时候的爱好"
embedding = ai.generate_embedding(text)
answer = ai.generate_llm(f"请基于家庭记忆回答: {text}")
print("Embedding:", embedding[:10], "...")  # 前10维
print("Answer:", answer)
```

* 确认返回正确向量和文本回答
* 如果返回异常，请检查：

  * AGNO 服务是否启动
  * API Key 是否有效
  * 防火墙或端口是否被占用

---

## 6️⃣ 集成到端到端流程

1. **Chat API**

   * `/api/v1/chat/send` → 调用 `generate_embedding()` + RAG + `generate_llm()`
2. **MCP JSON-RPC**

   * `chat.reply` → 同上
3. **Memory API**

   * 插入 embedding 向量，用于 RAG 检索
4. **SocketIO**

   * WebSocket 推送 `chat_reply`，返回真实回答
5. **Graph API**

   * 不依赖 LLM，但可将 RAG 结果关联节点，更新图谱显示

---

## 7️⃣ 验证端到端

* 使用之前生成的 **端到端 Python 验证脚本 V2**
* 检查：

  * Mem0 向量检索
  * Graph API nodes/edges
  * Chat API 返回真实 LLM 回答
  * MCP JSON-RPC 输出
  * WebSocket chat_reply & family_graph

---

💡 **提示**

* Qwen2.5 / DeepSeek / OpAI 可以替换 AGNO_KEY
* 如果本地部署 Agno，建议使用 Docker 方式，避免依赖冲突
* Embedding 向量维度需与 PostgreSQL pgvector 定义一致（1536）
* RAG 回答可结合 Memory API 检索结果，实现上下文增强

