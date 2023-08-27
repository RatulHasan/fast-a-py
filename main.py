from fastapi import FastAPI
from project import models
from project.databse import engine
from project.routers import users, blogs, login

models.Base.metadata.create_all(engine)
tags_metadata = [
    {
        "name": "Login",
        "description": "Login related endpoints",
    },
    {
        "name": "Blogs",
        "description": "Blog related endpoints",
    },
    {
        "name": "Users",
        "description": "User related endpoints",
    },
]

app = FastAPI(redoc_url=None, openapi_tags=tags_metadata)
app.include_router(login.router)
app.include_router(users.router)
app.include_router(blogs.router)
