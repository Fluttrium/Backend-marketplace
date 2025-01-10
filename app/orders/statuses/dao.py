from sqlalchemy import select

from app.dao.base import BaseDAO
from app.exceptions import ForbiddenException, raise_http_exception
from app.orders.statuses.exceptions import (
    OrderStatusAlreadyExistsException,
    OrderStatusNotFoundException,
)
from app.orders.statuses.models import OrderStatus
from app.utils.permision import  has_permission
from app.shipping_methods.exceptions import (
    ShippingMethodWithNameAlreadyExistsException,
)
from app.users.models import Users
from app.utils.data import get_new_data
from app.utils.manage import manage_session


class OrderStatusDAO(BaseDAO):
    model = OrderStatus

    @classmethod
    @manage_session
    async def add(cls, user: Users, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        existing_order_status = await cls.find_one_or_none(
            status=data["status"]
        )

        if existing_order_status:
            raise_http_exception(OrderStatusAlreadyExistsException)

        return await cls._create(**data)

    @classmethod
    @manage_session
    async def find_all(cls, session=None):
        query = select(cls.model).order_by(cls.model.id)

        result = await session.execute(query)

        values = result.scalars().all()

        return values

    @classmethod
    @manage_session
    async def change(cls, order_status_id, user, data, session=None):
        data = data.model_dump(exclude_unset=True)

        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        current_order_status = await cls.find_one_or_none(id=order_status_id)

        if not current_order_status:
            return None

        if not data:
            return current_order_status

        new_order_status_data = get_new_data(current_order_status, data)

        existing_order_status = await cls.find_one_or_none(
            **new_order_status_data
        )

        if (
            existing_order_status
            and existing_order_status.id != order_status_id
        ):
            raise_http_exception(ShippingMethodWithNameAlreadyExistsException)

        return await cls.update_data(order_status_id, data)

    @classmethod
    @manage_session
    async def delete(cls, user, order_status_id, session=None):
        if not await has_permission(user):
            raise_http_exception(ForbiddenException)

        # Get current order status
        order_status = await cls.find_one_or_none(id=order_status_id)

        if not order_status:
            raise_http_exception(OrderStatusNotFoundException)

        # Delete the order status
        await cls.delete_certain_item(order_status_id)
