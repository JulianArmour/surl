import os

from flask import Flask

from smurl import db


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        {
            "SECRET_KEY": "DEV",
            "DATABASE": os.path.join(app.instance_path, "smurl-db.sqlite"),
        }
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)
    return app
