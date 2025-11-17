第一步：数据库与基础模型搭建

目标：先构建数据基础层，保证后续 API、AI 模型、前端 UI 都有数据支撑。

1️⃣ PostgreSQL + pgvector

任务：

创建数据库 family_db

建立核心表：users、families、family_members、memory_records、memory_embeddings、chat_messages、devices、mcp_sessions

配置 pgvector 扩展

检查点：

每张表可插入测试数据

向量嵌入可正常插入和查询（测试 pgvector cosine similarity）

输出产物：

可查询、可写入的核心 PostgreSQL 数据库

测试向量数据

2️⃣ Neo4j 图数据库

任务：

创建图数据库 family_graph

建立节点类型 FamilyMember（id、name、role、avatar_url）

建立关系类型 SPOUSE_OF、PARENT_OF、SIBLING_OF

初始化测试家庭结构数据

检查点：

可以用 Cypher 查询生成家庭树

图谱数据与 PostgreSQL family_members 对应

输出产物：

可视化图谱（Neo4j 浏览器可看）

节点和关系映射表

3️⃣ CloudBase（微信生态数据）

任务：

创建 wx_users、cms_articles、wx_push_tasks 集合

测试通过 SDK 写入和读取

检查点：

小程序/公众号可以读取 CloudBase 数据

与 PostgreSQL 用户表可对应 user_id

输出产物：

云端可用的微信生态数据集合

数据接口可被 Flask 服务调用

4️⃣ 数据同步与初始化脚本

任务：

写一个 Python 脚本，初始化 PostgreSQL + Neo4j 的测试数据

实现 PostgreSQL → Neo4j 自动同步（新成员/关系自动创建节点/关系）

输出产物：

家庭成员、关系、记忆初始数据

自动同步脚本

🔑 第一步完成目标

核心数据库可用：PostgreSQL + pgvector + Neo4j + CloudBase

基础表、节点、集合初始化完成

数据结构与最终架构完全对应

可提供测试数据给后端 API、AI 模型和前端 UI 使用

💡 第一步小贴士：

建议先用 Docker Compose 启动 PostgreSQL + Neo4j

测试 pgvector 的向量检索能力

Neo4j 初期先用小规模家庭数据，验证关系查询

CloudBase 可用腾讯开发者工具先测试 SDK 写入/读取

以下是 **第一步的数据库初始化脚本 + Docker Compose 文件**，可以直接部署在本地或腾讯云进行测试。

---

# **1️⃣ Docker Compose（PostgreSQL + pgvector + Neo4j）**

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:15
    container_name: postgres_family
    environment:
      POSTGRES_USER: family_user
      POSTGRES_PASSWORD: Family@123
      POSTGRES_DB: family_db
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

  neo4j:
    image: neo4j:5
    container_name: neo4j_family
    environment:
      NEO4J_AUTH: neo4j/Family@123
      NEO4JLABS_PLUGINS: '["apoc"]'
    ports:
      - "7474:7474"   # Browser
      - "7687:7687"   # Bolt
    volumes:
      - neo4j_data:/data

volumes:
  pg_data:
  neo4j_data:
```

> 使用方法：
>
> 1. `docker-compose up -d` 启动
> 2. PostgreSQL: `localhost:5432`，Neo4j: `localhost:7474` 浏览器访问

---

# **2️⃣ PostgreSQL 初始化脚本（Python + SQLAlchemy + pgvector）**

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector

DATABASE_URL = "postgresql://family_user:Family@123@localhost:5432/family_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# --- Tables ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    avatar_url = Column(String)
    created_at = Column(TIMESTAMP)

class Family(Base):
    __tablename__ = "families"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    created_at = Column(TIMESTAMP)

class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    name = Column(String)
    role = Column(String)
    avatar_url = Column(String)
    is_virtual = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP)

class MemoryRecord(Base):
    __tablename__ = "memory_records"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    member_id = Column(Integer, ForeignKey("family_members.id"))
    content = Column(Text)
    tags = Column(ARRAY(String))
    created_at = Column(TIMESTAMP)

class MemoryEmbedding(Base):
    __tablename__ = "memory_embeddings"
    id = Column(Integer, primary_key=True, index=True)
    memory_id = Column(Integer, ForeignKey("memory_records.id"))
    embedding = Column(Vector(1536))
    created_at = Column(TIMESTAMP)

# --- Create tables ---
Base.metadata.create_all(bind=engine)

# --- Insert sample data ---
from datetime import datetime

user = User(name="余哥", email="yuge@example.com", avatar_url="", created_at=datetime.now())
session.add(user)
session.commit()

family = Family(owner_id=user.id, name="余氏家族", created_at=datetime.now())
session.add(family)
session.commit()

member1 = FamilyMember(family_id=family.id, name="爸爸", role="父亲", is_virtual=False, created_at=datetime.now())
member2 = FamilyMember(family_id=family.id, name="妈妈", role="母亲", is_virtual=False, created_at=datetime.now())
session.add_all([member1, member2])
session.commit()

print("✅ PostgreSQL 初始化完成，示例数据已插入。")
```

