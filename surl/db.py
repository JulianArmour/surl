import os
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@click.command("create-db", )
@with_appcontext
def create_db():
    if os.path.exists(current_app.config["DATABASE"]):
        raise click.ClickException(
            "A database already exists at the location specified in the DATABASE configuration"
        )

    db = get_db()
    with current_app.open_resource("schema.sql") as schema:
        db.executescript(schema.read().decode("UTF-8"))
    click.echo("Created database!")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(create_db)
