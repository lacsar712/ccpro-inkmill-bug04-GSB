from decimal import Decimal

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.database import SessionLocal
from app.models.mill import Mill
from app.models.viscosity_sample import ViscositySample
from app.serializers import viscosity_sample_json
from app.utils import error, normalize_datetime

bp = Blueprint("viscosity_samples", __name__, url_prefix="/api/viscosity-samples")


def _validate(body: dict) -> str | None:
    mill_id = int(body.get("millId") or 0)
    if mill_id <= 0:
        return "请选择研磨机"

    db = SessionLocal()
    try:
        if not db.get(Mill, mill_id):
            return "研磨机不存在"
    finally:
        db.close()

    sampled_at = str(body.get("sampledAt", "")).strip()
    if not sampled_at:
        return "取样时间不能为空"

    viscosity = float(body.get("viscosityPaS") or 0)
    if viscosity <= 0:
        return "粘度(Pa·s)必须大于 0"

    return None


@bp.get("")
@jwt_required()
def list_samples():
    db = SessionLocal()
    try:
        rows = (
            db.query(ViscositySample)
            .order_by(ViscositySample.sampled_at.desc(), ViscositySample.id.desc())
            .all()
        )
        return jsonify([viscosity_sample_json(r) for r in rows])
    finally:
        db.close()


@bp.post("")
@jwt_required()
def create_sample():
    body = request.get_json(silent=True) or {}
    err = _validate(body)
    if err:
        return error(err, 400)

    temp_raw = body.get("tempC")
    temp_c = None
    if temp_raw is not None and temp_raw != "":
        temp_c = Decimal(str(temp_raw))

    db = SessionLocal()
    try:
        row = ViscositySample(
            mill_id=int(body["millId"]),
            sampled_at=normalize_datetime(str(body["sampledAt"])),
            viscosity_pa_s=Decimal(str(body["viscosityPaS"])),
            temp_c=temp_c,
            notes=str(body.get("notes", "")).strip() or None,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return jsonify(viscosity_sample_json(row)), 201
    finally:
        db.close()


@bp.put("/<int:item_id>")
@jwt_required()
def update_sample(item_id: int):
    body = request.get_json(silent=True) or {}
    err = _validate(body)
    if err:
        return error(err, 400)

    temp_raw = body.get("tempC")
    temp_c = None
    if temp_raw is not None and temp_raw != "":
        temp_c = Decimal(str(temp_raw))

    db = SessionLocal()
    try:
        row = db.get(ViscositySample, item_id)
        if not row:
            return error("粘度取样记录不存在", 404)

        row.mill_id = int(body["millId"])
        row.sampled_at = normalize_datetime(str(body["sampledAt"]))
        row.viscosity_pa_s = Decimal(str(body["viscosityPaS"]))
        row.temp_c = temp_c
        row.notes = str(body.get("notes", "")).strip() or None
        db.commit()
        db.refresh(row)
        return jsonify(viscosity_sample_json(row))
    finally:
        db.close()


@bp.delete("/<int:item_id>")
@jwt_required()
def delete_sample(item_id: int):
    db = SessionLocal()
    try:
        row = db.get(ViscositySample, item_id)
        if not row:
            return error("粘度取样记录不存在", 404)
        db.delete(row)
        db.commit()
        return jsonify({"ok": True})
    finally:
        db.close()
