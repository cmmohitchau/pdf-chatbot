
import uuid
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import EmailStr
from pydantic import BaseModel

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True , index=True, max_length=255)
    name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)

class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None , unique=True , index=True, max_length=255)
    name: str | None = Field(default=None, max_length=255)

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str | None = Field(default=None)

