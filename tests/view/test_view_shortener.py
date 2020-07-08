def test_visit_shortened(app):
    with app.test_client() as c:
        rv = c.get("/short")
        assert rv.location == "https://en.wikipedia.org/wiki/Main_Page"
