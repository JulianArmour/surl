import os

from flask import Flask

from smurl import db


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        # default config
        {
            "SECRET_KEY": "DEV",
            "DATABASE": os.path.join(app.instance_path, "smurl-db.sqlite"),
        }
    )
    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    return app
