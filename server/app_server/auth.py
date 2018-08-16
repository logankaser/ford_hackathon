import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app_server import db, bcrypt
from app_server.models import User, hash_password

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        new_user = User(email, username, password)
        db.session.add(new_user)
        db.session.commit()
        flash("New user created")
    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).one_or_none()
        if not bcrypt.check_password_hash(user.password_hash, password):
            flash("Login failed")
            return redirect(url_for("auth.login"))
        session["user_id"] = user.id
        flash(user.username + " Logged in")
    return render_template("login.html")
