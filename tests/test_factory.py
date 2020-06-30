from smurl import create_app


def test_create_app():
    assert create_app() is not None


def test_default_config():
    app = create_app()
    assert app.config["SECRET_KEY"] is "DEV"
