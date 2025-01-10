from decimal import Decimal
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from app.products.items.utils import pick

from app.variations.options.models import VariationOption


class ProductItem(Base):
    __tablename__ = "product_items"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    SKU: Mapped[str] = mapped_column(default=pick(1))
    price: Mapped[Decimal] = mapped_column(nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(default=0)
    product_image: Mapped[str] = mapped_column(nullable=False)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )

    product = relationship("Product", back_populates="product_items")

    variations: Mapped[list["VariationOption"]] = relationship(  # noqa
        back_populates="product_items",
        secondary="configuration_product",
    )
    products_in_order = relationship(
        "OrderLine", back_populates="product_item"
    )



