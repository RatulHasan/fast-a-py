from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from project import models
from project.Hash import Hash
from project.Requests.Authentication import AuthenticationRequest, AuthenticationResponse
from project.databse import get_db
from project.token import create_access_token

router = APIRouter(
    prefix="/api/v1/login",
    tags=["Login"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_200_OK, response_model=AuthenticationResponse)
async def login(request: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {request.username} not found")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
