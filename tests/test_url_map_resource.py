import pytest

from Surl.db import get_db
from Surl.shortener import hash_from_id


@pytest.fixture
def app_conflict_next_generated(app):
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
    assert json_data["_links"]["short_url"]["href"] == "".join(
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


def test_post_generate_with_conflict(app_conflict_next_generated):
    app, next_id = app_conflict_next_generated
    with app.test_client() as c:
        req_data = {"original_url": "http://something.io"}
        rv = c.post("/api/urls", json=req_data)
        assert_response(app, rv, req_data, expected_hash=hash_from_id(1 + next_id))


def test_post_custom_url(app):
    with app.test_client() as c:
        req_data = {
            "original_url": "http://google.com",
            "short_str": "custom_url",
        }
        rv = c.post("/api/urls", json=req_data)
        assert_response(app, rv, req_data, expected_hash="custom_url")


def test_post_custom_url_conflict(app):
    req_data = {
        "original_url": "http://asdf.com",
        "short_str": "short",
    }
    with app.test_client() as c:
        rv = c.post("/api/urls", json=req_data)
        assert rv.status_code == 409


@pytest.mark.parametrize(
    "req_data",
    [
        {"original_url": "http://google.com", "short_str": "custom_url"},
        {"original_url": "https://abc.ca"},
    ],
)
def test_post_redirect(app, req_data):
    with app.test_client() as c:
        json = c.post("/api/urls", json=req_data).get_json()
        url = json["_links"]["short_url"]["href"]
        assert c.get(url).location == req_data["original_url"]
