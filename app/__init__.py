# -*- coding: utf-8 -*
import sys
from flask import Flask
import importlib


app = Flask(__name__)

# import all urls
from .views import *

if __name__ == '__main__':
    if sys.version_info.major < 3:
        importlib.reload(sys)
    sys.setdefaultencoding('utf8')
    app.run(port='5002')
