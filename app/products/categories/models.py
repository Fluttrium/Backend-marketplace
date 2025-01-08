
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.products.models import Product# noqa


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=True
    )

    products = relationship("Product", back_populates="category")
    variation = relationship("Variation", back_populates="category")
    children_categories = relationship("ProductCategory", lazy="subquery")
