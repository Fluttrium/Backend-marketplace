from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.database import Base
from app.products.categories.models import ProductCategory  # noqa


class Variation(Base):
    __tablename__ = "variations"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False
    )

    category = relationship("ProductCategory", back_populates="variation")
    options = relationship("VariationOption", back_populates="variation")
