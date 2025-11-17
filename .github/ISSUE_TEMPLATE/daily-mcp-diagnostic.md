---
name: "🩺 Daily MCP Diagnostic Report"
about: "CI 自动执行《MCP 家庭情感中台诊断脚本》并输出最新的系统进度、缺陷与 TODO"
title: "Daily MCP Diagnostic — {{date}}"
labels: ["diagnostic", "auto-generated", "mcp"]
assignees: []
---

# 🩺 Daily MCP Diagnostic Report
**Generated At:** {{date}}

本报告由 CI 自动生成，用于检查 Xiaobao Family Emotional AI 平台的 MCP Server 真实开发状态、缺失模块以及与《家庭记忆库示例教程》对照的落地情况。

---

# 1. 🧱 数据层检查（PostgreSQL / pgvector / Neo4j / CloudBase）

## ✅ PostgreSQL + pgvector（内存向量库）
**当前状态：**
- ORM 存在、embedding 字段可用  
- 向量检索可正常运作  
- 自动回退检索逻辑可运行  

**❗缺少：**
- [ ] *ivfflat 索引未创建*  
- [ ] *新增记忆时自动生成 embedding（AGNO / Qwen）缺失*  
- [ ] *标签体系 Tag Schema 未实现*

---

## 🟡 Neo4j 家庭图谱
**当前状态：**
- 图谱查询可运行  
- Cypher 读接口正常  

**❗缺少：**
- [ ] *family_id 属性未写入节点与关系*  
- [ ] *新增成员时未写入图谱节点/边*  
- [ ] *按 family_id 过滤的图谱查询接口未实现*

---

## 🔴 CloudBase 用户体系
**当前状态：**
- 环境变量配置存在  

**❗缺少：**
- [ ] *登录、用户注册、token、绑定逻辑全部未实现* 
- [ ] *未与 QR 登录、微信登录链路打通*

---

# 2. 🛠 后端微服务层检查（Family / Graph / Memory / Chat / MCP）

## 🟡 Family 成员 API
**已实现：**
- 添加成员  
- 按 ID 查询  

**❗缺少：**
- [ ] 列表接口  
- [ ] 更新接口  
- [ ] 删除接口  
- [ ] 分页  
- [ ] 数据校验（pydantic/schema）  

---

## 🟡 Relationship / Graph API
**已实现：**
- 读取图谱  

**缺少：**
- [ ] 关系写入  
- [ ] 标准化错误码  
- [ ] family_id 过滤  

---

## 🟡 Memory (Mem0 + pgvector)
**已实现：**
- 新增记忆  
- 基于向量检索  
- Mem0 → pgvector 回退链路  

**缺少：**
- [ ] 自动 embedding  
- [ ] 分页列表  
- [ ] 更新  
- [ ] 删除  
- [ ] 标签系统（tagging）  

---

## 🟢 Chat API
**已实现：**
- LLM 网关正常  
- SocketIO 多路广播  
- RAG 加载可用  

**缺少：**
- [ ] 聊天历史持久化  
- [ ] 会话（threads）管理 API  

---

## 🟡 MCP Server（核心商业化能力）
**已实现：**
- JSON-RPC 入口可访问  
- 已提供基础方法（family, graph, memory, chat）  

**缺少：**
- [ ] `/family-mcp/tools` 工具发现  
- [ ] `/family-mcp/schema` 模式公开  
- [ ] 权限模型与角色（device/user/admin）  
- [ ] JSON-RPC 错误码标准化  
- [ ] 会话 ID 管理  

---

# 3. 🤖 AI 能力诊断（Mem0 / AGNO / Qwen / 情绪）

## 🟢 情绪模型 + 亲密度模型
**已实现：**
- 关键词情绪识别  
- 亲密度规则  
- persona 语气匹配  

**缺少：**
- [ ] 权重可配置化  
- [ ] 多维情绪（valence/arousal）  
- [ ] persona schema（age/style/background）  

---

## AGNO 工作流
**已实现：**
- `/embedding`  
- `/generate`  
- prompt 中注入 memory + 关键词  

**缺少：**
- [ ] 断路器  
- [ ] 全局重试  
- [ ] 模型健康检测  

---

# 4. 🌐 前端层检查（Web/SocketIO/管理后台）

## Web 图谱（Three.js）
- [x] 渲染正常  
- [ ] 未按 family_id 分类  
- [ ] 新节点与边未实时联动 Neo4j  

## Memory Timeline
- [x] 时间轴可见  
- [ ] 缺分页  
- [ ] 缺标签过滤  

## 管理后台
- [ ] admin 接口未落地  
- [ ] 数据均为 mock  

---

# 5. 🔐 安全性与授权

**缺失严重：**
- [ ] JWT 中间件  
- [ ] 设备 token 体系（注册 / auth / scope）  
- [ ] CORS 控制  
- [ ] SocketIO 授权校验  

---

# 6. 🛠 部署诊断（Docker / Nginx / Logging）

**缺少：**
- [ ] docker-compose 一键启动脚本  
- [ ] 日志采集  
- [ ] Nginx 反代配置  
- [ ] 生产环境变量方案  

---

# 7. 🧩 硬件端能力（MCP 商业化关键）

**全部未实现：**
- [ ] 设备注册  
- [ ] 设备订阅  
- [ ] 语音控制适配层  
- [ ] 情感化老人陪伴模式  
- [ ] 紧急求助/健康提醒  

---

# 8. 📌 CI 自动 TODO 列表

❗ 任何 **下面仍未勾选的项目** 都会继续在明日的检查报告中出现。 

> CI 将自动从此 Issue 的未完成清单中抽取 TODO，并反馈到  
> `/backend/services/**` 和 `/frontend-web/**` 对应模块的二级目录中。 

---

# 9. 🗺 未来 14 天开发建议（按优先级）

## 🔥 P0（必须本周完成）
- [ ] JWT + 权限  
- [ ] 自动 embedding  
- [ ] pgvector 索引  
- [ ] family_id → Neo4j 写入  
- [ ] MCP 工具发现 & schema  
- [ ] 聊天历史持久化  

## 🟡 P1（第二周进行）
- [ ] 完整 CRUD（family/memory）  
- [ ] 设备注册与 token  
- [ ] Persona schema  
- [ ] 图谱写入与实时可视化  

## 🟢 P2（可延后）
- [ ] 更复杂情绪模型  
- [ ] 管理后台与 Admin API  
- [ ] Prometheus + 结构化日志  
- [ ] 老年陪伴与语音硬件协议  

---

# ✔ 诊断结束  
如需人工补充或自动修复脚本，请在评论中输入：