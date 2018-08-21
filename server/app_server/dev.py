import functools
import os.path
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for, Response, current_app
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
    '''
    New app with their metadata

    :returns: New app added to the form and render templates
    '''
    form = AppCreationForm()
    if form.validate_on_submit():
        date = datetime.datetime.now()
        app = AppEntry(
            name=request.form["name"],
            description=request.form["description"],
            created=date,
            updated=date,
            downloads=0,
            dev_id=g.user.id)
        db.session.add(app)
        db.session.commit()
        appPath = os.path.join(
            current_app.instance_path, str(app.id) + ".tar.gz")
        request.files["app"].save(appPath)
        flash("App succesfully created")
    print(form.errors)
    return render_template("new_app.html", form=form)


@bp.route("/app/<app_id>")
@login_required
def dev_app_page(app_id):
    '''
    Application ID

    :returns: Information of app metadata
    :raises Non Existant: If the app is not in the database, then is not uploaded
    :raises 400: Wrong user access to the app
    '''
    app = None
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
    except Exception as e:
        return "non existant app"
    if (g.user.id != app.dev_id):
        return "400"
    return render_template(
        "dev_app_page.html",
        name=app.name,
        description=app.description,
        created=str(app.created),
        updated=str(app.updated),
        downloads=str(app.downloads))


@bp.route("/app/<app_id>/delete", methods=["POST"])
@login_required
def delete_app(app_id):
    '''
    :param app_id: Application ID
    :type app_id: str.
    :returns: Successfully deleting the app from database
    :raises 400: Wrong user access to the app
    '''
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one
        if g.user.id != app.dev_id:
            return "400"
        os.remove(os.path.join(current_app.instance_path, app_id + ".tar.gz"))
        db.session.delete(app)
        db.session.commit()
    except Exception as e:
        return "400"
    return "200"


@bp.route("/")
@login_required
def dev_profile():
    '''
    Developer's profile
    
    :returns: Render's to new template of the developer user
    '''
    apps = db.session.query(AppEntry).filter_by(dev_id=g.user.id)
    return render_template(
        "dev_profile.html", apps=apps)
