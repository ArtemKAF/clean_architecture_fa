from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["root"])
def index():
    return {"ping": "OK"}
