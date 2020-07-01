import os
import tempfile

import pytest

from smurl import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(test_config={"TESTING": True, "DATABASE": db_path})

    yield app

    os.close(db_fd)
    os.unlink(db_path)
