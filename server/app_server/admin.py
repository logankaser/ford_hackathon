"""Admin blueprint."""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app_server import db
from app_server.auth import admin_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@admin_required
def index():
<<<<<<< HEAD
    """Admin test.

    :returns: admin test
=======
    """
    Admin requisite

    :returns: admin requisite
>>>>>>> nothing changed
    """
    return "Admin test"
