"""API for the client."""

import functools
import os.path
import datetime

from flask import (
    Blueprint, g, redirect, render_template, request,
    session, Response, current_app, send_file
)
from app_server import db
from app_server.models import AppEntry, User, AppSchema, AppPublicSchema
from app_server.auth import login_required
from flask_cors import CORS

bp = Blueprint("api/v1", __name__, url_prefix="/api/v1")
CORS(bp)


@bp.route("/app/<app_id>")
@login_required
def app_json(app_id):
    """JSON for a secific app.

    :param app_id: Application ID
    :returns: JSON string of the app
    """
    app = AppEntry.query.filter_by(id=app_id).one_or_none()
    if not app:
        return ("App not found", 404)
    if g.user.id != app.dev_id and not g.user.admin:
        return ("", 401)
    app_schema = AppSchema()
    return app_schema.jsonify(app)


@bp.route("/app")
def apps_json():
<<<<<<< HEAD
    """JSON of all apps.

    :param: JSON applications
    :returns: JSON of all apps
    """
=======
    '''
    JSON applications

    :returns: JSON string of the app
    :raises 404: No apps were found
    '''
>>>>>>> nothing really changed. Just wanted to rebase:
    apps = AppEntry.query.all()
    if not apps:
        return ("No apps", 404)
    app_schema = AppSchema(many=True)
    return app_schema.jsonify(apps)


@bp.route("/app/search/<keyword>", methods=["GET"])
def search(keyword):
    results = AppEntry.query.msearch(keyword, fields=["name", "description"]).\
        filter_by(approved=True).limit(100)
    modified_results = []
    for result in results:
        result.dev_name = User.query.filter_by(id=result.dev_id).one().username
        modified_results.append(result)
    app_schema = AppPublicSchema(many=True)
    return app_schema.jsonify(modified_results)


@bp.route("/app/<app_id>/approve", methods=["GET", "POST"])
@login_required
def approve(app_id):
    if not g.user.admin:
        return ("", 401)
    try:
        AppEntry.query.filter_by(id=app_id).one().approved = True
    except Exception as e:
        return ("", 400)
    db.session.commit()
    return ("", 204)


@bp.route("/delete/<app_id>", methods=["GET", "POST"])
@login_required
def delete_app(app_id):
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
    app = AppEntry.query.get(app_id)
    if not app or not app.approved:
        return ("App not found", 400)
    file_path = os.path.join(
        current_app.instance_path, str(app.id) + app.icon_ext)
    return send_file(file_path)


@bp.route("/app/<app_id>/icon/private", methods=["GET"])
@login_required
def private_app_icon(app_id):
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        if g.user.id != app.dev_id and not g.user.admin:
            return ("", 401)
        file_path = os.path.join(
            current_app.instance_path, str(app.id) + app.icon_ext)
        return send_file(file_path)
    except Exception as e:
        return ("", 400)
