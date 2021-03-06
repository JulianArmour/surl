from flask import Flask
from flask_restful import Api

from surl import db
from surl.resource.url_map import UrlMap
from surl.view.shortener import shortener_bp


def create_app(test_config=None):
    app = Flask(__name__)
    api = Api(app)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_envvar("PROD_CONFIG")

    db.init_app(app)

    app.register_blueprint(shortener_bp)
    api.add_resource(UrlMap, "/api/urls")
    return app
