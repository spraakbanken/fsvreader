import codecs
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as etree
from urllib.request import Request, urlopen

from flask import Flask, jsonify, render_template, send_file


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        # The path from your web server to this directory.
        # If you run the application directly with python, use ""
        APPLICATION_ROOT="",
        # The absolute path to this directory. Extra slash for urljoin
        APPLICATION_PATH=f"{os.path.dirname(__file__)}/",
        KARP="https://ws.spraakbanken.gu.se/ws/karp/v4/",
    )
    if config is None:
        app.config.from_prefixed_env("FSVREADER")
    else:
        app.config.from_mapping(config)

    @app.route("/reader/favicon.ico")
    def _favicon_base():
        return send_static_file("favicon.ico")

    @app.route("/reader/<dummy>/favicon.ico")
    def favicon(dummy):
        return send_static_file("favicon.ico")

    @app.route("/reader.js")
    def reader_js():
        return send_static_file("reader.js")

    @app.route("/reader/<dummy>/<filename>.css")
    def static_css(dummy, filename):
        return send_static_file(f"{filename}.css")

    @app.route("/reader/<filename>.css")
    def static_css_base(filename):
        return send_static_file(f"{filename}.css")

    @app.route("/fsvreader.html")
    def text():
        return serve_static_page("fsvreader")

    @app.route("/reader")
    def reader():
        return render_template(
            "reader.html",
            textframe="fsvreader.html",
            lexframe="fsvreader/lexseasy/hund--hime",
            lexurl=app.config["APPLICATION_ROOT"] + "/fsvreader/lexseasy/",
        )

    @app.route("/reader/<textdir>/<textfile>")
    def readerfile(textdir, textfile):
        texturl = f"/fsvreader/file/{textdir}/{textfile}"
        # texturl = url_for('file/%s/%s' % (textdir, textfile))
        return render_template(
            "reader.html",
            textframe=texturl,
            lexframe=app.config["APPLICATION_ROOT"] + "/fsvreader/lexseasy/",
            lexurl=app.config["APPLICATION_ROOT"] + "/fsvreader/lexseasy/",
        )

    @app.route("/fsvlex.html")
    def lex():
        return serve_static_page("fsvlex")

    @app.route("/lexseasy/")
    def emptylookup():
        return ""

    @app.route("/lexseasy/<words>")
    def lookup(words):
        karp_q = ""
        worddata = {}
        try:
            worddata = {}
            wordlist = words.split("--")

            # sometimes, the headword is repetead as the first alternative
            # only look for it once
            if len(wordlist) > 1 and wordlist[0] == wordlist[1]:
                wordlist = wordlist[1:]

            # if the first entry is a number, set it apart
            numberword = wordlist[0] if wordlist and wordlist[0].isdigit() else ""

            wordlist = [word.replace("_", " ") for word in wordlist]
            karp_q = {"q": f'extended||and|wfC|equals|{"|".join(wordlist)}'}
            res = karp_query("query", karp_q)
        except Exception:
            return jsonify(
                {
                    "call": karp_q,
                    "words": words,
                    "splitted": "|".join(words.split("--")),
                }
            )

        try:
            for hit in res.get("hits", {}).get("hits", []):
                _id = hit["_id"]
                base = (
                    hit["_source"].get("FormRepresentations", [{}])[0].get("baseform")
                )
                wfs = [
                    wf.get("writtenForm", "")
                    for wf in hit["_source"].get("WordForms", [{}])
                    if wf.get("tag", "") == "derived"
                ]
                # xml = hit['_source'].get('xml', '')
                text = " ".join(
                    etree.fromstring(
                        hit["_source"].get("xml").encode("utf-8")
                    ).itertext()
                )
                if re.search("^%s[ ,.;]*[sS]e\s\S*[,.:]*$" % base, text):
                    continue
                if len(text) > 40:
                    hit["_source"]["pre"] = text[:30]
                hit["_source"]["text"] = text
                pos = (
                    hit["_source"]
                    .get("FormRepresentations", [{}])[0]
                    .get("partOfSpeech", "")
                )
                if isinstance(pos, list):
                    pos = ", ".join(pos)
                hit["_source"]["pos"] = pos

                # if the base form is a requested lemma (=in wordlist), add the
                # entry under its base form and don't bother about other word forms
                if base.replace("_", " ") in wordlist:
                    worddata.setdefault(base, []).append((_id, hit["_source"]))

                # if not, go through them to find the interesting once
                for wf in wfs:
                    wf = wf.strip("*?")
                    if wf in wordlist:
                        worddata.setdefault(wf, []).append((_id, hit["_source"]))

        except Exception as e:
            return jsonify(
                {
                    "error": f"{e}",
                    "called": karp_q,
                    "words": words,
                    "hits": res.get("hits", {}).get("hits"),
                }
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
        wordlist = [
            (word, word.replace(" ", "_")) for word in wordlist if word in worddata
        ]
        return render_template(
            "lex.html",
            hword=wordlist[0][0],
            words=wordlist,
            data=worddata,
            hitlist="/".join([w[0] for w in wordlist]),
            # count the number of hits that we decided to keep
            hits=sum(len(v) for v in list(worddata.values())),
        )

    @app.route("/")
    def main():
        APP_STATIC = os.path.join(app.config["APPLICATION_PATH"], "pages")
        textdirspath = os.path.join(APP_STATIC, "lists/dirs.txt")
        dirs = []
        for d in codecs.open(textdirspath).readlines():
            path, text = d.split("\t")
            dirs.append((f"dir/{path.strip()}", text.strip()))
        return render_template("firstpage.html", textdirs=dirs, title="")

    @app.route("/dir/<dirname>")
    def showdir(dirname):
        APP_STATIC = os.path.join(app.config["APPLICATION_PATH"], "pages")
        textspath = os.path.join(APP_STATIC, dirname)
        dirs = []
        for d in codecs.open(f"{textspath}/content.txt").readlines():
            path, text, year = d.split("|")
            path = f"/fsvreader/reader/{dirname}/{path}"
            dirs.append(
                (path.strip(), text.strip().strip('"'), year.strip().strip('"'))
            )

        return render_template(
            "menu.html", textdirs=dirs, title="Texter", backbutton=".."
        )

    @app.route("/file/<dirname>/<filename>")
    def showtext(dirname, filename):
        APP_STATIC = os.path.join(app.config["APPLICATION_PATH"], "pages")
        dirpath = os.path.join(APP_STATIC, dirname)
        textspath = os.path.join(dirpath, filename)
        text = codecs.open(textspath).read()
        return render_template("fsvtext.html", text=text, back=f"../../dir/{dirname}")

    return app


app = create_app()


########################################
def serve_static_page(page, title=""):
    with app.open_resource(f"pages/static/{page}.html") as f:
        data = f.read()

    return render_template("page_static.html", content=data, title=title)


def send_static_file(page):
    path = urllib.parse.urljoin(app.config["APPLICATION_PATH"], f"pages/static/{page}")
    return send_file(path)


def karp_query(action, query):
    query["mode"] = "historic_ii"
    query["resource"] = "schlyter,soederwall,soederwall-supp"
    query["size"] = 25  # app.config['RESULT_SIZE']
    params = urllib.parse.urlencode(query)
    return karp_request(f"{action}?{params}")


def karp_request(action):
    q = Request(f'{app.config["KARP"]}/{action}')
    response = urlopen(q).read()
    return json.loads(response)


# @app.template_filter('deescape')
# def deescape_filter(s):
#     html_parser = html.parser.HTMLParser()
#     return html_parser.unescape(s)

##########################################


# @app.errorhandler(Exception)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response


if __name__ == "__main__":
    app.run(port=5002)
