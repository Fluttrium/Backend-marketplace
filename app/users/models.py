import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.addresses.models import Address
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.shopping_carts.models import ShoppingCart


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list["Users"]] = relationship("Users", back_populates="role")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # Уникальный email
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)  # Хэшированный пароль
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Состояние аккаунта
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)  # Администраторская роль
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)  # Дата регистрации
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True, default=1)

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="users_living",
        secondary="address_user",
    )
    shopping_cart = relationship("ShoppingCart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    role: Mapped["Role"] = relationship("Role", back_populates="users")


