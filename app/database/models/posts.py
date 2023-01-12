from sqlalchemy import (
    Column, Integer, String, ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.ext.hybrid import hybrid_property

from database.db import Base, db_session

metadata = Base.metadata


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    @hybrid_property
    def likes(self):
        with db_session() as db:
            count = db.query(PostLike).filter_by(post_id=self.id).count()
        return count

    @hybrid_property
    def dislikes(self):
        with db_session() as db:
            count = db.query(PostDislike).filter_by(post_id=self.id).count()
        return count


class PostLike(Base):
    __tablename__ = "post_like"
    __table_args__ = (
        PrimaryKeyConstraint(
            "post_id",
            "user_id"
        ),
    )

    post_id = Column(ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


class PostDislike(Base):
    __tablename__ = "post_dislike"
    __table_args__ = (
        PrimaryKeyConstraint(
            "post_id",
            "user_id"
        ),
    )

    post_id = Column(ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
