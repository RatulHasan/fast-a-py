from typing import Optional
from pydantic import BaseModel


class BlogRequest(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class BlogResponse(BlogRequest):
    id: int

    class Config:
        orm_mode = True
