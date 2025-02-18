import logging
import re
import xml.etree.ElementTree as etree
from typing import Annotated, Any, Union

from asgi_correlation_id import correlation_id
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from karp_api_client import Client, dsl
from karp_api_client.api import querying
from pydantic import BaseModel
from returns.result import Failure, Success

from fsvreader import deps

router = APIRouter()

_logger = logging.getLogger(__name__)


class Message(BaseModel):
    message: str


class ErrorMessage(BaseModel):
    error: str
    called: str
    words: str
    hits: list[dict[str, Any]]


@router.get(
    "/lexseasy/{words}",
    response_class=HTMLResponse,
    responses={400: {"model": ErrorMessage}, 501: {"model": Message}},
    name="lookup",
)
async def lookup(
    request: Request,
    words: str,
    karp_client: Annotated[Client, Depends(deps.get_karp_client)],
):
    wordlist = words.split("--")
    # sometimes, the headword is repetead as the first alternative
    # only look for it once
    if len(wordlist) > 1 and wordlist[0] == wordlist[1]:
        wordlist = wordlist[1:]

    # if the first entry is a number, set it apart
    numberword = wordlist[0] if wordlist and wordlist[0].isdigit() else ""

    wordlist = [word.replace("_", " ") for word in wordlist]
    karp_q = dsl.Or()
    for word in wordlist:
        karp_q = karp_q | dsl.Equals(field="baseform", value=word)

    res = await querying.query_async(
        "schlyter,soederwall,soederwall-supp",
        query_options=querying.QueryOptions(q=karp_q, size=25),
        client=karp_client,
    )
    match res:
        case Success(resp):
            worddata = process_response(resp.parsed, wordlist=wordlist)
        case Failure(err):
            return JSONResponse(
                status_code=400,
                headers={
                    "X-Request-ID": correlation_id.get() or "",
                    "Access-Control-Expose-Headers": "X-Request-ID",
                },
                content={
                    "error": f"{err}",
                    "called": str(karp_q),
                    "words": words,
                    "hits": [],
                },
            )

    # add in the numberword with a dummy entry
    if numberword:
        worddata[numberword] = [
            (
                "DEADDEADDEAD",
                {
                    "lexiconName": "Romerska-siffror",
                    "pre": "",
                    "txt": "",
                    "pos": "nl",
                },
            )
        ]
    # only list the forms that actually found a hit
    wordlist = [(word, word.replace(" ", "_")) for word in wordlist if word in worddata]
    templates = request.app.state.templates
    print(f"{request.headers=}")
    _logger.info("words=%s", words)
    _logger.info("worddata=%s", worddata)
    _logger.info("wordlist=%s", wordlist)
    return templates.TemplateResponse(
        request=request,
        name="lex.html",
        context={
            "hword": wordlist[0][0],
            "words": wordlist,
            "data": worddata,
            "hitlist": "/".join(w[0] for w in wordlist),
            "hits": sum(len(v) for v in worddata.values()),
        },
    )


@router.get(
    "/lexseasy/",
    response_class=HTMLResponse,
    responses={400: {"model": ErrorMessage}, 501: {"model": Message}},
    name="lookup-empty",
)
async def lookup_empty(
    request: Request,
    karp_client: Annotated[Client, Depends(deps.get_karp_client)],
):
    wordlist = []
    worddata = {}

    templates = request.app.state.templates

    return templates.TemplateResponse(
        request=request,
        name="lex.html",
        context={
            "hword": "",
            "words": wordlist,
            "data": worddata,
            "hitlist": "/".join(w[0] for w in wordlist),
            "hits": sum(len(v) for v in worddata.values()),
        },
    )


def process_response(
    response: querying.QueryResponse | None, *, wordlist: list[str]
) -> dict[str, Any]:
    worddata: dict[str, Any] = {}
    if response is None:
        return worddata
    for hit_raw in response.hits:
        _logger.info("hit_raw=%s", hit_raw)
        hit = hit_raw.entry
        hit["lexiconName"] = hit_raw.resource.replace("oe", "\xf6").replace("-", " ")
        id_ = hit_raw.id
        base: str = hit["baseform"]
        wfs = [
            wf.get("writtenForm", "")
            for wf in hit.get("inflectionTable", [{}])
            if wf.get("tag") == "derived"
        ]
        _logger.info("hit['xml']='%s'", hit["xml"])
        text = _parse_xml(hit["xml"])
        # text = " ".join(etree.fromstring(hit["xml"].encode("utf-8")).itertext())
        if re.search(r"^%s[ ,.;]*[sS]e\s\S*[,.:]*$" % base, text):
            continue
        if len(text) > 40:
            hit["pre"] = text[:30]
        hit["text"] = text
        pos: Union[str, list[str]] = hit.get("partOfSpeech", "")
        if isinstance(pos, list):
            pos = ", ".join(pos)
        hit["pos"] = pos
        # if the base form is a requested lemma (=in wordlist), add the
        # entry under its base form and don't bother about other word forms
        if base.replace("_", " ") in wordlist:
            worddata.setdefault(base, []).append((id_, hit))
        # if not, go through them to find the interesting once
        for wf in wfs:
            wf = wf.strip("*?")
            if wf in wordlist:
                worddata.setdefault(wf, []).append((id_, hit))
    return worddata


def _parse_xml(xml_source: str) -> str:
    return " ".join(etree.fromstring(_clean_source(xml_source)).itertext())


AMP_PATTERN = re.compile(r"&(c|e)")


def _clean_source(source: str) -> str:
    return AMP_PATTERN.sub(r"&amp;\1", source)


# r = {
#     "id": "01J9RWB6DM7STANZMRV3NQWAAN",
#     "version": 1,
#     "last_modified": 1728485628.340536,
#     "last_modified_by": "local admin",
#     "resource": "schlyter",
#     "entry": {
#         "baseform": "til agha",
#         "lemgram": "fsvm--til_agha..nn.1",
#         "partOfSpeech": "nn",
#         "senses": [
#             {
#                 "definition": {"text": ["se Tillagha."]},
#                 "senseid": "schlyter--til_agha..1",
#             }
#         ],
#         "xml": '<entry subtype="main" xml:id="fsvm--til_agha..nn.1"><form><orth type="hw">Til agha</orth></form>, se Tillagha.</entry>',
#     },
# }
