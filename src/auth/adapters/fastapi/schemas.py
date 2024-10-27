from pydantic import BaseModel


class UserCreationSchema(BaseModel):
    email: str
    password: str


class UserSchema(BaseModel):
    email: str
    is_active: bool


class ActivationCodeSchema(BaseModel):
    code: str
