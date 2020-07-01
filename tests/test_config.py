from smurl import create_app


def test_test_config():
    app = create_app({"TEST_CONFIG_PASS": True})
    assert app.config["TEST_CONFIG_PASS"]


def test_instance_config():
    app = create_app()
    assert app.config["SECRET_KEY"] is not None
    assert app.config["DATABASE"] is not None
