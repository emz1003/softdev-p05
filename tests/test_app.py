import pytest
from flask import url_for

def test_home(client):
    res = client.get(url_for('home'))
    assert res.status_code == 200

def test_login(client):
    res = client.get(url_for('auth'))
    assert res.status_code == 302
