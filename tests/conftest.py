import pytest
from flask import Flask
from app import app

@pytest.fixture
def app():
    app = Flask(__name__)
    app.debug = True
    return app
