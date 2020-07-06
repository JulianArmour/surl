def test_visit_shortened(client):
    with client as c:
        rv = c.get("/short")
        assert rv.location == "https://en.wikipedia.org/wiki/Main_Page"


def test_create_shortened(app):
    with app.test_client() as c:
        rv = c.post("/api/urls", json={"original_url": "https://www.python.org/"})
        json_data = rv.get_json()
        assert len(json_data["short_str"]) > 0
        assert json_data["original_url"] == "https://www.python.org/"
        assert json_data["_links"]["short_url"] == "".join(
            (
                app.config["PREFERRED_URL_SCHEME"],
                "://",
                app.config["SERVER_NAME"],
                "/",
                json_data["short_str"],
            )
        )


# TODO test generating a hash that was taken by a custom url
