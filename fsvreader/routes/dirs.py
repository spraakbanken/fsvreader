from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from fsvreader.errors import UnknownDirError
from fsvreader.metadata import METADATA

router = APIRouter()


@router.get("/", response_class=HTMLResponse, name="home")
async def index(
    request: Request,
) -> HTMLResponse:
    templates = request.app.state.templates
    return templates.TemplateResponse(request=request, name="firstpage.html")


@router.get("/dir/{dirname}", response_class=HTMLResponse, name="showdir")
async def showdir(
    request: Request,
    dirname: str,
) -> HTMLResponse:
    if dirname not in METADATA:
        raise UnknownDirError(dir=dirname)
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name=f"{dirname}.html",
        context={"title": METADATA[dirname]["title"]},
    )
