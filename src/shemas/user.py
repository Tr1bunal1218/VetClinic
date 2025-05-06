from pydantic import BaseModel,  EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    role: str
    hashed_password: str


class User(BaseModel):
    id: int
    role:str
    email: EmailStr
    
class UserHashedPass(User):
    hashed_password: str