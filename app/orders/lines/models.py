from decimal import Decimal
import uuid
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from app.products.items.models import ProductItem  # noqa
# from app.users.reviews.models import UserReview  # noqa


class OrderLine(Base):
    __tablename__ = "order_lines"

    id:  Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("product_items.id", ondelete="CASCADE"), nullable=False
    )
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[Decimal] = mapped_column(nullable=False)

    product_item = relationship(
        "ProductItem", back_populates="products_in_order"
    )
    order = relationship("Order", back_populates="products_in_order")
    #  reviews = relationship("UserReview", back_populates="ordered_product")
