from pydantic import BaseModel


class BaseUser(BaseModel):
    fname: str
    lname: str
    email: str


class BaseML(BaseModel):
    user_id: int
    title: str
    description: str
    pass


class CreateML(BaseML):
    created_at: str
    pass


class ShowML(BaseML):
    id: int

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    created_at: str
    password: str


class CreateUserAsAdmin(CreateUser):
    is_admin: bool


class UpdateUser(BaseUser):
    updated_at: str
    pass


class ShowUser(BaseUser):
    created_at: str
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
