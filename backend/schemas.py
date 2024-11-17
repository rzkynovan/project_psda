from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin:bool

class UserLogin(BaseModel):
    username: str
    password: str