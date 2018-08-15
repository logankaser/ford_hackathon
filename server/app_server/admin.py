import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app_server import db
from app_server.models import Test

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    t = Test(name="An example")
    db.session.add(t)
    db.session.commit()
    return "Admin test"
