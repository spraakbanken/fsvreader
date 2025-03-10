import pytest


@pytest.mark.asyncio
async def test_can_access_index(client):
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_can_access_favicon(client):
    response = await client.get("/static/favicon.ico")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_can_access_reader_css(client):
    response = await client.get("/static/reader.css")
    assert response.status_code == 200


@pytest.mark.skip(reason="not supported yet")
@pytest.mark.asyncio
async def test_can_access_reader(client):
    response = await client.get("/reader")
    assert response.status_code == 200


@pytest.mark.parametrize("words", ["", "hund--hime"])
@pytest.mark.asyncio
async def test_can_access_lexseasy(client, words: str):
    response = await client.get(f"/lexseasy/{words}")
    assert response.status_code == 200


@pytest.mark.parametrize("dirname", ["aldre_lagar", "aldre_profan", "aldre_religios"])
@pytest.mark.asyncio
async def test_can_access_dir(client, dirname: str):
    response = await client.get(f"/dir/{dirname}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "path",
    [
        "aldre_lagar/AVgL.html",
        "aldre_lagar/BjR.html",
        "aldre_lagar/DL.html",
        "aldre_lagar/GL.html",
        "aldre_lagar/HL.html",
        "aldre_lagar/MEL.html",
        "aldre_lagar/MESt.html",
        "aldre_lagar/OgL.html",
        "aldre_lagar/SdmL-A.html",
        "aldre_lagar/SdmL.html",
        "aldre_lagar/SkL.html",
        "aldre_lagar/SmL_Kb.html",
        "aldre_lagar/UL.html",
        "aldre_lagar/VmL.html",
        "aldre_lagar/YVgL.html",
        "aldre_profan/Ks.html",
        "aldre_religios/Birgitta_aut-B.html",
        "aldre_religios/Legendarium-B.html",
        "aldre_religios/Moses-B.html",
    ],
)
@pytest.mark.asyncio
async def test_can_access_reader_files(client, path: str):
    response = await client.get(f"/reader/{path}")
    assert response.status_code == 200
