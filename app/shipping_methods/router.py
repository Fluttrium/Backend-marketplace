from fastapi import APIRouter, Depends, status

from app.users.dependencies import get_current_user
from app.examples import example_shipping_method
from app.exceptions import raise_http_exception
from app.responses import (UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE)
from app.shipping_methods.dao import ShippingMethodDAO
from app.shipping_methods.exceptions import (
    ShippingMethodNotFoundException,
    ShippingMethodNotImplementedException,
    ShippingMethodsNotFoundException,
)
from app.shipping_methods.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE,
    SHIPPING_METHOD_NOT_FOUND_RESPONSE,
    SHIPPING_METHODS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE,
)
from app.shipping_methods.schemas import (
    SShippingMethod,
    SShippingMethodCreate,
    SShippingMethodCreateOptional,
    SShippingMethods,
)
from app.users.models import Users


router = APIRouter(prefix="/shipping_methods", tags=["Shipping Methods"])


@router.post(
    "",
    response_model=SShippingMethod,
    name="Add shipping method.",
    responses=UNAUTHORIZED_FORBIDDEN_UNPROCESSABLE_RESPONSE,
)
async def add_shipping_method(
    shipping_method_data: SShippingMethodCreate = example_shipping_method,
    user: Users = Depends(get_current_user),
):
    shipping_method = await ShippingMethodDAO.add(user, shipping_method_data)

    if not shipping_method:
        raise ShippingMethodNotImplementedException

    return shipping_method


@router.get(
    "",
    name="Get all shipping methods.",
    response_model=SShippingMethods,
    responses=SHIPPING_METHODS_NOT_FOUND_RESPONSE,
)
async def get_all_shipping_methods():
    shipping_methods = await ShippingMethodDAO.find_all()

    if not shipping_methods:
        raise ShippingMethodsNotFoundException

    return {"shipping_methods": shipping_methods}


@router.get(
    "/{shipping_method_id}",
    name="Get certain product shipping method.",
    response_model=SShippingMethod,
    responses=SHIPPING_METHOD_NOT_FOUND_RESPONSE,
)
async def get_shipping_method_by_id(shipping_method_id: int):
    shipping_method = await ShippingMethodDAO.find_one_or_none(
        id=shipping_method_id
    )

    if not shipping_method:
        raise_http_exception(ShippingMethodNotFoundException)

    return shipping_method


@router.patch(
    "/{shipping_method_id}",
    name="Change certain shipping method.",
    response_model=SShippingMethod,
    responses=UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE,
)
async def change_shipping_method_by_id(
    shipping_method_id: int,
    data: SShippingMethodCreateOptional,
    user: Users = Depends(
        get_current_user
    ),
):
    shipping_method = await ShippingMethodDAO.change(
        shipping_method_id, user, data
    )

    if not shipping_method:
        raise ShippingMethodsNotFoundException

    return shipping_method


@router.delete(
    "/{shipping_method_id}",
    name="Delete certain product category.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_SHIPPING_METHOD_NOT_FOUND_RESPONSE,
)
async def delete_shipping_method_by_id(
    shipping_method_id: int,
    user: Users = Depends(get_current_user),
):
    shipping_method = await ShippingMethodDAO.delete(user, shipping_method_id)

    if not shipping_method:
        return {"detail": "The shipping method was deleted."}
