from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.addresses.dao import AddressDAO
from app.addresses.exceptions import (
    AddressNotImplementedException,
    NoSuchAddressException,
    UserHasNoAddressesException,
)
from app.addresses.responses import (
    DELETED_UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_ADDRESS_NOT_FOUND_RESPONSE,
    UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
from app.addresses.schemas import (
    SAddress,
    SAddressCountry,
    SAddressCreate,
    SAddressOptional,
    SAllUserAddresses,
    SAllUsersAddresses,
)
from app.users.dependencies import get_current_user
from app.addresses.countries.responses import (
    UNAUTHORIZED_COUNTRY_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
from app.examples import example_address
from app.users.models import Users


router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post(
    "",
    response_model=SAddress,
    name="Add address.",
    responses=UNAUTHORIZED_COUNTRY_NOT_FOUND_UNPROCESSABLE_RESPONSE,
)
async def add_address(
    address_data: SAddressCreate = example_address,
    user: Users = Depends(get_current_user),
):
    address = await AddressDAO.add(user, **address_data.model_dump())

    if not address:
        raise AddressNotImplementedException

    return address


@router.post(
    "/{address_id}/set_default",
    name="Set an address to default.",
    responses=UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def set_address_to_default(
    address_id: UUID, user: Users = Depends(get_current_user)
):
    address = await AddressDAO.set_to_default(address_id, user)

    if not address:
        raise NoSuchAddressException

    return address


@router.get(
    "",
    response_model=Union[SAllUsersAddresses, SAllUserAddresses],
    name="Get all User addresses.",
    responses=UNAUTHORIZED_ADDRESS_NOT_FOUND_RESPONSE,
)
async def get_user_addresses(user: Users = Depends(get_current_user)):
    addresses = await AddressDAO.find_all(user)

    if not addresses:
        raise UserHasNoAddressesException

    return addresses


@router.get(
    "/{address_id}",
    response_model=SAddressCountry,
    name="Get certain address.",
    responses=UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def get_address_by_id(
    address_id: UUID, user: Users = Depends(get_current_user)
):
    address = await AddressDAO.find_by_id(user, address_id)

    if not address:
        raise NoSuchAddressException

    return address


@router.patch(
    "/{address_id}",
    response_model=SAddressOptional,
    response_model_exclude_none=True,
    name="Change certain address.",
    responses=UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def change_user_address(
    address_id: UUID,
    address_data: SAddressOptional,
    user: Users = Depends(get_current_user),
):
    address = await AddressDAO.change_address(address_id, user, address_data)

    if not address:
        raise NoSuchAddressException

    return address


@router.delete(
    "/{address_id}",
    name="Delete certain address.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETED_UNAUTHORIZED_FORBIDDEN_ADDRESS_NOT_FOUND_RESPONSE,
)
async def delete_user_address(
    address_id: UUID,
    user: Users = Depends(get_current_user),
):
    address = await AddressDAO.delete_address(user, address_id)

    if not address:
        return {"detail": "The address was deleted."}
