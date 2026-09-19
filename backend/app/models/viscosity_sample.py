from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ViscositySample(Base):
    __tablename__ = "viscosity_samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mill_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("mills.id", ondelete="SET NULL"), nullable=True
    )
    sampled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    viscosity_pa_s: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    temp_c: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    mill: Mapped["Mill | None"] = relationship("Mill", back_populates="viscosity_samples")
