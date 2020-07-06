def test_visit_shortened(client):
    with client as c:
        rv = c.get("/short")
        assert rv.location == "www.example.com/something"
