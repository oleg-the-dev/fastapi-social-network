from typing import Any, Generic, TypeVar

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from database.db import Base, db_session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseManager(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    INSTANCE_NAME = "Instance"

    def __init__(self, model: ModelType):
        self.model = model

    def get(
            self,
            filters: dict[str, Any]
    ) -> ModelType | None:
        """
        Get instance from database
        :param filters: dict of filters for WHERE statement
        :return: database instance of ModelType or None
        """
        with db_session() as db:
            instance = db.query(self.model).filter_by(**filters).first()
        return instance

    def get_or_404(
            self,
            filters: dict[str, Any]
    ) -> ModelType:
        """
        Get instance from database or raise 404 HTTP error
        :param filters: dict of filters for WHERE statement
        :return: database instance of ModelType
        :raises: 404 HTTPException if no instance was found
        """
        instance = self.get(filters)
        if not instance:
            raise HTTPException(
                detail=f"{self.INSTANCE_NAME} with parameters {filters} not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return instance

    def get_all(self) -> list[ModelType]:
        """
        Get all instances from database
        :return: list of database instance of ModelType
        """
        with db_session() as db:
            instances = db.query(self.model).all()
        return instances

    def create(
            self,
            create_data: CreateSchemaType | dict[str, Any],
            *args,
            **kwargs
    ) -> ModelType:
        """
        Create new instance in database
        :param create_data: pydantic schema or python dict
        :return: created instance of ModelType
        """
        if not isinstance(create_data, dict):
            create_data = jsonable_encoder(create_data)
        instance_to_create = self.model(**create_data)
        with db_session() as db:
            db.add(instance_to_create)
            db.commit()
            db.refresh(instance_to_create)
        return instance_to_create

    def update(
            self,
            instance_to_update: ModelType,
            update_data: UpdateSchemaType | dict[str, Any],
            *args,
            **kwargs
    ) -> ModelType:
        """
        Update instance from database
        :param instance_to_update: instance of ModelType that will be updated
        :param update_data: pydantic schema or python dict
        :param args:
        :param kwargs:
        :return: updated instance of ModelType
        """
        if not isinstance(update_data, dict):
            update_data = update_data.dict(exclude_unset=True)
        instance_data = jsonable_encoder(instance_to_update)
        for field in instance_data:
            if field in update_data:
                # Check if data field is not None for partial update
                if update_data[field] is not None:
                    setattr(instance_to_update, field, update_data[field])
        with db_session() as db:
            db.merge(instance_to_update)
            db.commit()
        return instance_to_update

    def delete(self, instance_to_delete: ModelType) -> None:
        """
        Delete instance from database
        :param instance_to_delete: instance that will be deleted
        :return: None
        """
        with db_session() as db:
            db.delete(instance_to_delete)
            db.commit()
