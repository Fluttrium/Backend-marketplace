from uuid import UUID

from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_user
from app.orders.lines.dao import OrderLineDAO
from app.orders.lines.exceptions import OrderLineNotFoundException
from app.orders.lines.schemas import SOrderLineCreate
from app.users.models import Users


router = APIRouter(prefix="/{order_id}/lines")


async def create_order_line(
    order_id: UUID,
    order_line_data: SOrderLineCreate,
    user: Users = Depends(get_current_user),
):
    order_line = await OrderLineDAO.add(user, order_id, order_line_data)

    if not order_line:
        raise OrderLineNotFoundException

    return order_line