> 使用方法：
>
> 1. 安装依赖：
>
> ```bash
> pip install sqlalchemy psycopg2-binary pgvector
> ```
>
> 2. 运行 `python init_postgres.py`，即可生成表和示例数据

---

# **3️⃣ Neo4j 初始化脚本（Python + Neo4j Bolt）**

```python
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Family@123"))

def init_graph(tx):
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:FamilyMember) REQUIRE m.id IS UNIQUE")
    tx.run("MERGE (p:FamilyMember {id:1, name:'爸爸', role:'父亲'})")
    tx.run("MERGE (m:FamilyMember {id:2, name:'妈妈', role:'母亲'})")
    tx.run("MERGE (p)-[:SPOUSE_OF]->(m)")

with driver.session() as session:
    session.write_transaction(init_graph)

print("✅ Neo4j 图谱初始化完成，示例家庭关系已创建。")
```

> 使用方法：
>
> ```bash
> pip install neo4j
> python init_neo4j.py
> ```

---

# 🔹 **第一步完成效果**

1. PostgreSQL + pgvector 可插入用户、家庭、成员和记忆向量
2. Neo4j 家庭图谱节点和关系可查询
3. 你可以开始构建 Flask 微服务调用这两层数据库
4. CloudBase 可先测试 SDK 与微信生态的集成

---

我给你整理了一个 **完整的 TRAE 指令/提示词模板**，可以直接粘贴到字节跳动 TRAE 上执行，用来检查你第一步的数据库初始化是否符合孝宝系统要求（PostgreSQL + pgvector + Neo4j + 示例数据）。

---

# **TRAE 指令模板**

```
请帮我检查当前孝宝系统第一步数据库初始化是否正确，并验证如下内容：

1️⃣ PostgreSQL + pgvector
- 数据库名称: family_db
- 表是否存在: users, families, family_members, memory_records, memory_embeddings, chat_messages, devices, mcp_sessions
- 每张表至少有一个示例数据
- memory_embeddings 表是否支持向量查询（pgvector cosine similarity）
- 表结构字段类型是否正确，如：
    - memory_embeddings.embedding 为 VECTOR(1536)
    - family_members.is_virtual 为 BOOLEAN
- 是否可以通过 SQL 查询关联数据（如 family_members.family_id 对应 families.id）

2️⃣ Neo4j 家庭图谱
- 数据库是否可访问（bolt://localhost:7687）
- 节点类型 FamilyMember 是否存在
- 节点至少包含两条示例数据（如 爸爸、妈妈）
- 关系是否存在：
    - SPOUSE_OF（配偶）
    - PARENT_OF（父子）
    - SIBLING_OF（兄弟姐妹）
- 是否可用 Cypher 查询返回家庭树

3️⃣ CloudBase（微信生态）
- 集合 wx_users, cms_articles, wx_push_tasks 是否存在
- 每个集合至少有一条测试数据
- 是否可以通过 CloudBase SDK / API 读取数据

4️⃣ 测试结果
- 每项检查的通过/失败状态
- 提示任何缺失或错误的表、节点、关系、字段或数据

请以清晰表格或列表形式输出检查结果。
```

---

你只需要：

1. 打开 TRAE 控制台
2. 粘贴以上内容到命令行/提示输入框
3. 执行

TRAE 会帮你检查数据库结构、示例数据和可查询性，并给出每一项的**通过/失败状态**。

