from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.dependencies import get_current_user
from core.security import create_token
from database.managers.users import user_manager
from database.models.users import User
from schemas.auth import TokenSchema
from schemas.users import UserDB

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=TokenSchema)
def login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    user = user_manager.authenticate(
        user_credentials.username,  # email
        user_credentials.password,
    )
    access_token = create_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/whoami", response_model=UserDB)
def whoami(
    current_user: User = Depends(get_current_user)
) -> User:
    return current_user
