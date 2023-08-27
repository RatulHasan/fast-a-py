from typing import Union

from pydantic import BaseModel


class AuthenticationRequest(BaseModel):
    email: str
    password: str


class AuthenticationResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
