"""Routes for controling the local machine.

For example, install and uninstall pakages,
or query what packages are currently installed.
"""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint("local", __name__)


@bp.route("/list")
def list_installed_apps():
    """List installed apps."""
    return "None"
