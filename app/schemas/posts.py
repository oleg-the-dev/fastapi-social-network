from pydantic import BaseModel


class PostDB(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    likes: int
    dislikes: int

    class Config:
        orm_mode = True


class PostCreateUpdate(BaseModel):
    title: str
    content: str
