"""API for the client."""

import functools
import os.path
import datetime

from flask import (
    Blueprint, g, redirect, render_template, request,
    session, Response, current_app, send_file
)
from app_server import db
from app_server.models import (
    AppEntry, User, AppSchema, AppPublicSchema,
    UserSchema, UserPublicSchema
)
from app_server.auth import login_required
from flask_cors import CORS

bp = Blueprint("api/v1", __name__, url_prefix="/api/v1")
CORS(bp)


@bp.route("/app/<app_id>")
@login_required
def app_json(app_id):
    """JSON for private app profile.

    :param app_id: Application ID
    :returns: JSON string of the private app profile
    """
    app = AppEntry.query.filter_by(id=app_id).one_or_none()
    if not app:
        return ("App not found", 404)
    if g.user.id != app.dev_id and not g.user.admin:
        return ("", 401)
    app_schema = AppSchema()
    return app_schema.jsonify(app)


@bp.route("/app/top")
def apps_json():
    """Top 100 public app profiles by downloads.

    :returns: JSON string of up to 100 public
    app profiles from most to least downloaded
    :limitations: top 100 apps are calculated each api call and not stored
    anywhere
    """
    apps = AppEntry.query.order_by(AppEntry.downloads.desc()).limit(100)
    app_schema = AppPublicSchema(many=True)
    output = []
    for app in apps:
        app.dev_name = User.query.filter_by(id=app.dev_id).one().username
        output.append(app)
    return app_schema.jsonify(output)
    apps = AppEntry.query.all()
    if not apps:
        return ("No apps", 404)
    app_schema = AppSchema(many=True)
    return app_schema.jsonify(apps)


@bp.route("/app/search/<keyword>", methods=["GET"])
def search(keyword):
    """Best 100 public app profiles that match search phrase.

    :param keyword: phrase used for searching
    :returns: JSON string of up to 100 public app profiles from
    most relevent to least
    relevent
    :limitations: only words in the app name and description are matched
    """
    results = AppEntry.query.msearch(keyword, fields=["name", "description"]).\
        filter_by(approved=True).limit(100)
    app_schema = AppPublicSchema(many=True)
    output = []
    for result in results:
        result.dev_name = User.query.filter_by(id=result.dev_id).one().username
        output.append(result)
    return app_schema.jsonify(output)


@bp.route("/app/<app_id>/approve", methods=["GET", "POST"])
@login_required
def approve(app_id):
    """Approve an app. Requires admin.

    :param app_id: Application ID
    :returns: 204 - success, 400 - app does not exist, 401 - bad permission
    """
    if not g.user.admin:
        return ("", 401)
    try:
        AppEntry.query.filter_by(id=app_id).one().approved = True
    except Exception as e:
        return ("", 400)
    db.session.commit()
    return ("", 204)


@bp.route("/app/<app_id>/delete", methods=["GET", "POST"])
@login_required
def delete_app(app_id):
    """Delete any app of admin or owned app if dev.

    :param app_id: Application ID
    :returns: 204 - success, 400 - app does not exist, 401 - bad permission
    """
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        if g.user.id != app.dev_id and not g.user.admin:
            return ("", 401)
        os.remove(os.path.join(current_app.instance_path, app_id + ".tar.gz"))
        os.remove(
            os.path.join(current_app.instance_path, app_id + app.icon_ext))
        db.session.delete(app)
        db.session.commit()
    except Exception as e:
        return ("", 400)
    return ("", 204)


@bp.route("/app/<app_id>/icon", methods=["GET"])
def public_app_icon(app_id):
    """Get the icon of an approved app.

    :param app_id: Application ID
    :returns: file contents of image or 400 if app does not exist
    """
    app = AppEntry.query.get(app_id)
    if not app or not app.approved:
        return ("App not found", 400)
    file_path = os.path.join(
        current_app.instance_path, str(app.id) + app.icon_ext)
    return send_file(file_path)


@bp.route("/app/<app_id>/icon/private", methods=["GET"])
@login_required
def private_app_icon(app_id):
    """Get the icon of any app.

    :param app_id: Application ID
    :returns: file contents of image - success, 400 - app does not exist,
    401 - bad permission

    only admins or the developer of the app have valid permissions
    """
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        if g.user.id != app.dev_id and not g.user.admin:
            return ("", 401)
        file_path = os.path.join(
            current_app.instance_path, str(app.id) + app.icon_ext)
        return send_file(file_path)
    except Exception as e:
        return ("", 400)


@bp.route("user/make_dev", methods=["GET", "POST"])
@login_required
def make_dev():
    """Make the user a developer.

    :returns: 204 - always succeeds
    """
    User.query.filter_by(id=g.user.id).one().dev = True
    db.session.commit()
    return ("", 204)


@bp.route("user/<user_id>/private", methods=["GET"])
@login_required
def private_user_info(user_id):
    """Get a JSON string of a user's private infomation.

    :returns: JSON of user - success, 400 - user does not exist,
    401 - bad permission

    only admins have valid permissions
    """
    if not g.user.admin:
        return ("bad permission", 401)
    user = User.query.filter_by(id=user_id).one_or_none()
    if not user:
        return ("user does not exist", 400)
    user_schema = UserSchema()
    return user_schema.jsonify(user)


@bp.route("user/<user_id>", methods=["GET"])
def public_user_info(user_id):
    """Get a JSON string of a user's public infomation.

    :returns: JSON of user - success, 400 - user does not exist
    """
    user = User.query.filter_by(id=user_id).one_or_none()
    if not user:
        return ("user does not exist", 400)
    user_schema = UserPublicSchema()
    return user_schema.jsonify(user)


@bp.route("user/<user_id>/apps", methods=["GET"])
def user_apps(user_id):
    """Get a list of."""
    apps = AppEntry.query.filter_by(dev_id=user_id)
    name = User.query.get(user_id)
    app_schema = AppPublicSchema(many=True)
    output = []
    for app in apps:
        app.dev_name = name.username
        output.append(app)
    return app_schema.jsonify(output)
