from neo4j import GraphDatabase
import os

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "Family@123")
driver = GraphDatabase.driver(uri, auth=(user, password))

def init_constraints(tx):
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:FamilyMember) REQUIRE m.id IS UNIQUE")

def init_data(tx):
    tx.run("MERGE (p:FamilyMember {id:1, name:'爸爸', role:'父亲'})")
    tx.run("MERGE (m:FamilyMember {id:2, name:'妈妈', role:'母亲'})")
    tx.run("MERGE (p)-[:SPOUSE_OF]->(m)")
    tx.run("MERGE (c:FamilyMember {id:3, name:'孩子', role:'子女'})")
    tx.run("MERGE (p)-[:PARENT_OF]->(c)")
    tx.run("MERGE (c2:FamilyMember {id:4, name:'孩子2', role:'子女'})")
    tx.run("MERGE (c)-[:SIBLING_OF]->(c2)")

with driver.session() as session:
    session.execute_write(init_constraints)
    session.execute_write(init_data)

print("Neo4j 图谱初始化完成，示例家庭关系已创建。")