from decimal import Decimal

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.database import SessionLocal
from app.models.grind_pass import GrindPass
from app.models.mill import Mill
from app.serializers import grind_pass_json
from app.utils import error, normalize_datetime

bp = Blueprint("grind_passes", __name__, url_prefix="/api/grind-passes")


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

    started_at = str(body.get("startedAt", "")).strip()
    if not started_at:
        return "开始时间不能为空"

    pass_no = int(body.get("passNo") or 0)
    if pass_no < 1:
        return "遍次编号必须 ≥ 1"

    duration_min = float(body.get("durationMin") or 0)
    if duration_min <= 0:
        return "研磨时长(分钟)必须大于 0"

    media_type = str(body.get("mediaType", "")).strip()
    if not media_type:
        return "研磨介质不能为空"

    operator_name = str(body.get("operatorName", "")).strip()
    if not operator_name:
        return "操作员不能为空"

    return None


@bp.get("")
@jwt_required()
def list_passes():
    db = SessionLocal()
    try:
        rows = (
            db.query(GrindPass)
            .order_by(GrindPass.started_at.desc(), GrindPass.id.desc())
            .all()
        )
        return jsonify([grind_pass_json(r) for r in rows])
    finally:
        db.close()


@bp.post("")
@jwt_required()
def create_pass():
    body = request.get_json(silent=True) or {}
    err = _validate(body)
    if err:
        return error(err, 400)

    db = SessionLocal()
    try:
        row = GrindPass(
            mill_id=int(body["millId"]),
            started_at=normalize_datetime(str(body["startedAt"])),
            pass_no=int(body["passNo"]),
            duration_min=Decimal(str(body["durationMin"])),
            media_type=str(body["mediaType"]).strip(),
            operator_name=str(body["operatorName"]).strip(),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return jsonify(grind_pass_json(row)), 201
    finally:
        db.close()


@bp.put("/<int:item_id>")
@jwt_required()
def update_pass(item_id: int):
    body = request.get_json(silent=True) or {}
    err = _validate(body)
    if err:
        return error(err, 400)

    db = SessionLocal()
    try:
        row = db.get(GrindPass, item_id)
        if not row:
            return error("研磨遍次不存在", 404)

        row.mill_id = int(body["millId"])
        row.started_at = normalize_datetime(str(body["startedAt"]))
        row.pass_no = int(body["passNo"])
        row.duration_min = Decimal(str(body["durationMin"]))
        row.media_type = str(body["mediaType"]).strip()
        row.operator_name = str(body["operatorName"]).strip()
        db.commit()
        db.refresh(row)
        return jsonify(grind_pass_json(row))
    finally:
        db.close()


@bp.delete("/<int:item_id>")
@jwt_required()
def delete_pass(item_id: int):
    db = SessionLocal()
    try:
        row = db.get(GrindPass, item_id)
        if not row:
            return error("研磨遍次不存在", 404)
        db.delete(row)
        db.commit()
        return jsonify({"ok": True})
    finally:
        db.close()
