from typing import Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from project import models
from project.Requests.Authentication import AuthenticationResponse
from project.Requests.Blog import BlogResponse, BlogRequest
from project.databse import get_db
from project.oAuth2 import get_current_user

router = APIRouter(
    prefix="/api/v1/blogs",
    tags=["Blogs"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[BlogResponse])
async def root(limit: int = 10, published: bool = True, sort: Optional[str] = 'ASC', db: Session = Depends(get_db), current_user: Annotated[AuthenticationResponse, Depends(get_current_user)] = None):
    blogs = db.query(models.Blog)
    if published:
        blogs = blogs.filter(models.Blog.published == published)
    if sort:
        blogs = blogs.order_by(models.Blog.id.desc() if sort == 'DESC' else models.Blog.id.asc())

    blogs = blogs.limit(limit).all()
    return blogs


@router.get("/unpublished", status_code=status.HTTP_200_OK, response_model=list[BlogResponse])
async def unpublished(db: Session = Depends(get_db), current_user: Annotated[AuthenticationResponse, Depends(get_current_user)] = None):
    blogs = db.query(models.Blog).filter(models.Blog.published == False)
    return blogs.all()


# Show blog
@router.get('/{blogId}', status_code=status.HTTP_200_OK, response_model=BlogResponse)
async def show(blogId: int, db: Session = Depends(get_db), current_user: Annotated[AuthenticationResponse, Depends(get_current_user)] = None):
    blog = db.query(models.Blog).filter(models.Blog.id == blogId).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blogId} not found")
    return blog


@router.post('', status_code=status.HTTP_201_CREATED, response_model=BlogResponse)
async def create(request: BlogRequest, db: Session = Depends(get_db), current_user: Annotated[AuthenticationResponse, Depends(get_current_user)] = None):
    new_blog = models.Blog(title=request.title, body=request.body, published=request.published, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put('/{blogId}', status_code=status.HTTP_202_ACCEPTED)
async def update(blogId: int, request: BlogRequest, db: Session = Depends(get_db), current_user: Annotated[AuthenticationResponse, Depends(get_current_user)] = None):
    blog = db.query(models.Blog).filter(models.Blog.id == blogId)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blogId} not found")
    blog.update(request.model_dump())
    db.commit()
    return {"data": "updated"}


@router.delete('/{blogId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(blogId: int, db: Session = Depends(get_db), current_user: Annotated[AuthenticationResponse, Depends(get_current_user)] = None):
    blog = db.query(models.Blog).filter(models.Blog.id == blogId)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blogId} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"data": "deleted"}
