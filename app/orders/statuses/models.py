from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, unique=False)
    status: Mapped[str]

    orders = relationship("Order", back_populates="order_status")
