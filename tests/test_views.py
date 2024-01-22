import pytest


def test_can_access_index(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("path", ["/any"])
def test_can_access_favicon(client, path: str):
    response = client.get(f"/reader{path}/favicon.ico")
    assert response.status_code == 200


@pytest.mark.parametrize("path", ["/any"])
def test_can_access_reader_js(client, path: str):
    response = client.get(f"/reader{path}/reader.js")
    assert response.status_code == 200


@pytest.mark.parametrize("path", ["/any"])
def test_can_access_reader_css(client, path: str):
    response = client.get(f"/reader{path}/reader.css")
    assert response.status_code == 200


def test_can_access_fsvreader_html(client):
    response = client.get("/fsvreader.html")
    assert response.status_code == 200


def test_can_access_fsvlex_html(client):
    response = client.get("/fsvlex.html")
    assert response.status_code == 200


def test_can_access_reader(client):
    response = client.get("/reader")
    assert response.status_code == 200


@pytest.mark.parametrize("words", ["", "hund--hime"])
def test_can_access_lexseasy(client, words: str):
    response = client.get(f"/lexseasy/{words}")
    assert response.status_code == 200


@pytest.mark.parametrize("dirname", ["aldre_lagar", "aldre_profan", "aldre_religios"])
def test_can_access_dir(client, dirname: str):
    response = client.get(f"/dir/{dirname}")
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
def test_can_access_file(client, path: str):
    response = client.get(f"/file/{path}")
    assert response.status_code == 200
