from pydantic import BaseModel


class Post(BaseModel):
    Title: str
    Body: str
