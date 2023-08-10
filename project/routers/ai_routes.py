from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/api/v1",
    tags=["ai"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/sync-data")
async def read_root():
    return {"Hello": "World"}
