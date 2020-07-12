from flask import Blueprint, redirect, render_template

from surl.db import get_db

shortener_bp = Blueprint("shortener", __name__)


@shortener_bp.route("/<short_hash>")
def redirect_short(short_hash):
    db = get_db()
    url = db.execute(
        "SELECT original_url FROM UrlMap WHERE short_hash = ?", (short_hash,)
    ).fetchone()["original_url"]
    return redirect(url)


@shortener_bp.route("/")
def index():
    return render_template("index.html")
