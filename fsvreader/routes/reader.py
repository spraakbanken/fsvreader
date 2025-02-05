from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get(
    "/reader/{textdir}/{textfile}",
    response_class=HTMLResponse,
    name="reader",
)
async def readerfile(
    request: Request,
    textdir: str,
    textfile: str,
) -> HTMLResponse:
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request=request,
        name=f"{textdir}_{textfile}",
        context={"title": "Äldre lagar"},
    )
