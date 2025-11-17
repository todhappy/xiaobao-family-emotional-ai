from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector

Base = declarative_base()

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