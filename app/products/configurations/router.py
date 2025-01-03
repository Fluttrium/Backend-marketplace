from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.users.dependencies import get_current_user
from app.exceptions import raise_http_exception
from app.products.configurations.dao import ProductConfigurationDAO
from app.products.configurations.exceptions import (
    ProductConfigurationNotImplementedException,
    ProductConfigurationsNotFoundException,
)

from app.products.configurations.schemas import (
    SProductConfiguration,
    SProductConfigurations,
)
from app.users.models import Users


router = APIRouter(prefix="/configurations")


@router.post(
    "",
    name="Create a product configuration.",
    response_model=SProductConfiguration,

)
async def create_product_configuration(
    configuration_data: Annotated[SProductConfiguration, Depends()],
    user: Users = Depends(get_current_user),
):
    product_configuration = await ProductConfigurationDAO.add(
        user, configuration_data
    )

    if not product_configuration:
        raise raise_http_exception(ProductConfigurationNotImplementedException)

    return product_configuration


@router.get(
    "",
    name="Get all product configurations.",
    response_model=SProductConfigurations,

)
async def get_product_configurations():
    product_configurations = await ProductConfigurationDAO.find_all()

    if not product_configurations:
        raise_http_exception(ProductConfigurationsNotFoundException)

    return {"product_configurations": product_configurations}


@router.delete(
    "",
    name="Delete certain product configuration.",
    status_code=status.HTTP_204_NO_CONTENT,

)
async def delete_variation(
    configuration_data: Annotated[SProductConfiguration, Depends()],
    user: Users = Depends(get_current_user),
):
    product_configuration = await ProductConfigurationDAO.delete(
        user, configuration_data
    )

    if not product_configuration:
        return {"detail": "The product configuration was deleted."}
