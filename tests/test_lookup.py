from fsvreader.routes.lookup import _clean_source


def test_clean_source(snapshot) -> None:
    source = " &c., H."

    actual = _clean_source(source)

    assert actual == snapshot
