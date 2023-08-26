from typing import Optional
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from project import models
from project.Hash import Hash
from project.Requests.Blog import BlogRequest, BlogResponse
from project.Requests.User import UserRequest, UserResponse
from project.databse import engine, SessionLocal

models.Base.metadata.create_all(engine)
tags_metadata = [
    {
        "name": "blog",
        "description": "Blog related endpoints",
    },
    {
        "name": "user",
        "description": "User related endpoints",
    },
]
app = FastAPI(redoc_url=None, openapi_tags=tags_metadata)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=status.HTTP_200_OK, response_model=list[BlogResponse], tags=["blog"])
async def root(limit: int = 10, published: bool = True, sort: Optional[str] = 'ASC', db: Session = Depends(get_db)):
    blogs = db.query(models.Blog)
    if published:
        blogs = blogs.filter(models.Blog.published == published)
    if sort:
        blogs = blogs.order_by(models.Blog.id.desc() if sort == 'DESC' else models.Blog.id.asc())

    blogs = blogs.limit(limit).all()
    return blogs


@app.get("/blog/unpublished", status_code=status.HTTP_200_OK, response_model=list[BlogResponse], tags=["blog"])
async def unpublished(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.published == False)
    return blogs.all()


# Show blog
@app.get('/blog/{blogId}', status_code=status.HTTP_200_OK, response_model=BlogResponse, tags=["blog"])
async def show(blogId: int, response: Response = status.HTTP_200_OK, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blogId).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blogId} not found")
    return blog


@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=BlogResponse, tags=["blog"])
async def create(request: BlogRequest, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, published=request.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put('/blog/{blogId}', status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
async def update(blogId: int, request: BlogRequest, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blogId)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blogId} not found")
    blog.update(request.model_dump())
    db.commit()
    return {"data": "updated"}


@app.delete('/blog/{blogId}', status_code=status.HTTP_204_NO_CONTENT, tags=["blog"])
async def delete(blogId: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blogId)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blogId} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"data": "deleted"}


@app.get('/user', status_code=status.HTTP_200_OK, response_model=list[UserResponse], tags=["user"])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["user"])
async def create_user(request: UserRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {request.email} already exists")

    new_user = models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{userId}', status_code=status.HTTP_200_OK, response_model=UserResponse, tags=["user"])
async def get_user(userId: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == userId).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {userId} not found")
    return user