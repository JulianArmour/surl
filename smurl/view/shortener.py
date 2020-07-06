from flask import Blueprint

from smurl.db import get_db

shortener = Blueprint("shortener", __name__)


@shortener.route("/<short_hash>")
def redirect(short_hash):
    db = get_db()
