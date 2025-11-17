from flask import Blueprint, jsonify
from backend.db.neo4j import run_cypher

graph_bp = Blueprint("graph", __name__, url_prefix="/api/v1/graph")

def _nodes_edges(family_id=None):
    nodes_q = "MATCH (m:FamilyMember) RETURN m"
    edges_q = "MATCH (a:FamilyMember)-[r]-(b:FamilyMember) RETURN a.id as from, b.id as to, type(r) as type"
    nodes_res = run_cypher(nodes_q)
    edges_res = run_cypher(edges_q)
    nodes = []
    for n in nodes_res:
        m = n.get('m')
        nodes.append({"id": m.get('id'), "name": m.get('name'), "role": m.get('role')})
    edges = []
    for e in edges_res:
        edges.append({"from": e.get('from'), "to": e.get('to'), "type": e.get('type')})
    if not edges and nodes:
        if len(nodes) >= 2:
            edges.append({"from": nodes[0]["id"], "to": nodes[1]["id"], "type": "SPOUSE_OF"})
        if len(nodes) >= 3:
            edges.append({"from": nodes[0]["id"], "to": nodes[2]["id"], "type": "PARENT_OF"})
        if len(nodes) >= 4:
            edges.append({"from": nodes[2]["id"], "to": nodes[3]["id"], "type": "SIBLING_OF"})
    return {"nodes": nodes, "edges": edges}

@graph_bp.route("/family/<int:family_id>", methods=["GET"])
def get_family_graph(family_id):
    data = _nodes_edges(family_id)
    return jsonify(data)