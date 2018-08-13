import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    return "Admin test"
