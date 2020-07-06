from flask import Blueprint, redirect

from smurl.db import get_db

shortener_bp = Blueprint("shortener", __name__)


@shortener_bp.route("/<short_hash>")
def redirect_short(short_hash):
    db = get_db()
    url = db.execute(
        "SELECT original_url FROM UrlMap WHERE short_hash = ?", (short_hash,)
    ).fetchone()["original_url"]
    return redirect(url)
