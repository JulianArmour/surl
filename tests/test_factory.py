import pytest


def test_create_app(app):
    assert app is not None


def test_default_config(app):
    assert app.config["SECRET_KEY"] is "DEV"
