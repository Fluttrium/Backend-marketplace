from fastapi import APIRouter, Depends, Response,HTTPException
from app.logger import logger

from app.exceptions import (
    CannotAddDataToDatabase,
    UserAlreadyExistsException,
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    """
    Регистрация нового пользователя.
    """
    try:
        # Проверяем, существует ли пользователь
        existing_user = await UserDAO.find_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        hashed_password = get_password_hash(user_data.password)

        # Добавляем нового пользователя
        new_user = await UserDAO.add(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        # Проверяем успешность добавления
        if not new_user:
            raise CannotAddDataToDatabase

        # Возвращаем информацию о новом пользователе
        return {"id": str(new_user.id), "email": new_user.email}

    except UserAlreadyExistsException:
        logger.warning(f"User already exists: {user_data.email}")
        raise HTTPException(status_code=400, detail="User already exists")

    except CannotAddDataToDatabase:
        logger.error(f"Failed to add user to database: {user_data.email}")
        raise HTTPException(status_code=500, detail="Failed to add user to database")

    except Exception as e:
        logger.error(f"Unhandled exception during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        "booking_access_token",
        access_token,
        httponly=True,
        samesite="none",
        secure=True  
    )

    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
