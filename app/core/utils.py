from fastapi.exceptions import HTTPException


def check_ownership(
        user_id: int,
        author_id: int,
        detail: str = "Forbidden",
        status_code: int = 403
) -> None:
    if user_id != author_id:
        raise HTTPException(
            detail=detail,
            status_code=status_code
        )
