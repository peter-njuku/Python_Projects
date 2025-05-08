from pydantic import BaseModel,EmailStr
from datetime import datetime

class TaskUpdate(BaseModel):
    name: str | None=None
    completed: bool | None=None

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    is_active:bool=True

class UserResponse(BaseModel):
    id:int
    email:str
    is_active:bool

    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None=None
