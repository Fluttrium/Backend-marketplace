import uuid
from datetime import date
from decimal import Decimal
from uuid import UUID


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.orders.lines.models import OrderLine  # noqa
from app.orders.statuses.models import OrderStatus  # noqa
# from app.payments.methods.models import PaymentMethod  # noqa
from app.shipping_methods.models import ShippingMethod  # noqa


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    order_date: Mapped[date] = mapped_column(nullable=False)
    #    payment_method_id: Mapped[UUID] = mapped_column(
    #    ForeignKey("payment_methods.id", ondelete="CASCADE"),
    #    nullable=False,
    #  )
    shipping_address_id: Mapped[UUID] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False
    )
    shipping_method_id: Mapped[int] = mapped_column(
        ForeignKey("shipping_methods.id", ondelete="CASCADE"), nullable=False
    )
    order_total: Mapped[Decimal] = mapped_column(nullable=False)
    order_status_id: Mapped[int] = mapped_column(
        ForeignKey("order_statuses.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("Users", back_populates="orders")
    # payment_method = relationship("PaymentMethod", back_populates="orders")
    shipping_address = relationship("Address", back_populates="orders")
    shipping_method = relationship("ShippingMethod", back_populates="orders")
    order_status = relationship("OrderStatus", back_populates="orders")
    products_in_order = relationship("OrderLine", back_populates="order")
