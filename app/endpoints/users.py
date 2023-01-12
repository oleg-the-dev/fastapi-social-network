from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from core.dependencies import get_current_user
from core.utils import check_ownership
from database.managers.users import user_manager
from database.models.users import User
from schemas.users import UserCreateUpdate, UserDB

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserDB]
)
def get_users() -> list[User]:
    users = user_manager.get_all()
    return users


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDB
)
def get_user(user_id: int) -> User:
    user = user_manager.get_or_404({"id": user_id})
    return user


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDB
)
def create_user(user_data: UserCreateUpdate) -> User:
    email_exists = user_manager.get({"email": user_data.email})
    if email_exists:
        raise HTTPException(
            detail="Invalid email",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    new_user = user_manager.create(user_data)
    return new_user


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDB
)
def update_user(
        user_id: int,
        user_data: UserCreateUpdate,
        current_user: User = Depends(get_current_user)
) -> User:
    check_ownership(
        current_user.id,
        user_id,
        "You can update only your own account"
    )
    user_db = user_manager.get_or_404({"id": user_id})
    if user_db.email != user_data.email:
        email_exists = user_manager.get({"email": user_data.email})
        if email_exists:
            raise HTTPException(
                detail="Invalid email",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    updated_user = user_manager.update(user_db, user_data)
    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK
)
def delete_user(
        user_id: int,
        current_user: User = Depends(get_current_user)
) -> None:
    check_ownership(
        current_user.id,
        user_id,
        "You can delete only your own account"
    )
    user_to_delete = user_manager.get_or_404({"id": user_id})
    user_manager.delete(user_to_delete)
