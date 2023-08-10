from project.routers import login_routes as login, ai_routes as ai

from fastapi import FastAPI

app = FastAPI()

app.include_router(login.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
