#!/usr/bin/python3
import sys
sys.path.insert(0, "/var/www/learninationmachine/")
sys.path.insert(0, "/var/www/learninationmachine/learninationmachine/")

import logging
logging.basicConfig(stream = sys.stderr)

from learninationmachine import app as application
