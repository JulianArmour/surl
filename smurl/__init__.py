import os

from flask import Flask
from flask_restful import Api

from smurl import db
from smurl.resource.url_map import UrlMap
from smurl.view.shortener import shortener_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile("config.py")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(shortener_bp)
    api.add_resource(UrlMap, "/api/urls")
    return app
