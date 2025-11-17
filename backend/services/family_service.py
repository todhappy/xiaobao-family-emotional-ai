from flask import Blueprint, request, jsonify
from backend.db.postgres import get_session
from backend.models import FamilyMember

family_bp = Blueprint("family", __name__, url_prefix="/api/v1/family")

@family_bp.route("/member/add", methods=["POST"])
def add_member():
    data = request.json
    session = next(get_session())
    member = FamilyMember(
        family_id=data["family_id"],
        name=data["name"],
        role=data.get("role", ""),
        is_virtual=data.get("is_virtual", False)
    )
    session.add(member)
    session.commit()
    return jsonify({"member_id": member.id})

@family_bp.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    session = next(get_session())
    member = session.get(FamilyMember, member_id)
    if member:
        return jsonify({"id": member.id, "name": member.name, "role": member.role})
    return jsonify({"error": "Not found"}), 404