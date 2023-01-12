from pydantic import BaseModel, EmailStr


class UserDB(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class UserCreateUpdate(BaseModel):
    email: EmailStr
    password: str
