import pytest

from smurl import create_app


@pytest.fixture
def app():
    return create_app()
