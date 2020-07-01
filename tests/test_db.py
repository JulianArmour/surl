import sqlite3

import pytest

from smurl.db import get_db, close_db, init_db


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


def test_init_db(app, monkeypatch):
    class MockDB:
        ran_query = False
        script_loaded = False

        @staticmethod
        def executescript(sql_script):
            MockDB.ran_query = True
            MockDB.script_loaded = "CREATE".lower() in sql_script.lower()

    def get_db_mock():
        return MockDB()

    monkeypatch.setattr("smurl.db.get_db", get_db_mock)
    with app.app_context():
        init_db()
    assert MockDB.ran_query
    assert MockDB.script_loaded
