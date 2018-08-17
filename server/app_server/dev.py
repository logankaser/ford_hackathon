import functools
import os.path

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for, Response, current_app
)
from app_server import db
from app_server.models import AppEntry
from sqlalchemy import *

bp = Blueprint("dev", __name__, url_prefix="/dev")


@bp.route("/app/new", methods=["GET", "POST"])
def new_app():
    if request.method == "GET":
        return render_template("new_app.html")
    appName = request.form["name"]
    dev_id = session["user_id"]
    app = AppEntry(name=appName, dev_id=dev_id)
    db.session.add(app)
    db.session.commit()
    appPath = os.path.join(current_app.instance_path, str(app.id) + ".tar.gz")
    if "app" not in request.files:
        flash("no file given", "error")
        return render_template("new_app.html")
    file = request.files["app"]
    if file.filename == "":
        flash("no file given", "error")
        return render_template("new_app.html")
    file.save(appPath)
    flash("app succesfully created", "success")
    return render_template("new_app.html")


@bp.route("app/<app_id>/delete", methods=["POST"])
def delete_app(app_id):
    # get app object from table
    # check if dev id matches session user id
    # remove entry from table
    # delete app file
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        os.remove(os.path.join(current_app.instance_path, app_id + ".ford_app"))
        db.session.delete(app)
        db.session.commit()
    except:
        return "400"
    return "200"
'''
@bp.route("app/<app_id>/modify", methods=("POST"))
def modify_app(app_id):
    # get app object from table
    # check if dev id matches session user id
    # replace app file with request.form["app"]
    try:
        app = db.session.query(AppEntry).filter_by(id=app_id).one()
        appfile = open(flask_app.instance_path + app_id + ".ford_app", "w")
        appfile.write(request.form["app"])
    except:
        return "400"
    return "200"
'''