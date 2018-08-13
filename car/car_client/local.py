import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint("local", __name__)


@bp.route("/list")
def list_installed_apps():
    return "None"
