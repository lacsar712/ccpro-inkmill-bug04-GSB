from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

MILL_STATUSES = ("grinding", "idle", "wash")


class Mill(Base):
    __tablename__ = "mills"
    __table_args__ = (UniqueConstraint("workshop_id", "mill_code", name="uq_mill_workshop_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workshop_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workshops.id", ondelete="CASCADE"), nullable=False
    )
    mill_code: Mapped[str] = mapped_column(String(64), nullable=False)
    pigment_base: Mapped[str] = mapped_column(String(128), nullable=False)
    bowl_liters: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="idle")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    workshop: Mapped["Workshop"] = relationship("Workshop", back_populates="mills")
    viscosity_samples: Mapped[list["ViscositySample"]] = relationship(
        "ViscositySample", back_populates="mill"
    )
    grind_passes: Mapped[list["GrindPass"]] = relationship("GrindPass", back_populates="mill")
