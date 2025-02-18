import html
from pathlib import Path
from typing import Any, TextIO

from lxml import etree

from fsvreader.metadata import METADATA

PAGE_PATH: str = "fsvreader/pages"
DST_PATH: str = "templates"
DIRS_PATH: Path = Path("fsvreader/pages/lists/dirs.txt")


def main() -> None:
    files: list[tuple[str, str]] = []
    for dir, texts in METADATA.items():
        print(f"{dir=}, {texts=}")
        for file in texts["texts"]:
            files.append((dir, file))
    convert_pages(files)


def read_dirs() -> dict[str, str]:
    dirs: dict[str, str] = {}
    with DIRS_PATH.open() as dirs_file:
        for dir in dirs_file:
            path, descr = dir.split("\t")
            dirs[path] = descr
    return dirs


SPACE: str = " " * 4


def convert_overviews(dirs: dict[str, str]) -> list[tuple[str, str]]:
    files: list[tuple[str, str]] = []
    for dir_name, dir_descr in dirs.items():
        contentfile = Path(f"{PAGE_PATH}/{dir_name}/content.txt")
        dst_path = Path(f"{DST_PATH}/{dir_name}.html")
        with contentfile.open() as contents:
            with dst_path.open("w") as dst:
                dst.write('{% extends "layout.html" %} {% block content %}\n')
                dst.write("<div>\n")
                dst.write(f"{SPACE}<h1>{dir_descr}</h1>\n")
                dst.write(f"{SPACE}<h4>Texter</h4>\n")
                dst.write(f"{SPACE}<ul>\n")
                for content in contents:
                    filename, description, period = content.split("|")
                    files.append((dir_name, filename.split(".")[0]))
                    filename = filename.strip()
                    description = description.strip(' "')
                    period = period.strip(' "')
                    dst.write(f"{SPACE * 2}<li>\n")
                    dst.write(
                        f"{SPACE * 3}<a href=\"{{{{ url_for('reader', textdir='{dir_name}', textfile='{filename}') }}}}\"> {description}</a>\n"
                    )
                    dst.write(f"{SPACE * 3}{period}\n")
                    dst.write(f"{SPACE * 2}</li>\n")
                dst.write(f"{SPACE}</ul>\n")
                dst.write("</div>\n")
                dst.write("{% endblock %}\n")

    return files


def convert_pages(files: list[tuple[str, str]]) -> None:
    parser = etree.HTMLParser(encoding="utf-8")
    for dir, name in files:
        filename = Path(f"{PAGE_PATH}/{dir}/{name}")
        dst_path = Path(f"{DST_PATH}/{dir}_{name}")

        if not filename.exists():
            continue
        with dst_path.open(mode="w") as dst:
            dst.write('{% extends "reader_layout.html" %} {% block content %}\n')
            dst.write("\n")

            tree = etree.parse(filename, parser)

            root = tree.getroot()
            _print_xml(dst, root)

            dst.write("\n{% endblock %}\n")


def _clean_xml_code(src: str) -> str:
    src = src.replace('hx-target="#main&gt;#lexframe"', 'hx-target="#main>#lexframe"')
    return src


def _make_link(src: str) -> str:
    lst = src.split()
    unesc = [html.unescape(w) for w in lst]
    return "--".join(unesc)


def _print_xml(dst: TextIO, elem) -> None:
    attributes = elem.attrib
    if elem.tag == "a":
        _enrich_attribs(attributes)
    elem_attribs = _print_attribs(attributes)
    if elem_attribs:
        dst.write(f"<{elem.tag} {elem_attribs}>")
    else:
        dst.write(f"<{elem.tag}>")
    if elem.text is not None:
        dst.write(f"{elem.text}")

    for subelem in elem:
        _print_xml(dst, subelem)
    dst.write(f"</{elem.tag}>")
    if elem.tail is not None:
        dst.write(f"{elem.tail}")


def _print_attribs(d: dict[str, Any]) -> str:
    return " ".join(f'{k}="{v}"' for k, v in d.items())


def _enrich_attribs(attributes: dict[str, Any]) -> None:
    words = _make_link(attributes["class"])
    # class_words = attributes["class"]
    # words = "--".join((html.unescape(w) for w in class_words.split()))
    attributes["hx-target"] = "#main>#lexframe"
    attributes["hx-get"] = f"{{{{ url_for('lookup', words='{words}') }}}}"
    attributes["hx-swap"] = "innerHtml"


if __name__ == "__main__":
    main()
