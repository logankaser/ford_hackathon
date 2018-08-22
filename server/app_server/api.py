import functools
import os.path
import datetime

from flask import (
    Blueprint, g, redirect, render_template, request,
    session, Response, current_app
)
from app_server import db
from app_server.models import AppEntry, User, AppSchema, AppPublicSchema
from app_server.auth import login_required

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/app/<app_id>")
@login_required
def app_json(app_id):
    app = AppEntry.query.filter_by(id=app_id).one_or_none()
    if not app:
        return Response("App not found", 404)
    if g.user.id != app.dev_id and not g.user.admin:
        return ("", 401)
    app_schema = AppSchema()
    return app_schema.jsonify(app)


@bp.route("/app")
@login_required
def apps_json():
    apps = AppEntry.query.all()
    if not apps:
        return Response("No apps", 404)
    if g.user.id != app.dev_id and not g.user.admin:
        return ("", 401)
    app_schema = AppSchema(many=True)
    return app_schema.jsonify(apps)


@bp.route("/search/<keyword>", methods=["GET"])
def search(keyword):
    results = AppEntry.query.msearch(keyword, fields=["name", "description"]).\
        filter_by(approved=True).limit(100)
    modified_results = []
    for result in results:
        result.dev_name = User.query.filter_by(id=result.dev_id).one().username
        modified_results.append(result)
    app_schema = AppPublicSchema(many=True)
    return app_schema.jsonify(modified_results)


@bp.route("/approve/<app_id>", methods=["GET", "POST"])
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


@bp.route("/icon/<app_id>/public", methods=["GET"])
def public_app_icon(app_id):
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        if not app.approved:
            return ("", 401)
        file_path = os.path.join(
            current_app.instance_path, str(app.id) + app.icon_ext)
        return send_file(file_path)
    except Exception as e:
        return ("", 400)


@bp.route("/icon/<app_id>/private", methods=["GET"])
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
