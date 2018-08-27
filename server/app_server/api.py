"""API for the client."""

import functools
import datetime

from flask import (
    Blueprint, g, redirect, render_template, request,
    session, Response, current_app, send_file, safe_join
)
from app_server import db
from app_server.models import (
    AppEntry, User, AppSchema, AppPublicSchema,
    UserSchema, UserPublicSchema
)
from app_server.auth import login_required, admin_required
from flask_cors import CORS
from secrets import randbelow
import requests
import os

bp = Blueprint("api/v1", __name__, url_prefix="/api/v1")
CORS(bp)


def random_hash256():
    """Random 256bithash."""
    hex_string = "0123456789abcdef"
    output = ""
    for _ in range(64):
        output += hex_string[randbelow(16)]
    return output


def send_email(to, subject, message):
    """Sends an email.
    :param to: email address of reciever
    :param subject: subject of email
    :param message: body of email
    """
    res = requests.post(
        "https://api.mailgun.net/v3/" +
        current_app.config.get("MAILGUN_DOMAIN") +
        "/messages",
        auth=("api", current_app.config.get("MAILGUN_KEY")),
        data={
            "from": "No Reply <" +
                    "noreply@" +
                    current_app.config.get("MAILGUN_DOMAIN") +
                    ">",
            "to": [to],
            "subject": subject,
            "html": message
        })


@bp.route("/app/<app_id>")
def app_json(app_id):
    """JSON for public App.

    :param app_id: Application ID
    :returns: JSON string of the public App
    """
    app = AppEntry.query.get(app_id)
    app.dev_name = User.query.get(app.dev_id).username
    if not app:
        return ("App not found", 404)
    app_schema = AppPublicSchema()
    return app_schema.jsonify(app)


@bp.route("/app/top")
def apps_json():
    """Top 100 public app profiles by downloads.

    :returns: JSON of up to 100 public
    app profiles from most to least downloaded
    :limitations: top 100 apps are calculated each api call and not stored
    anywhere
    """
    apps = AppEntry.query.order_by(AppEntry.downloads.desc()).\
        filter_by(approved=True).limit(100)
    app_schema = AppPublicSchema(many=True)
    output = []
    for app in apps:
        app.dev_name = User.query.get(app.dev_id).username
        output.append(app)
    return app_schema.jsonify(output)


@bp.route("/app/search/<keyword>", methods=["GET"])
def search(keyword):
    """Best 100 public app profiles that match search phrase.

    :param keyword: phrase used for searching
    :returns: JSON of up to 100 public app profiles from
    most relevent to least
    relevent
    :limitations: only words in the app name and description are matched
    """
    results = AppEntry.query.msearch(keyword, fields=["name", "description"]).\
        filter_by(approved=True).limit(100)
    app_schema = AppPublicSchema(many=True)
    output = []
    for result in results:
        result.dev_name = User.query.get(result.dev_id).username
        output.append(result)
    return app_schema.jsonify(output)


@bp.route("/app/<app_id>/approve", methods=["POST"])
@admin_required
def approve(app_id):
    """Approve an app.

    :param app_id: Application ID
    :returns: 200 - success, 404 - app does not exist
    """
    app = AppEntry.query.get(app_id)
    if not app:
        return ("App does not exist", 400)
    app.approved = True
    db.session.commit()
    send_email(User.query.get(app.dev_id).email,
               "Congratulations, your app is now in our store!",
               app.name + " was just accepted into our store.")
    return ("App approved", 200)


@bp.route("/app/<app_id>/delete", methods=["DELETE", "POST"])
@login_required
def delete_app(app_id):
    """Delete any app of admin or owned app if dev.

    :param app_id: Application ID
    :returns: 200 - success, 404 - app does not exist, 401 - bad permission
    """
    app = AppEntry.query.get(app_id)
    if not app:
        return ("App not found", 404)
    if g.user.id != app.dev_id and not g.user.admin:
        return ("Bad permissions", 401)
    os.remove(safe_join(current_app.instance_path, app_id + ".tar.gz"))
    os.remove(safe_join(current_app.instance_path, app_id + app.icon_ext))
    if g.user.admin:
        send_email(User.query.get(app.dev_id).email,
                   "Your app was removed by an admin",
                   app.name + " has just been removed from our store.")
    db.session.delete(app)
    db.session.commit()
    return ("App Deleted", 200)


@bp.route("/app/<app_id>/icon", methods=["GET"])
def public_app_icon(app_id):
    """Get the icon of an approved app.

    :param app_id: Application ID
    :returns: file contents of image or 404 if app does not exist
    """
    app = AppEntry.query.get(app_id)
    if not app or not app.approved:
        return ("App not found", 404)
    file_path = safe_join(
        current_app.instance_path, str(app.id) + app.icon_ext)
    return send_file(file_path)


@bp.route("/app/<app_id>/download", methods=["GET"])
def public_app_download(app_id):
    """Get and app package.

    :param app_id: Application ID
    :returns: App package file or 404 if app does not exist
    """
    app = AppEntry.query.get(app_id)
    if not app or not app.approved:
        return ("App not found", 404)
    app.downloads += 1
    db.session.commit()
    file_path = safe_join(current_app.instance_path, str(app.id) + ".tar.gz")
    return send_file(file_path, conditional=True)


