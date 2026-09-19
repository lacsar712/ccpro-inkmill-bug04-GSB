from datetime import datetime, timedelta
from decimal import Decimal

from app.auth import hash_password
from app.database import SessionLocal
from app.models.grind_pass import GrindPass
from app.models.mill import Mill
from app.models.user import User
from app.models.viscosity_sample import ViscositySample
from app.models.workshop import Workshop


def seed() -> None:
    db = SessionLocal()
    try:
        for username, display_name, role in [
            ("admin", "系统管理员", "admin"),
            ("grinder", "研磨工", "grinder"),
        ]:
            if not db.query(User).filter(User.username == username).first():
                db.add(
                    User(
                        username=username,
                        password_hash=hash_password("123456"),
                        display_name=display_name,
                        role=role,
                    )
                )
        db.commit()

        if db.query(Workshop).count() == 0:
            w1 = Workshop(name="一号油墨车间", site="厂区 A 栋", notes="高固含色浆线")
            w2 = Workshop(name="调墨中心", site="厂区 B 栋", notes="小批量专色")
            db.add_all([w1, w2])
            db.flush()

            m1 = Mill(
                workshop_id=w1.id,
                mill_code="M-01",
                pigment_base="酞菁蓝载体",
                bowl_liters=Decimal("25.00"),
                status="grinding",
            )
            m2 = Mill(
                workshop_id=w1.id,
                mill_code="M-02",
                pigment_base="炭黑载体",
                bowl_liters=Decimal("18.50"),
                status="idle",
            )
            m3 = Mill(
                workshop_id=w2.id,
                mill_code="M-A1",
                pigment_base="专色红载体",
                bowl_liters=Decimal("12.00"),
                status="wash",
            )
            db.add_all([m1, m2, m3])
            db.flush()

            now = datetime.now()
            db.add_all(
                [
                    ViscositySample(
                        mill_id=m1.id,
                        sampled_at=now - timedelta(hours=2),
                        viscosity_pa_s=Decimal("12.5000"),
                        temp_c=Decimal("28.50"),
                        notes="首检合格",
                    ),
                    ViscositySample(
                        mill_id=m1.id,
                        sampled_at=now - timedelta(minutes=30),
                        viscosity_pa_s=Decimal("9.8000"),
                        temp_c=Decimal("29.00"),
                        notes="二检微调",
                    ),
                    ViscositySample(
                        mill_id=m2.id,
                        sampled_at=now - timedelta(days=1),
                        viscosity_pa_s=Decimal("15.2000"),
                        temp_c=Decimal("27.00"),
                        notes=None,
                    ),
                    GrindPass(
                        mill_id=m1.id,
                        started_at=now - timedelta(hours=3),
                        pass_no=1,
                        duration_min=Decimal("45.00"),
                        media_type="0.8mm 锆珠",
                        operator_name="张研磨",
                    ),
                    GrindPass(
                        mill_id=m1.id,
                        started_at=now - timedelta(hours=2),
                        pass_no=2,
                        duration_min=Decimal("38.00"),
                        media_type="0.8mm 锆珠",
                        operator_name="张研磨",
                    ),
                    GrindPass(
                        mill_id=m2.id,
                        started_at=now - timedelta(days=5),
                        pass_no=1,
                        duration_min=Decimal("60.00"),
                        media_type="1.0mm 玻璃珠",
                        operator_name="李工",
                    ),
                ]
            )
            db.commit()
            print("Seed data inserted.")
        else:
            print("Seed skipped (workshops exist).")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
