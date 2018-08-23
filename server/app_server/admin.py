"""Admin blueprint."""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app_server import db
from app_server.auth import admin_required
from app_server.models import AppEntry, User

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
@admin_required
def admin_home():
    apps = AppEntry.query.filter_by(approved=False).limit(20)
    return render_template("admin_profile.html", apps=apps)


@bp.route("/user/search/<keyword>", methods=["GET", "POST"])
@admin_required
def admin_user_search(keyword):
    users = User.query.msearch(keyword, fields=["id", "username", "email"]).\
        limit(100)
    return render_template("admin_user_search.html", users=users)


@bp.route("/app/search/<keyword>", methods=["GET", "POST"])
@admin_required
def admin_app_search(keyword):
    apps = AppEntry.query.msearch(keyword, fields=["id", "name", "description"]).\
        limit(100)
    return render_template("admin_app_search.html", apps=apps)


@bp.route("/app/<app_id>", methods=["GET"])
@admin_required
def admin_app_view(app_id):
    app = AppEntry.query.get(app_id)
    if not app:
        return ("App not found", 400)
    user = User.query.get(app.dev_id)
    return render_template("admin_app_view.html", app=app, dev=user)

@bp.route("/user/<user_id>", methods=["GET"])
@admin_required
def admmin_app_view(user_id):
    user = User.query.get(user_id)
    if not user:
        return ("User not found", 400)
    return render_template("admin_user_view.html", user=user)