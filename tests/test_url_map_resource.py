import pytest

from smurl.db import get_db
from smurl.shortener import hash_from_id


@pytest.fixture
def app_conflict(app):
    """
    :param app: app fixture
    :return: an app fixture for which the next auto-generated short url will conflict
    with a custom url.
    """
    with app.app_context():
        db = get_db()
        next_id = (
            1 + db.execute("SELECT coalesce(max(id), 0) FROM HashIdGen").fetchone()[0]
        )
        next_hash = hash_from_id(next_id)
        db.execute(
            "INSERT INTO UrlMap (original_url, short_hash) VALUES (?,?)",
            ("http://something.io", next_hash),
        )
        db.commit()
    return app, next_id


def assert_response(app, rv, req_data, expected_hash=None):
    json_data = rv.get_json()
    assert len(json_data["short_str"]) > 0
    assert json_data["original_url"] == req_data["original_url"]
    assert json_data["_links"]["short_url"] == "".join(
        (
            app.config["PREFERRED_URL_SCHEME"],
            "://",
            app.config["SERVER_NAME"],
            "/",
            expected_hash if expected_hash else json_data["short_str"],
        )
    )


def test_post_generate(app):
    with app.test_client() as c:
        req_data = {"original_url": "https://www.python.org/"}
        rv = c.post("/api/urls", json=req_data)
        assert_response(app, rv, req_data)


def test_post_generate_with_conflict(app_conflict):
    app, next_id = app_conflict
    with app.test_client() as c:
        req_data = {"original_url": "http://something.io"}
        rv = c.post("/api/urls", json=req_data)
        assert_response(app, rv, req_data, expected_hash=hash_from_id(1 + next_id))
