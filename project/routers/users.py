from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from project import models
from project.Hash import Hash
from project.Requests.User import UserRequest, UserResponse
from project.databse import get_db

router = APIRouter(
    prefix="/api/v1",
    tags=["Users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get('/users', status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(request: UserRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {request.email} already exists")

    new_user = models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{userId}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(userId: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == userId).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {userId} not found")
    return user
