from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.database import SessionLocal
from app.models.workshop import Workshop
from app.serializers import workshop_json
from app.utils import error

bp = Blueprint("workshops", __name__, url_prefix="/api/workshops")


@bp.get("")
@jwt_required()
def list_workshops():
    db = SessionLocal()
    try:
        rows = db.query(Workshop).order_by(Workshop.id.desc()).all()
        return jsonify([workshop_json(r) for r in rows])
    finally:
        db.close()


@bp.post("")
@jwt_required()
def create_workshop():
    body = request.get_json(silent=True) or {}
    name = str(body.get("name", "")).strip()
    if not name:
        return error("车间名称不能为空", 400)

    site = str(body.get("site", "")).strip() or None
    notes = str(body.get("notes", "")).strip() or None

    db = SessionLocal()
    try:
        row = Workshop(name=name, site=site, notes=notes)
        db.add(row)
        db.commit()
        db.refresh(row)
        return jsonify(workshop_json(row)), 201
    finally:
        db.close()


@bp.put("/<int:item_id>")
@jwt_required()
def update_workshop(item_id: int):
    db = SessionLocal()
    try:
        row = db.get(Workshop, item_id)
        if not row:
            return error("车间不存在", 404)

        body = request.get_json(silent=True) or {}
        name = str(body.get("name", "")).strip()
        if not name:
            return error("车间名称不能为空", 400)

        row.name = name
        row.site = str(body.get("site", "")).strip() or None
        row.notes = str(body.get("notes", "")).strip() or None
        db.commit()
        db.refresh(row)
        return jsonify(workshop_json(row))
    finally:
        db.close()


@bp.delete("/<int:item_id>")
@jwt_required()
def delete_workshop(item_id: int):
    db = SessionLocal()
    try:
        row = db.get(Workshop, item_id)
        if not row:
            return error("车间不存在", 404)
        db.delete(row)
        db.commit()
        return jsonify({"ok": True})
    finally:
        db.close()
