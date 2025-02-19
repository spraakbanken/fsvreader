from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from fsvreader.errors import UnknownDirError, UnknownFileError
from fsvreader.metadata import METADATA

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
    if textdir not in METADATA:
        raise UnknownDirError(dir=textdir)
    if textfile not in METADATA[textdir]["texts"]:
        raise UnknownFileError(dir=textdir, file=textfile)
    templates = request.app.state.templates
    title = f"{METADATA[textdir]['texts'][textfile]['title']} | {METADATA[textdir]['title']}"
    return templates.TemplateResponse(
        request=request,
        name=f"{textdir}_{textfile}",
        context={"title": title, "back": textdir},
    )
