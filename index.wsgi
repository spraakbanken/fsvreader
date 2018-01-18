import os
import sys

datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'fsvreader2'))

activate_this = os.path.join(datadir, 'venv', 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

if datadir not in sys.path:
    sys.path.append(datadir)

from app import app as real_application

def application(env, resp):
    env['SCRIPT_NAME'] = ''
    return real_application(env, resp)

