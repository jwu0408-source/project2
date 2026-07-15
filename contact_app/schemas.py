from pydantic import BaseModel, ConfigDict, Field, field_validator
import re


class SignupIn(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=4, max_length=20)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.fullmatch(r"[a-z0-9]+", value):
            raise ValueError("username must contain only lowercase letters and numbers")
        return value


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=20)


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# This assignment does not include a memo field.
# The contact payloads intentionally omit memo and reserve that as a future extension.
class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=5)
    phone: str = Field(pattern=r"^010\d{8}$")
    addr: str = Field(min_length=1, max_length=100)
    category_id: int | None = None


class ContactUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=5)
    phone: str | None = Field(default=None, pattern=r"^010\d{8}$")
    addr: str | None = Field(default=None, min_length=1, max_length=100)
    category_id: int | None = None


class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    addr: str
    category_id: int | None
