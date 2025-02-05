import traceback
from contextlib import asynccontextmanager
from logging.config import dictConfig

import asgi_correlation_id
import karp_api_client
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.staticfiles import StaticFiles

from fsvreader import routes, templating
from fsvreader.config import Settings


def create_server(*, settings: Settings) -> FastAPI:
    configure_logging()
    webapp = FastAPI(
        title="FSvReader",
        lifespan=lifespan,
    )

    webapp.state.settings = settings
    webapp.state._karp_client = karp_api_client.Client()
    webapp.state.templates = templating.init_template_engine(settings.app)
    webapp.include_router(routes.router)
    webapp.mount("/static", StaticFiles(directory="static"), name="static")

    _configure_exception_handlers(webapp)
    webapp.add_middleware(CorrelationIdMiddleware)

    return webapp


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": asgi_correlation_id.CorrelationIdFilter,
                    "uuid_length": 32,
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "format": "%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                "fsvreader": {
                    "level": "INFO",
                    "propagate": True,
                    "handlers": ["console"],
                },
                # third-party package loggers
                "sqlalchemy": {"level": "WARNING", "handlers": ["console"]},
                "uvicorn": {"level": "INFO", "handlers": ["console"]},
                # "elasticsearch": {"level": "DEBUG", "handlers": ["console"]},
            },
        }
    )


def _configure_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def _unhandled_exception_handler(request: Request, exc: Exception):
        def extract_exceptions(excs):
            output = []
            for inner_exc in excs:
                if hasattr(inner_exc, "exceptions"):
                    output.extend(extract_exceptions(inner_exc.exceptions))
                else:
                    output.append(inner_exc)
            return output

        for out_exc in extract_exceptions([exc]):
            traceback.print_exception(out_exc)
        return await http_exception_handler(
            request,
            HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
                headers={
                    "X-Request-ID": correlation_id.get() or "",
                    "Access-Control-Expose-Headers": "X-Request-ID",
                },
            ),
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with app.state._karp_client:
        yield
