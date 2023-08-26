from typing import Optional
# from project.routers import login_routes as login, ai_routes as ai

from fastapi import FastAPI

app = FastAPI()


# app.include_router(login.router)
# app.include_router(ai.router)


@app.get("/")
async def root(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {"data": f"{limit} blogs from the db"}


@app.get("/blog/unpublished")
async def unpublished():
    return {"data": "all unpublished blogs"}


# Show blog
@app.get('/blog/{blogId}')
async def show(blogId: int):
    return {"data": f"blog with id {blogId}"}


@app.get('/blog/{blogId}/comments')
async def comments(blogId: int):
    return {"data": {"1", "2"}}
