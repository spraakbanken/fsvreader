from typing import Any

import jinja2
from fastapi import Request
from fastapi.datastructures import URL
from fastapi.templating import Jinja2Templates

from fsvreader.config import AppSettings


def init_template_engine(settings: AppSettings) -> Jinja2Templates:
    templates = Jinja2Templates(directory=settings.template_directory)
    templates.env.globals["url_for"] = custom_url_for
    return templates


@jinja2.pass_context
def custom_url_for(context: dict[str, Any], name: str, **path_params) -> URL:
    request: Request = context["request"]
    # if name == "korpus_ref" and "lids" in path_params:
    #     return URL(
    #         f"{request.app.state.settings.korp_url}/#?search=lemgram|{path_params['lids'][0]}"
    #     )
    if base_url := request.app.state.settings.app.base_url:
        return request.app.url_path_for(name, **path_params).make_absolute_url(base_url)

    return request.url_for(name, **path_params)
