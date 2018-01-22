import codecs
from flask import jsonify, render_template, Flask
import HTMLParser  # in app
import json  # in app
import os
import urllib  # in app
from urllib2 import Request, urlopen  # in app
import xml.etree.ElementTree as etree


app = Flask(__name__)
app.config["APPLICATION_ROOT"] = ""
app.config["HOST"] = "http://localhost:5002"
app.config['KARP'] = 'https://ws.spraakbanken.gu.se/ws/karp/v4/'


########################################
# TODO should be in app, but can't import
def serve_static_page(page, title=''):
    with app.open_resource("pages/static/%s.html" % page) as f:
        data = f.read()

    return render_template('page_static.html',
                           content=data.decode('utf-8'),
                           title=title)


def karp_query(action, query):
    query['mode'] = 'historic_ii'
    query['resource'] = 'schlyter,soederwall,soederwall-supp'
    query['size'] = 25  # app.config['RESULT_SIZE']
    params = urllib.urlencode(query)
    return karp_request("%s?%s" % (action, params))


def karp_request(action):
    q = Request("%s/%s" % (app.config['KARP'], action))
    response = urlopen(q).read()
    # logging.debug(q)
    data = json.loads(response)
    return data


@app.template_filter('deescape')
def deescape_filter(s):
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(s)

##########################################


@app.route('/fsvreader.html')
def text():
    return serve_static_page("fsvreader")


@app.route("/reader")
def reader():
    return render_template('reader.html', textframe='fsvreader.html',
                           lexframe="fsvreader/lexseasy/hund--hime",
                           lexurl=app.config["APPLICATION_ROOT"]+"/fsvreader/lexseasy/",
                           host=app.config["HOST"])


@app.route("/reader/<textdir>/<textfile>")
def readerfile(textdir, textfile):
    texturl = '%s/file/%s/%s' % (app.config["APPLICATION_ROOT"], textdir, textfile)
    # texturl = url_for('file/%s/%s' % (textdir, textfile))
    return render_template('reader.html', textframe=texturl,
                           lexframe=app.config["APPLICATION_ROOT"]+"/fsvreader/lexseasy/",
                           lexurl=app.config["APPLICATION_ROOT"]+"/fsvreader/lexseasy/",
                           host=app.config["HOST"])


@app.route('/fsvlex.html')
def lex():
    return serve_static_page("fsvlex")


@app.route('/fsvreader/lexseasy/')
def emptylookup():
    return ""


@app.route('/fsvreader/lexseasy/<words>')
def lookup(words):
    karp_q = ''
    worddata = {}
    try:
        worddata = {}
        wordlist = words.split('--')
        if len(wordlist) > 1 and wordlist[0] == wordlist[1]:
            wordlist = wordlist[1:]
        wordlist = [word.replace('_', ' ') for word in wordlist]
        karp_q = {'q': "extended||and|wfC|equals|%s" % '|'.join(wordlist).encode('utf8')}
        res = karp_query('query', karp_q)
    except:
        return jsonify({"call": karp_q, "words": words,
                        "splitted": '|'.join(words.split('--'))})
    try:
        for hit in res.get('hits', {}).get('hits', []):
            base = hit['_source'].get('FormRepresentations', [{}])[0].get('baseform')
            wfs = [wf.get('writtenForm', '') for wf in hit['_source'].get('WordForms', [{}])]
            # xml = hit['_source'].get('xml', '')
            text = " ".join(etree.fromstring(hit['_source'].get('xml').encode('utf-8')).itertext())
            if len(text) > 30:
                hit['_source']['pre'] = text[:30]
            hit['_source']['text'] = text
            pos = hit['_source'].get('FormRepresentations', [{}])[0].get('partOfSpeech', '')
            if type(pos) == list:
                pos = ', '.join(pos)
            hit['_source']['pos'] = pos

            worddata.setdefault(base, []).append(hit['_source'])
            for wf in wfs:
                if not wf or wf not in wordlist:
                    continue
                worddata.setdefault(wf, []).append(hit['_source'])
    except Exception as e:
        return jsonify({"error": "%s" % e, "called": karp_q, "words": words,
                        "hits": res.get('hits', {}).get('hits')})

    #for word in words.split('--'):
    #    if word not in worddata:
    #        karp_q = {'q' : "extended||and|baseform|equals|%s" % word}
    #        worddata[word] = karp_query('query', karp_q)
    wordlist = [(word, word.replace(' ', '_')) for word in wordlist]
    return render_template('lex.html', hword=wordlist[0][0], words=wordlist,
                           data=worddata,
                           hits=res.get("hits", {}).get("total", 0))


@app.route('/')
def main():
    # move to config or use the config above
    APP_STATIC = os.path.join(app.config['APPLICATION_ROOT'], 'pages')
    textdirspath = os.path.join(APP_STATIC, 'lists/dirs.txt')
    dirs = []
    for d in codecs.open(textdirspath).readlines():
        path, text = d.split('\t')
        dirs.append(('dir/'+path.strip(), text.strip()))
    return render_template('menu.html', textdirs=dirs, title="Kategorier")


@app.route('/dir/<dirname>')
def showdir(dirname):
    # move to config or use the config above
    APP_STATIC = os.path.join(app.config['APPLICATION_ROOT'], 'pages')
    textspath = os.path.join(APP_STATIC, dirname)
    dirs = []
    root = app.config["APPLICATION_ROOT"]
    for d in codecs.open(textspath+'/content.txt').readlines():
        path, text, year = d.split('|')
        path = '%s/reader/%s/%s' % (root, dirname, path)
        dirs.append((path.strip(), text.strip().strip('"'), year.strip().strip('"')))

    return render_template('menu.html', textdirs=dirs, title="Texter")


@app.route('/file/<dirname>/<filename>')
def showtext(dirname, filename):
    # move to config or use the config above
    APP_STATIC = os.path.join(app.config['APPLICATION_ROOT'], 'pages')
    dirpath = os.path.join(APP_STATIC, dirname)
    textspath = os.path.join(dirpath, filename)
    text = codecs.open(textspath).read()
    return render_template('fsvtext.html', text=text)
