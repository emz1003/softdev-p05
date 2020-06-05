import pytest
from flask import *

class TestApp:
    def test_home(self, client):
        res = client.get(url_for('home'))
        assert res.status_code == 200

    def test_login(self, client):
        res = client.get(url_for('auth'))
        assert res.status_code == 302
