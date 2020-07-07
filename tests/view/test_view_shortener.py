def test_visit_shortened(client):
    with client as c:
        rv = c.get("/short")
        assert rv.location == "https://en.wikipedia.org/wiki/Main_Page"
