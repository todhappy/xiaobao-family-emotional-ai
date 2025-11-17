from sqlalchemy import create_engine, text
import os
from neo4j import GraphDatabase

PG_URL = os.getenv("FAMILY_DB_URL", "postgresql://family_user:Family@123@localhost:5432/family_db")
engine = create_engine(PG_URL)

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "Family@123")
driver = GraphDatabase.driver(uri, auth=(user, password))

def ensure_constraints(tx):
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:FamilyMember) REQUIRE m.id IS UNIQUE")

def merge_member(tx, mid, name, role, avatar_url):
    tx.run(
        "MERGE (m:FamilyMember {id:$id}) SET m.name=$name, m.role=$role, m.avatar_url=$avatar_url",
        id=mid,
        name=name,
        role=role,
        avatar_url=avatar_url,
    )

def merge_relation(tx, a_id, b_id, rel):
    tx.run(
        "MATCH (a:FamilyMember {id:$a}), (b:FamilyMember {id:$b}) MERGE (a)-[r:%s]->(b)" % rel,
        a=a_id,
        b=b_id,
    )

with driver.session() as gsession, engine.connect() as conn:
    gsession.execute_write(ensure_constraints)

    members = conn.execute(text("SELECT id, name, role, COALESCE(avatar_url,'') FROM family_members"))
    for row in members:
        gsession.execute_write(merge_member, row[0], row[1], row[2], row[3])

    rel_table_exists = conn.dialect.has_table(conn, "family_relationships")
    if rel_table_exists:
        rels = conn.execute(text("SELECT from_member_id, to_member_id, type FROM family_relationships"))
        for r in rels:
            rel_type = r[2]
            if rel_type in ("SPOUSE_OF", "PARENT_OF", "SIBLING_OF"):
                gsession.execute_write(merge_relation, r[0], r[1], rel_type)

print("PostgreSQL → Neo4j 同步完成。")