@bp.route("/app/<app_id>/icon/private", methods=["GET"])
@login_required
def private_app_icon(app_id):
    """Get the icon of any app.

    :param app_id: AppEntry ID
    :returns: file contents of image - success, 400 - app does not exist,
    401 - bad permission

    only admins or the developer of the app have valid permissions
    """
    app = AppEntry.query.get(app_id)
    if not app:
        return ("App not found", 404)
    if g.user.id != app.dev_id and not g.user.admin:
        return ("Bad permissions", 401)
    file_path = safe_join(
        current_app.instance_path, str(app.id) + app.icon_ext)
    return send_file(file_path)


@bp.route("user/make_dev", methods=["GET", "POST"])
@login_required
def make_dev():
    """Make the user a developer.

    :returns: 204 - always succeeds
    """
    User.query.get(g.user.id).dev = True
    db.session.commit()
    return ("", 204)


@bp.route("user/<user_id>/private", methods=["GET"])
@admin_required
def private_user_info(user_id):
    """Get a user's private infomation as JSON.

    :returns: JSON of user - success, 400 - user does not exist,
    401 - bad permission
    """
    user = User.query.get(user_id)
    if not user:
        return ("user does not exist", 400)
    user_schema = UserSchema()
    return user_schema.jsonify(user)


@bp.route("user/<user_id>", methods=["GET"])
def public_user_info(user_id):
    """Get a JSON string of a user's public infomation.

    :returns: JSON of user - success, 400 - user does not exist
    """
    user = User.query.get(user_id)
    if not user:
        return ("user does not exist", 400)
    user_schema = UserPublicSchema()
    return user_schema.jsonify(user)


@bp.route("user/<user_id>/apps", methods=["GET"])
def public_user_apps(user_id):
    """Get a list of public App profiles belonging to user.

    :returns: JSON list of public app profiles
    """
    apps = AppEntry.query.filter_by(dev_id=user_id)
    name = User.query.get(user_id)
    app_schema = AppPublicSchema(many=True)
    output = []
    for app in apps:
        app.dev_name = name.username
        if app.approved:
            output.append(app)
    return app_schema.jsonify(output)


@bp.route("user/<user_id>/apps/private", methods=["GET"])
@login_required
def private_user_apps(user_id):
    """Get a list of private App profiles belonging to user.

    :returns: JSON list of private app profiles or 401 if bad permissions
    only admins and the developer have valid permissions
    """
    if int(user_id) != g.user.id and not g.user.admin:
        return ("bad permission", 401)
    apps = AppEntry.query.filter_by(dev_id=user_id)
    app_schema = AppSchema(many=True)
    return app_schema.jsonify(apps)


@bp.route("user/<user_id>/admin/promote", methods=["POST"])
@admin_required
def promote_admin(user_id):
    """Promote user to admin.

    :returns: 204 - success, 400 - user does not exist
    """
    try:
        User.query.get(user_id).admin = True
    except Exception as e:
        return ("User not found", 404)
    db.session.commit()
    return ("User promoted", 200)


@bp.route("user/<user_id>/admin/demote", methods=["POST"])
@admin_required
def demote_admin(user_id):
    """Demote user to admin.

    :returns: 204 - success, 400 - user does not exist
    """
    if int(user_id) == g.user.id or user_id == "1":
        return ("Cannot demote self", 401)
    try:
        User.query.get(user_id).admin = False
        db.session.commit()
    except Exception as e:
        return ("Database error", 500)
    return ("Success", 200)


@bp.route("user/<user_id>/delete", methods=["DELETE", "POST"])
@login_required
def delete_user(user_id):
    """Delete a user, requires admin or account ownership.

    :returns: 404 on user not found, 401 on bad permissions
    """
    user = User.query.get(user_id)
    if not user or user.id == 1:
        return ("User does not exist", 404)
    if user.id != g.user.id and not g.user.admin:
        return ("bad permission", 401)
    apps = AppEntry.query.filter_by(dev_id=user_id)
    for app in apps:
        os.remove(
            safe_join(current_app.instance_path, str(app.id) + ".tar.gz"))
        os.remove(
           safe_join(current_app.instance_path, str(app.id) + app.icon_ext))
        db.session.delete(app)
    if g.user.admin:
        send_email(user.email,
                   "Your account was deleted by an admin",
                   "We decided to delete your account. lol")
    db.session.delete(user)
    db.session.commit()
    return ("Success", 200)


@bp.route("user/<user_email>/password/reset", methods=["GET", "POST"])
def forgot_password(user_email):
    """Send a password reset link to the users email.

    :returns: 404 if no user has that email, or 200 if user exists.
    :limitations: no cooldown, so a user could be blocked from changing their
    password if this api is spammed
    """
    user = User.query.filter_by(email=user_email).one_or_none()
    if not user:
        return ("User does not exist", 404)
    user.reset_hash = random_hash256()
    db.session.commit()
    send_email(user_email,
               "FordApps password reset",
               f"""<a href=\"{request.url_root}
               password/{user.reset_hash}
               \"> click here to reset your password</a>""")
    return (res.text, 200)
