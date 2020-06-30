import sqlite3

import pytest
from flask import g

from smurl.db import get_db, close_db


def test_get_db(app):
    with app.app_context():
        db = get_db()
        # get_db() returns the same object within an app context
        assert db is get_db()
        # g.db = db after calling get_db()
        assert g.db is db
    # get_db() throws an exception when outside an app context
    with pytest.raises(sqlite3.ProgrammingError):
        db.execute("SELECT 1")


def test_close_db(app):
    with app.app_context():
        db = get_db()
        close_db()
        with pytest.raises(sqlite3.ProgrammingError):
            db.execute("SELECT 1")
