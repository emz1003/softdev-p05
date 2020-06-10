#!/usr/bin/python3
import sys
import os
sys.path.insert(0, "/var/www/learninationmachine/")
sys.path.insert(0, "/var/www/learninationmachine/learninationmachine/")

import logging
logging.basicConfig(stream = sys.stderr)

from learninationmachine import app as _application

def application(req_environ, start_response):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    os.environ['PASSPHRASE'] = '42069'

    return _application(req_environ, start_response)
