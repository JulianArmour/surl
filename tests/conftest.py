import os
import tempfile

import pytest

from surl import create_app
from surl.db import get_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(
        test_config={
            "TESTING": True,
            "DATABASE": db_path,
            "SECRET_KEY": "TEST",
            "SERVER_NAME": "mydomain.com",
            "PREFERRED_URL_SCHEME": "https",
        }
    )
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql") as schema:
            db.executescript(schema.read().decode("UTF-8"))
        with open(os.path.join(os.path.dirname(__file__), "test_data.sql"), "rb") as f:
            db.executescript(f.read().decode("UTF-8"))

    yield app

    os.close(db_fd)
    os.unlink(db_path)
