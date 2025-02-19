from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from fsvreader.config import Settings
from fsvreader.server import create_server


@pytest.fixture(name="webapp")
def fixture_webapp() -> FastAPI:
    webapp = create_server(
        settings=Settings()
        # settings=SaldoWsSettings(
        #     semantic_path="assets/testing/saldo.txt",
        #     fm_server_url="not-used",
        #     fm_bin=FmBinSettings(path="not used"),
        #     tracking=MatomoSettings(matomo_url=None),
        #     otel=OTelSettings(
        #         otel_service_name="saldo-ws",
        #         debug_log_otel_to_console=False,
        #         debug_log_otel_to_provider=False,
        #     ),
        #     app=AppSettings(template_directory="templates/saldo_ws"),
        # )
        # config={
        #     "semantic.path": "assets/testing/saldo.txt",
        #     "morphology.path": "assets/testing/saldo.lex",
        # },
        # env=env,
    )
    return webapp


@pytest_asyncio.fixture()
async def client(webapp: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(webapp):
        async with AsyncClient(
            transport=ASGITransport(webapp),  # type: ignore [arg-type]
            base_url="http://testserver.saldo_ws",
        ) as client:
            yield client
