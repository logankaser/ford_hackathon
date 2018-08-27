"""Initialize app_server."""

import os

from flask import Flask, render_template
from app_server.models import db, bcrypt, search, ma, User
from app_server.auth import login_required


def create_app(test_config=None):
    """Create app_server instance."""
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder="resources")
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(
            app.instance_path, "database.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        BCRYPT_LOG_ROUNDS=12,
        MSEARCH_INDEX_NAME="search_index",
        MSEARCH_BACKEND="simple",
        MSEARCH_ENABLE=True,
        ADMIN_PASSWORD="password",
        MAILGUN_DOMAIN="mail.fordhackathon.com",
        MAILGUN_KEY="key-88a8a25eb4a4b21be0150838cfe141c0"
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
    with app.app_context():
        if not User.query.filter_by(username="admin").count():
            admin = User(
                "admin@admin.admin",
                "admin", app.config.get("ADMIN_PASSWORD", "password"),
                admin=True
            )
            db.session.add(admin)
            db.session.commit()

    # Initialize Password Hashing
    bcrypt.init_app(app)

    # Initialize Search
    search.init_app(app)
    if app.config.get("MSEARCH_BACKEND") == "whoosh":
        with app.app_context():
            search.create_index()
            search.update_index()

    # Initialize Marshmallow Serialization
    ma.init_app(app)

    # Initialize Blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import dev
    app.register_blueprint(dev.bp)

    from . import api
    app.register_blueprint(api.bp)

    @app.route("/")
    @login_required
    def index():
        return render_template("home.html")

    return app
