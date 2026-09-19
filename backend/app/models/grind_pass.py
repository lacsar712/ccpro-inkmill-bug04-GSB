from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GrindPass(Base):
    __tablename__ = "grind_passes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mill_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("mills.id", ondelete="SET NULL"), nullable=True
    )
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pass_no: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_min: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    media_type: Mapped[str] = mapped_column(String(64), nullable=False)
    operator_name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    mill: Mapped["Mill | None"] = relationship("Mill", back_populates="grind_passes")
