from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, Text, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
import os

DATABASE_URL = os.getenv("FAMILY_DB_URL", "postgresql://family_user:Family@123@localhost:5432/family_db")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

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

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    member_id = Column(Integer, ForeignKey("family_members.id"))
    role = Column(String)
    content = Column(Text)
    created_at = Column(TIMESTAMP)

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    type = Column(String)
    platform = Column(String)
    created_at = Column(TIMESTAMP)

class MCPSession(Base):
    __tablename__ = "mcp_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_token = Column(String)
    status = Column(String)
    created_at = Column(TIMESTAMP)

Base.metadata.create_all(bind=engine)

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

memory = MemoryRecord(family_id=family.id, member_id=member1.id, content="家庭聚餐记忆", tags=["聚餐", "家庭"], created_at=datetime.now())
session.add(memory)
session.commit()

embedding_vector = [0.1] * 1536
embedding = MemoryEmbedding(memory_id=memory.id, embedding=embedding_vector, created_at=datetime.now())
session.add(embedding)
session.commit()

msg = ChatMessage(family_id=family.id, member_id=member1.id, role="assistant", content="欢迎加入家庭系统", created_at=datetime.now())
session.add(msg)
session.commit()

device = Device(user_id=user.id, name="iPhone", type="mobile", platform="iOS", created_at=datetime.now())
session.add(device)
session.commit()

mcp = MCPSession(user_id=user.id, session_token="token-demo", status="active", created_at=datetime.now())
session.add(mcp)
session.commit()

print("PostgreSQL 初始化完成，核心表与示例数据已插入。")