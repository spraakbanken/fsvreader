from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

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
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request, name="aldre_lagar.html", context={"title": "Äldre lagar"}
    )
