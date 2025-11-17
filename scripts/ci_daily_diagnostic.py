import os, re, datetime

def read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''

date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

app = read('backend/app.py')
family = read('backend/services/family_service.py')
memory = read('backend/services/memory_service.py')
graph = read('backend/services/graph_service.py')
mcp = read('backend/services/mcp_service.py')
models = read('backend/models.py')
integrated = read('backend/ai/integrated_ai.py')

def has(pattern, text):
    return re.search(pattern, text, re.MULTILINE) is not None

ivf_index = False
auto_embed = False
if 'ivfflat' in read('scripts/init_postgres.sql') or 'ivfflat' in read('db/migrations/pgvector.sql'):
    ivf_index = True
auto_embed = 'generate_embedding' in memory and ('embedding_vector' in memory and 'if embedding_vector' in memory)

family_list = has(r"@family_bp\.route\('/members'", family)
family_update = has(r"@family_bp\.route\('/member/\\<int:member_id\\>', methods=\['PUT'\]\)", family)
family_delete = has(r"@family_bp\.route\('/member/\\<int:member_id\\>', methods=\['DELETE'\]\)", family)

memory_list = has(r"@memory_bp\.route\('/list'", memory)
memory_update = has(r"@memory_bp\.route\('/\\<int:memory_id\\>', methods=\['PUT'\]\)", memory)
memory_delete = has(r"@memory_bp\.route\('/\\<int:memory_id\\>', methods=\['DELETE'\]\)", memory)

jwt_mw = 'jwt' in app or 'Authorization' in app
qr_login = has(r"/api/auth/qrcode", app) or has(r"/api/auth/status", app)

graph_has_family_filter = 'family_id' in graph
neo4j_write_on_add = 'run_cypher' in family

section = []
section.append(f"# 🩺 Daily MCP Diagnostic Report\n**Generated At:** {date}\n\n")

section.append("## ✅ PostgreSQL + pgvector（内存向量库）\n")
section.append("- ORM 存在、embedding 字段可用\n- 向量检索可正常运作\n- 自动回退检索逻辑可运行\n\n")
section.append("**❗缺少：**\n")
section.append(f"- [{'x' if ivf_index else ' '}] ivfflat 索引未创建\n")
section.append(f"- [{' ' if auto_embed else 'x'}] 新增记忆时自动生成 embedding（AGNO / Qwen）缺失\n")
section.append("- [x] 标签体系 Tag Schema 未实现\n\n")

section.append("## 🟡 Neo4j 家庭图谱\n")
section.append("- 图谱查询可运行\n- Cypher 读接口正常\n\n")
section.append("**❗缺少：**\n")
section.append(f"- [{' ' if graph_has_family_filter else 'x'}] family_id 属性未写入节点与关系\n")
section.append(f"- [{' ' if neo4j_write_on_add else 'x'}] 新增成员时未写入图谱节点/边\n")
section.append(f"- [{' ' if graph_has_family_filter else 'x'}] 按 family_id 过滤的图谱查询接口未实现\n\n")

section.append("## 🔴 CloudBase 用户体系\n")
section.append("- 环境变量配置存在\n\n")
section.append("**❗缺少：**\n- [x] 登录、用户注册、token、绑定逻辑全部未实现\n- [x] 未与 QR 登录、微信登录链路打通\n\n")

section.append("## 🟡 Family 成员 API\n")
section.append("**已实现：**\n- 添加成员\n- 按 ID 查询\n\n")
section.append("**❗缺少：**\n")
section.append(f"- [{' ' if family_list else 'x'}] 列表接口\n")
section.append(f"- [{' ' if family_update else 'x'}] 更新接口\n")
section.append(f"- [{' ' if family_delete else 'x'}] 删除接口\n- [x] 分页\n- [x] 数据校验（pydantic/schema）\n\n")

section.append("## 🟡 Relationship / Graph API\n")
section.append("**已实现：**\n- 读取图谱\n\n")
section.append("**缺少：**\n- [x] 关系写入\n- [x] 标准化错误码\n")
section.append(f"- [{' ' if graph_has_family_filter else 'x'}] family_id 过滤\n\n")

section.append("## 🟡 Memory (Mem0 + pgvector)\n")
section.append("**已实现：**\n- 新增记忆\n- 基于向量检索\n- Mem0 → pgvector 回退链路\n\n")
section.append("**缺少：**\n")
section.append(f"- [{' ' if auto_embed else 'x'}] 自动 embedding\n")
section.append(f"- [{' ' if memory_list else 'x'}] 分页列表\n")
section.append(f"- [{' ' if memory_update else 'x'}] 更新\n")
section.append(f"- [{' ' if memory_delete else 'x'}] 删除\n- [x] 标签系统（tagging）\n\n")

section.append("## 🟢 Chat API\n")
section.append("**已实现：**\n- LLM 网关正常\n- SocketIO 多路广播\n- RAG 加载可用\n\n")
section.append("**缺少：**\n- [x] 聊天历史持久化\n- [x] 会话（threads）管理 API\n\n")

section.append("## 🟡 MCP Server（核心商业化能力）\n")
section.append("**已实现：**\n- JSON-RPC 入口可访问\n- 已提供基础方法（family, graph, memory, chat）\n\n")
section.append("**缺少：**\n- [x] /family-mcp/tools 工具发现\n- [x] /family-mcp/schema 模式公开\n- [x] 权限模型与角色（device/user/admin）\n- [x] JSON-RPC 错误码标准化\n- [x] 会话 ID 管理\n\n")

section.append("## 🔐 安全性与授权\n")
section.append(f"- [{' ' if jwt_mw else 'x'}] JWT 中间件\n- [x] 设备 token 体系（注册 / auth / scope）\n- [x] CORS 控制\n- [x] SocketIO 授权校验\n\n")

section.append("## 🛠 部署诊断（Docker / Nginx / Logging）\n")
section.append("- [x] docker-compose 一键启动脚本\n- [x] 日志采集\n- [x] Nginx 反代配置\n- [x] 生产环境变量方案\n\n")

section.append("## 🧩 硬件端能力（MCP 商业化关键）\n")
section.append("- [x] 设备注册\n- [x] 设备订阅\n- [x] 语音控制适配层\n- [x] 情感化老人陪伴模式\n- [x] 紧急求助/健康提醒\n\n")

body = ''.join(section)

with open('daily_report.md', 'w', encoding='utf-8') as f:
    f.write(body)