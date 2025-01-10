from sqlalchemy.orm import Mapped, relationship,mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str]

    addresses = relationship("Address", back_populates="country")
