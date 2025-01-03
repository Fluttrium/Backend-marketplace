from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from starlette import status

from app.users.dependencies import get_current_user
from app.exceptions import raise_http_exception
from app.products.configurations.exceptions import (
    ProductConfigurationsNotFoundException,
)
from app.products.items.dao import ProductItemDAO
from app.products.items.exceptions import (
    ProductItemNotFoundException,
    ProductItemsNotFoundException,
)

from app.products.items.schemas import (
    SProductItem,
    SProductItemCreate,
    SProductItemCreateOptional,
    SProductItems,
    SProductItemWithProduct,
    SProductItemWithVariations,
)


from app.users.models import Users



router = APIRouter(prefix="/items")


@router.post(
    "",
    response_model=SProductItem,
    name="Add product item.",

)
async def create_product_item(
    file: UploadFile = File(...),
    price: Decimal = Form(...),
    quantity_in_stock: int = Form(...),
    product_id: UUID = Form(...),
    user: Users = Depends(get_current_user),
):
    product_item_data = SProductItemCreate(
        price=price, quantity_in_stock=quantity_in_stock, product_id=product_id
    )

    product_item = await ProductItemDAO.add(user, product_item_data, file)

    return product_item


@router.get(
    "",
    name="Get all product items.",
    response_model=SProductItems,

)
async def get_all_product_items():
    product_items = await ProductItemDAO.find_all()

    if not product_items:
        raise_http_exception(ProductItemsNotFoundException)

    return {"product_items": product_items}


@router.get(
    "/{product_item_id}",
    name="Get certain product item.",
    response_model=SProductItemWithProduct,

)
async def get_product_item_by_id(product_item_id: UUID):
    product_item = await ProductItemDAO.find_by_id(product_item_id)

    if not product_item:
        raise_http_exception(ProductItemNotFoundException)

    return product_item


@router.get(
    "/{product_item_id}/configurations",
    name="Get all product item configurations.",
    response_model=SProductItemWithVariations,

)
async def get_product_item_configurations(product_item_id: UUID):
    product_item = await ProductItemDAO.get_product_item_configurations(
        product_item_id
    )

    if not product_item:
        raise_http_exception(ProductItemNotFoundException)

    if not product_item.__dict__["variations"]:
        raise_http_exception(ProductConfigurationsNotFoundException)

    return product_item





@router.patch(
    "/{product_item_id}",
    response_model=SProductItem,
    response_model_exclude_none=True,
    name="Change certain product item.",

)
async def change_product_item_by_id(
    product_item_id: UUID,
    data: SProductItemCreateOptional,
    user: Users = Depends(get_current_user),
):
    product_item = await ProductItemDAO.change(product_item_id, user, data)

    if not product_item:
        raise ProductItemNotFoundException

    return product_item


@router.delete(
    "/{product_item_id}",
    name="Delete certain product item.",
    status_code=status.HTTP_204_NO_CONTENT,


)
async def delete_product_item_by_id(
    product_item_id: UUID,
    user: Users = Depends(get_current_user),
):
    product_item = await ProductItemDAO.delete(user, product_item_id)

    if not product_item:
        return {"detail": "The product item was deleted."}
