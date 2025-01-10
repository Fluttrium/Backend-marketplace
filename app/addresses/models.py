from uuid import UUID
import uuid

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from  app.addresses.countries.models import Country  # noqa
from app.database import Base
from app.orders.models import Order  # noqa


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    unit_number: Mapped[str]
    street_number: Mapped[str]
    address_line1: Mapped[str]
    address_line2: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str]
    region: Mapped[str]
    postal_code: Mapped[str]
    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id", ondelete="CASCADE")
    )

    country = relationship("Country", back_populates="addresses")

    users_living: Mapped[list["Users"]] = relationship(  # noqa
        back_populates="addresses",
         secondary="address_user",)

    orders = relationship("Order", back_populates="shipping_address")

    __mapper_args__ = {"eager_defaults": True}


class UserAddress(Base):
    __tablename__ = "address_user"
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    address_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("addresses.id", ondelete="CASCADE"), primary_key=True
    )
    is_default: Mapped[bool] = mapped_column(default=True)
