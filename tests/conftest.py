import os
import tempfile

import pytest

from smurl import create_app
from smurl.db import get_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(
        test_config={"TESTING": True, "DATABASE": db_path, "SECRET_KEY": "TEST"}
    )

    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql") as schema:
            db.executescript(schema.read().decode("UTF-8"))

    yield app

    os.close(db_fd)
    os.unlink(db_path)
