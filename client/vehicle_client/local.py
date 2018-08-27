"""Routes for controling the local machine.

For example, install and uninstall pakages,
or query what packages are currently installed.
"""

import functools
import requests
import shutil
import os
import subprocess
import datetime
import json
from hashlib import sha256
from vehicle_client.models import db, AppInstallation

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for, current_app, safe_join
)

bp = Blueprint("local", __name__)


@bp.route("/list")
def list_installed_apps():
    """List installed apps.

    :return: None
    """
    return "None"


@bp.route("/install_app/<app_id>", methods=["POST"])
def install_app(app_id):
    """Install an app.

    :returns: Success- App installed
    :returns: 500 - Checksum not found; failed to fetch app package; unmatched checksum
    :returns: 500 - Failed to fetch app package
    :returns: 500 - Unmatched checksum
    :returns: 500 - Error unpacking app package
    """
    app_json = requests.get(
        current_app.config.get("API_DOMAIN") + "/api/v1/app/" + app_id).json()
    checksum = app_json.get("checksum")
    if not checksum:
        return ("App checksum not found.", 500)
    app_pkg = requests.get(
        current_app.config.get("API_DOMAIN") + "/api/v1/app/"
        + app_id + "/download", stream=True)
    if app_pkg.status_code != 200:
        return ("Failed to fetch app package", 500)
    save_path = safe_join(
        current_app.instance_path, checksum + ".pkg")
    with open(save_path, "wb") as f:
        app_pkg.raw.decode_contant = True
        shutil.copyfileobj(app_pkg.raw, f)
    with open(save_path, "rb") as f:
        actual_checksum = sha256(f.read()).hexdigest()
    if actual_checksum != checksum:
        os.remove(save_path)
        return ("App checksum did not match", 500)
    try:
        shutil.unpack_archive(
            save_path,
            safe_join(current_app.instance_path, checksum),
            format="tar"
        )
    except Exception as e:
        os.remove(save_path)
        return ("Error unpacking app package", 500)
    os.remove(save_path)
    if not AppInstallation.query.filter_by(checksum=checksum).count():
        app_install = AppInstallation(
            app_id=app_json.get("id"),
            name=app_json.get("name"),
            created=datetime.datetime.now(),
            checksum=checksum
        )
        db.session.add(app_install)
        db.session.commit()
    from time import sleep
    sleep(2)
    return (actual_checksum + " Installed", 200)


@bp.route("/run_app/<app_id>")#, methods=["POST"])
def run_app(app_id):
    """Run an installed app.

    :returns: Success - Execute app
    :returns: 400 - App not installed
    """
    app_install = AppInstallation.query.filter_by(app_id=app_id).one_or_none()
    if not app_install:
        return ("App not installed", 400)
    app_path = safe_join(current_app.instance_path, app_install.checksum)
    with open(safe_join(app_path, "app.json"), "r") as f:
        raw_json = f.read()
    app_meta = json.loads(raw_json)
    app_type = app_meta.get("type", "console")
    if app_type == "console":
        process = subprocess.Popen(
            [safe_join(app_path, "app/" + app_meta.get("executable", "app"))],
            stdout=subprocess.PIPE, shell=True)
        result = process.communicate()[0]
        print(result.decode("ascii"))
    elif app_type == "gui":
        subprocess.call(
            [safe_join(app_path, "app/" + app_meta.get("executable", "app"))])
    return (result, 200)
