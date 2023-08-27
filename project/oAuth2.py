from typing import Annotated

from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from project.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)