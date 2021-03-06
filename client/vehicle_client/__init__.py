"""Initialize a new vehicle_client instance."""

import os

from flask import Flask, render_template
from vehicle_client.models import db, ma


def create_app(test_config=None):
    """Create a new app.

    :param test_config: Optionaly load configuration from python dict,
    useful for testing.
    :returns: New app:
    """
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder="resources")
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(
            app.instance_path, "database.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        API_DOMAIN="http://localhost:5000"
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize DB
    db.init_app(app)
    db.create_all(app=app)

    # Initialize Marshmallow Serialization
    ma.init_app(app)

    # Initialize Blueprints
    from . import local
    app.register_blueprint(local.bp)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def index(path):
        return render_template(
            "index.html", api_domain=app.config.get("API_DOMAIN")
        )

    return app
