from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.auth import verify_password
from app.database import SessionLocal
from app.models.user import User
from app.serializers import user_json
from app.utils import error

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    username = str(body.get("username", "")).strip()
    password = str(body.get("password", ""))

    if not username or not password:
        return error("请输入账号和密码", 400)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            return error("账号或密码错误", 401)

        token = create_access_token(identity=user.username)
        return jsonify({"accessToken": token, "user": user_json(user)})
    finally:
        db.close()


@bp.get("/me")
@jwt_required()
def me():
    db = SessionLocal()
    try:
        username = get_jwt_identity()
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return error("未登录或登录已过期", 401)
        return jsonify(user_json(user))
    finally:
        db.close()
