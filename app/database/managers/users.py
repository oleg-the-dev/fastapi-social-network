from typing import Any

from database.managers.base import (
    BaseManager, CreateSchemaType, UpdateSchemaType
)
from database.models.posts import PostLike, PostDislike
from database.models.users import User
from core.security import (
    credentials_exception, get_password_hash, verify_password
)

# Create likes/dislikes manager
post_likes_manager = BaseManager(PostLike)
post_dislikes_manager = BaseManager(PostDislike)


class UserManager(BaseManager):
    INSTANCE_NAME = "User"

    def authenticate(self, email: str, password: str) -> User:
        user = self.get_or_404({"email": email})
        if not verify_password(password, user.password):
            raise credentials_exception
        return user

    def create(
            self,
            create_data: CreateSchemaType | dict[str, Any],
            *args,
            **kwargs
    ) -> User:
        create_data.password = get_password_hash(create_data.password)
        new_user = super().create(create_data)
        return new_user

    def update(
            self,
            user_to_update: User,
            update_data: UpdateSchemaType | dict[str, Any],
            *args,
            **kwargs
    ) -> User:
        update_data.password = get_password_hash(update_data.password)
        new_user = super().update(user_to_update, update_data)
        return new_user

    @staticmethod
    def like_post(
            user_id: int,
            post_id: int,
    ) -> None:
        """
        Add like to the post.
        :param user_id: FK from User table
        :param post_id: FK from Post table
        :return: None
        """
        data = {"post_id": post_id, "user_id": user_id}
        post_like = post_likes_manager.get(data)
        post_dislike = post_dislikes_manager.get(data)
        # If post is disliked -> remove dislike and add like to the post
        if post_dislike:
            post_dislikes_manager.delete(post_dislike)
            post_likes_manager.create(data)
        # If post is liked -> remove like
        elif post_like:
            post_likes_manager.delete(post_like)
        # If neither like nor dislike were found in DB -> add like to the post
        else:
            post_likes_manager.create(data)

    @staticmethod
    def dislike_post(
            user_id: int,
            post_id: int,
    ) -> None:
        """
        Add dislike to the post.
        :param user_id: FK from User table
        :param post_id: FK from Post table
        :return: None
        """
        data = {"post_id": post_id, "user_id": user_id}
        post_dislike = post_dislikes_manager.get(data)
        post_like = post_likes_manager.get(data)
        # If post is liked -> remove like and add dislike to the post
        if post_like:
            post_likes_manager.delete(post_like)
            post_dislikes_manager.create(data)
        # If post is disliked -> remove dislike
        elif post_dislike:
            post_dislikes_manager.delete(post_dislike)
        # If neither like nor dislike were found in DB
        # -> add dislike to the post
        else:
            post_dislikes_manager.create(data)


user_manager = UserManager(User)
