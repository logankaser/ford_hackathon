import functools
import os.path
import datetime

from flask import (
    Blueprint, g, redirect, render_template, request,
    session, Response, current_app
)
from app_server import db
from app_server.models import AppEntry, AppSchema
from app_server.auth import login_required

bp = Blueprint("api/v1", __name__, url_prefix="/api/v1")


@bp.route("/app/<app_id>")
@login_required
def app_json(app_id):
    app = AppEntry.query.filter_by(id=app_id).one_or_none()
    if not app:
        return Response("App not found", 404)
    app_schema = AppSchema()
    return app_schema.jsonify(app)


@bp.route("/app")
@login_required
def apps_json():
    apps = AppEntry.query.all()
    if not apps:
        return Response("No apps", 404)
    app_schema = AppSchema(many=True)
    return app_schema.jsonify(apps)
