import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": "DEV",
        "DATABASE": os.path.join(app.instance_path, "smurl-db.sqlite")
    })
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app
