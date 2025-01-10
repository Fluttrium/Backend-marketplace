from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base



class ShippingMethod(Base):
    __tablename__ = "shipping_methods"

    id: Mapped[int] = mapped_column(primary_key=True, unique=False)
    name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(nullable=False)

    orders = relationship("Order", back_populates="shipping_method")
