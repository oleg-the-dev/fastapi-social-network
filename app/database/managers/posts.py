from typing import Any

from fastapi.encoders import jsonable_encoder

from database.managers.base import (
    BaseManager, CreateSchemaType, UpdateSchemaType
)
from database.models.posts import Post


class PostManager(BaseManager):
    INSTANCE_NAME = "Post"

    def create(
            self,
            create_data: CreateSchemaType | dict[str, Any],
            *args,
            **kwargs
    ) -> Post:
        user_id = kwargs.get("user_id")
        create_data = jsonable_encoder(create_data)
        create_data["user_id"] = user_id
        new_post = super().create(create_data)
        return new_post

    def update(
            self,
            post_to_update: Post,
            update_data: UpdateSchemaType | dict[str, Any],
            *args,
            **kwargs
    ) -> Post:
        user_id = kwargs.get("user_id")
        update_data = jsonable_encoder(update_data)
        update_data["user_id"] = user_id
        updated_post = super().update(post_to_update, update_data)
        return updated_post


post_manager = PostManager(Post)
