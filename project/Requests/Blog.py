from typing import Optional
from pydantic import BaseModel

from project.Requests.User import UserResponse


class BlogRequest(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class BlogResponse(BlogRequest):
    id: int
    creator: UserResponse

    class Config:
        orm_mode = True
