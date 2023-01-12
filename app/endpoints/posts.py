from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from core.dependencies import get_current_user
from core.utils import check_ownership
from database.managers.posts import post_manager
from database.managers.users import user_manager
from database.models.users import User
from schemas.posts import PostCreateUpdate, PostDB

router = APIRouter(
    tags=["Posts"],
    prefix="/posts"
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[PostDB]
)
def get_posts():
    posts = post_manager.get_all()
    return posts


@router.get(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostDB
)
def get_post(post_id: int):
    post = post_manager.get_or_404({"id": post_id})
    return post


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PostDB
)
def create_post(
        post_data: PostCreateUpdate,
        current_user: User = Depends(get_current_user)
):
    new_post = post_manager.create(
        post_data,
        user_id=current_user.id
    )
    return new_post


@router.put(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=PostDB
)
def update_post(
        post_id: int,
        post_data: PostCreateUpdate,
        current_user: User = Depends(get_current_user)
):
    post = post_manager.get_or_404({"id": post_id})
    check_ownership(
        current_user.id,
        post.user_id,
        "You can update only your own posts"
    )
    updated_post = post_manager.update(
        post,
        post_data,
        user_id=current_user.id
    )
    return updated_post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
)
def delete_post(
        post_id: int,
        current_user: User = Depends(get_current_user)
) -> None:
    post = post_manager.get_or_404({"id": post_id})
    check_ownership(
        current_user.id,
        post.user_id,
        "You can delete only your own posts"
    )
    post_manager.delete(post)


@router.post(
    "/{post_id}/like",
    status_code=status.HTTP_200_OK,
)
def like_post(
        post_id: int,
        current_user: User = Depends(get_current_user)
) -> None:
    post = post_manager.get_or_404({"id": post_id})
    if current_user.id == post.user_id:
        raise HTTPException(
            detail="You can't like your own post",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user_manager.like_post(current_user.id, post_id)


@router.post(
    "/{post_id}/dislike",
    status_code=status.HTTP_200_OK,
)
def dislike_post(
        post_id: int,
        current_user: User = Depends(get_current_user)
) -> None:
    post = post_manager.get_or_404({"id": post_id})
    if current_user.id == post.user_id:
        raise HTTPException(
            detail="You can't dislike your own post",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user_manager.dislike_post(current_user.id, post_id)
