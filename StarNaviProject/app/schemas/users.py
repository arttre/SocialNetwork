from pydantic import BaseModel, EmailStr


class UserFullInfo(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
