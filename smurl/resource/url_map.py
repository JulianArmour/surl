import sqlite3

from flask import url_for
from flask_restful import Resource, reqparse, inputs

from smurl import shortener
from smurl.db import get_db

parser = reqparse.RequestParser()
parser.add_argument("original_url", type=inputs.url, required=True, trim=True)


class UrlMap(Resource):
    @staticmethod
    def post():
        args = parser.parse_args()
        db = get_db()
        c = db.cursor()
        # The next generated short hash may be taken by a custom url. Keep trying until
        # a free hash is found.
        while True:
            c.execute("INSERT INTO HashIdGen DEFAULT VALUES")
            db.commit()
            new_id = c.lastrowid
            id_hash = shortener.hash_from_id(new_id)
            try:
                c.execute(
                    "INSERT INTO UrlMap (original_url, short_hash) VALUES (?,?)",
                    (args["original_url"], id_hash),
                )
                db.commit()
                break
            except sqlite3.IntegrityError:
                continue

        return {
            "_links": {
                "short_url": url_for(
                    "shortener.redirect_short", short_hash=id_hash, _external=True
                )
            },
            "original_url": args["original_url"],
            "short_str": id_hash,
        }
