from typing import Optional

from pydantic import BaseModel
from src.schemas.validators.email_validator import EmailValidatorSchema
from src.schemas.validators.name_validator import NameValidatorSchema
from src.schemas.validators.password_validator import PasswordValidatorSchema
from src.util.user_roles import UserRoles


class UserBaseSchema(BaseModel):
    id: Optional[int]
    name: NameValidatorSchema
    email: EmailValidatorSchema

    class Config:
        orm_mode = True


class UserSchema(UserBaseSchema):
    role: UserRoles


class UserRegisterSchema(UserSchema):
    password: PasswordValidatorSchema
