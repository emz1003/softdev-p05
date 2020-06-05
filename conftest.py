import pytest
import sys
sys.path.append("app/")

from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app
