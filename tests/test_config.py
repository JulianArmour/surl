import os
import tempfile

from surl import create_app


def test_test_config():
    app = create_app({"TEST_CONFIG_PASS": True})
    assert app.config["TEST_CONFIG_PASS"]


def test_environment_var_config(monkeypatch):
    temp_fd, temp_path = tempfile.mkstemp(".py")
    with os.fdopen(temp_fd, "wb") as cfg:
        cfg.write(b"FLASK_CONFIG_FROM_ENV = True")
    monkeypatch.setenv("PROD_CONFIG", temp_path)
    app = create_app()

    with app.app_context():
        assert app.config["FLASK_CONFIG_FROM_ENV"]

    os.unlink(temp_path)
