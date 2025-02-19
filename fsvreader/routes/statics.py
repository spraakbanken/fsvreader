from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/static/{path:path}", name="static")
async def staticfiles_workaround(path: str) -> FileResponse:
    return FileResponse(f"static/{path}")
