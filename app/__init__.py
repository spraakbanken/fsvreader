# -*- coding: utf-8 -*
import os
import os.path
import json
import logging
import urllib
import shutil
import sys

from flask import Flask, g, request, redirect, render_template, url_for
from flask_babel import Babel
from setuptools import setup
from urllib2 import Request, urlopen
import HTMLParser


app = Flask(__name__)

# if os.path.exists(app.config.root_path + '/config.cfg') is False:
#     print "copy config.default.cfg to config.cfg and add your settings"
#     app.config.from_pyfile(app.config.root_path + '/config.default.cfg')
# else:
#     app.config.from_pyfile(app.config.root_path + '/config.cfg')



def serve_static_page(page, title=''):
    with app.open_resource("pages/static/%s.html" % page) as f:
        data = f.read()

    return render_template('page_static.html',
                           content=data.decode('utf-8'),
                           title=title)


def karp_query(action, query):
    query['mode'] = 'historic_ii'
    query['resource'] = 'schlyter,soederwall,soederwall-supp'
    query['size'] = 25 # app.config['RESULT_SIZE']
    params = urllib.urlencode(query)
    return karp_request("%s?%s" % (action, params))


def karp_request(action):
    backend = 'https://ws.spraakbanken.gu.se/ws/karp/v5/'
    q = Request("%s/%s" % (backend, action))
    response = urlopen(q).read()
    logging.debug(q)
    data = json.loads(response)
    return data


@app.template_filter('deescape')
def deescape_filter(s):
    # return s.replace("&amp;", "&").replace("&apos;", "'").replace("&quot;", '"')
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(s)


from views import *
#from app import views

if __name__ == '__main__':
    if sys.version_info.major < 3:
        reload(sys)
    sys.setdefaultencoding('utf8')
    app.run(port='5002')
