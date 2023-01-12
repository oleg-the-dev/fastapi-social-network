from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.security import verify_access_token
from database.managers.users import user_manager
from database.models.users import User

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(
        token: str = Depends(oauth_scheme)
) -> User:
    token_data = verify_access_token(token)
    user = user_manager.get_or_404({"id": token_data.id})
    return user
