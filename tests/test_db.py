import os
import sqlite3
import tempfile

import pytest

from surl import create_app
from surl.db import get_db, close_db


def test_get_db(app):
    with app.app_context():
        db = get_db()
        # get_db() returns the same object within an app context
        assert db is get_db()
        # g.db = db after calling get_db()


def test_get_db_close_db_app_context(app):
    with app.app_context():
        db = get_db()
        assert db
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute("SELECT 1")


def test_close_db(app):
    with app.app_context():
        db = get_db()
        close_db()
        with pytest.raises(sqlite3.ProgrammingError):
            db.execute("SELECT 1")


def test_create_db_already_exist():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(test_config={"TESTING": True, "DATABASE": db_path})
    cli = app.test_cli_runner()

    result = cli.invoke(args=["create-db"])
    assert "A database already exists" in result.output

    os.close(db_fd)
    os.unlink(db_path)


def test_create_db_uncreated():
    db_path = os.path.join(tempfile.gettempdir(), "a_temp_db.sqlite")
    app = create_app(test_config={"TESTING": True, "DATABASE": db_path})
    cli = app.test_cli_runner()

    result = cli.invoke(args=["create-db"])
    assert "Created database" in result.output

    os.unlink(db_path)
