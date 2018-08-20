import functools
import os.path
import datetime
import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for, Response, current_app, send_file
)
from app_server import db
from app_server.models import AppEntry
from sqlalchemy import *
from app_server.auth import login_required
from app_server.forms import AppCreationForm

bp = Blueprint("dev", __name__, url_prefix="/dev")


@bp.route("/app/new", methods=["GET", "POST"])
@login_required
def new_app():
    form = AppCreationForm()
    if form.validate_on_submit():
        imageFile = request.files["icon"]
        print(type(imageFile))
        ext = os.path.splitext(imageFile.filename)[1]

        date = datetime.datetime.now()
        app = AppEntry(
            name=request.form["name"],
            description=request.form["description"],
            created=date,
            updated=date,
            downloads=0,
            icon_ext=ext,
            approved=False,
            checksum = hashlib.md5(imageFile.read()).hexdigest(),
            dev_id=g.user.id)
        db.session.add(app)
        db.session.commit()
        appPath = os.path.join(
            current_app.instance_path, str(app.id) + ".tar.gz")
        request.files["app"].save(appPath)
        imagePath = os.path.join(current_app.instance_path, str(app.id) + ext)
        imageFile.save(imagePath)
        flash("App succesfully created")
    print(form.errors)
    return render_template("new_app.html", form=form)


@bp.route("/app/<app_id>")
@login_required
def dev_app_page(app_id):
    app = None
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
    except Exception as e:
        return "non existant app"
    if (g.user.id != app.dev_id):
        return "invalid user"
    return render_template(
        "dev_app_page.html",
        name=app.name,
        description=app.description,
        created=str(app.created),
        updated=str(app.updated),
        downloads=str(app.downloads))


@bp.route("/app/<app_id>/delete", methods=["GET", "POST"])
@login_required
def delete_app(app_id):
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        if g.user.id != app.dev_id:
            return "400"
        os.remove(os.path.join(current_app.instance_path, app_id + ".tar.gz"))
        os.remove(os.path.join(current_app.instance_path, app_id + app.icon_ext))
        db.session.delete(app)
        db.session.commit()
    except Exception as e:
        return "400"
    return "200"

@bp.route("/app/<app_id>/icon", methods=["GET"])
@login_required
def app_icon(app_id):
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        if g.user.id != app.dev_id:
            return "400"
        return send_file(os.path.join(current_app.instance_path, str(app.id) + app.icon_ext))
    except:
        return "400"

@bp.route("/")
@login_required
def dev_profile():
    apps = db.session.query(AppEntry).filter_by(dev_id=g.user.id)
    return render_template("dev_profile.html", apps=apps, username=g.user.username)

'''
@bp.route("app/<app_id>/update", methods=["POST"])
>>>>>>> added picture upload and checksum
@login_required
def app_icon(app_id):
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        if g.user.id != app.dev_id:
            return "400"
        return send_file(os.path.join(current_app.instance_path, str(app.id) + app.icon_ext))
    except:
        return "400"

@bp.route("/")
@login_required
def dev_profile():
    apps = db.session.query(AppEntry).filter_by(dev_id=g.user.id)
    return render_template(
        "dev_profile.html", apps=apps)
