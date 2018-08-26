"""Developer mangement blueprint."""

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
    """Create a new app.

    :returns: New app added to the form and render templates
    """
    form = AppCreationForm()
    if form.validate_on_submit():
        imageFile = request.files["icon"]
        appFile = request.files["app"]
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
            checksum=hashlib.sha256(appFile.read()).hexdigest(),
            dev_id=g.user.id)
        db.session.add(app)
        db.session.commit()

        appPath = os.path.join(
            current_app.instance_path, str(app.id) + ".tar.gz")
        appFile.seek(0)
        appFile.save(appPath)
        imagePath = os.path.join(current_app.instance_path, str(app.id) + ext)
        imageFile.save(imagePath)
        return redirect(url_for("dev.dev_app_page", app_id=app.id))
    print(form.errors)
    return render_template("dev_app_new.html", form=form)


@bp.route("/app/<app_id>")
@login_required
def dev_app_page(app_id):
    """Developer status page.

    :raises 403: Wrong user access to the app.
    :raises 404: Not the right app
    :returns: Information of app metadata
    """
    app = AppEntry.query.get(int(app_id))
    if not app:
        return ("Non existant app", 404)
    if g.user.id != app.dev_id and not g.user.admin:
        return ("Invalid user", 403)
    return render_template("dev_app_view.html", app=app)


@bp.route("/")
@login_required
def dev_profile():
    """Developer's profile.

    :returns: Renders to new template of the developer user
    """
    apps = AppEntry.query.filter_by(dev_id=g.user.id)
    return render_template(
        "dev_app_list.html", apps=apps, username=g.user.username)
