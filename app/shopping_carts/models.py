from uuid import UUID
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.shopping_carts.items.models import ShoppingCartItem  # noqa


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("Users", back_populates="shopping_cart")
    cart_items = relationship("ShoppingCartItem", back_populates="cart")
