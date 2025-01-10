from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
import uuid
from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        # Расшифровка токена
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    # Получение user_id из токена
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    # Проверка, что user_id имеет формат UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise IncorrectTokenFormatException

    # Поиск пользователя по UUID
    user = await UserDAO.find_one_or_none(id=user_uuid)
    if not user:
        raise UserIsNotPresentException
    return user
