from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/api/v1",
    tags=["login"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/login")
async def read_root():
    return {"Hello": "World"}
