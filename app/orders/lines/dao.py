from app.dao.base import BaseDAO
from app.exceptions import raise_http_exception
from app.orders.lines.models import OrderLine
from app.products.items.dao import ProductItemDAO
from app.products.items.exceptions import ProductItemNotFoundException
from app.utils.manage import manage_session


class OrderLineDAO(BaseDAO):
    model = OrderLine

    @classmethod
    @manage_session
    async def add(cls, user, order_id, order_line_data, session=None):
        order_line_data = order_line_data.model_dump(exclude_unset=True)

        # Validate product item
        product_item = await ProductItemDAO.find_one_or_none(
            id=order_line_data["product_item_id"]
        )

        if not product_item:
            raise_http_exception(ProductItemNotFoundException)

        order_line_data.update({"order_id": order_id})

        return await cls._create(**order_line_data)
