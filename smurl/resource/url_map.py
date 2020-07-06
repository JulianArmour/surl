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
        c.execute("INSERT INTO HashIdGen DEFAULT VALUES")
        new_id = c.lastrowid
        id_hash = shortener.hash_from_id(new_id)
        c.execute(
            "INSERT INTO UrlMap (original_url, short_hash) VALUES (?,?)",
            (args["original_url"], id_hash),
        )

        return {
            "_links": {
                "short_url": url_for(
                    "shortener.redirect_short", short_hash=id_hash, _external=True
                )
            },
            "original_url": args["original_url"],
            "short_str": id_hash,
        }
