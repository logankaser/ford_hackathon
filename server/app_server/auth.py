"""Authentication Blueprint.

Supports session and token based authentication.
"""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    Response
)
from app_server import db, bcrypt
from app_server.models import User, hash_password
from app_server.forms import RegisterForm, LoginForm, ChangePasswordForm
from secrets import randbelow

bp = Blueprint("auth", __name__)


@bp.before_app_request
def load_logged_in_user():
    """Load user model if user is logged in."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def login_required(view):
    """Require a logged in user.

    :param view: view to wrap
    :returns: wrapped view
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


def dev_required(view):
    """Require a logged in dev user.

    :param view: view to wrap
    :returns: wrapped view
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not (g.user.dev or g.user.admin):
            flash("Not authorized, must be dev or admin")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    """Require a logged in admin user.

    :param view: view to wrap
    :returns: wrapped view
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.admin:
            flash("Not authorized, must be admin")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Registration form.

    :returns: Registered user form data or False on failure
    """
    form = RegisterForm()
    if form.validate_on_submit():
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        error = None
        if password != password_again:
            flash("Password does not match Password Again")
            error = True
        if User.query.filter_by(email=email).first():
            flash("Email already in use")
            error = True
        if error is not None:
            return redirect(url_for("auth.register"))
        new_user = User(email, username, password)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Login with session based authentication.

    :returns: On success redircts to home, otherwise back to the login page.
    """
    if g.user:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).one_or_none()
        if not user or not bcrypt.check_password_hash(
                user.password_hash, password):
            flash("Login failed")
            return redirect(url_for("auth.login"))
        session["user_id"] = user.id
        g.user = User.query.get(user.id)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    """Clear session and logout.

    :returns: Redirect to login screen
    """
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/get_token", methods=["POST"])
def get_token():
    """Get a new auth token (JWT).

    :returns: Token or HTTP status code 401 on error.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).one_or_none()
    if user and password and bcrypt.check_password_hash(
            user.password_hash, password):
        return user.get_token()
    return Response(
        "Invalid credentials",
        401,
        {"WWWAuthenticate":
            "Basic realm=\"email and password must be present and valid\""}
    )


def random_hash64():
    hex_string = "0123456789abcdef"
    output = ""
    for _ in range (16):
        output += hex_string[randbelow(16)]
    return output


@bp.route("/password/<reset_hash>", methods=["GET"])
def reset_forgotten_password(reset_hash):
    if len(reset_hash) != 64:
        return ("Page not found", 404)
    user = User.query.filter_by(reset_hash=reset_hash).one_or_none()
    if not user:
        return ("Page not found", 404)
    user.reset_hash = ""
    newPassword = random_hash64()
    user.password = hash_password(newPassword)
    db.session.commit()
    return ("your new password is: " + newPassword, 200)


@bp.route("/password/change", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if request.form["newPassword1"] != request.form["newPassword2"]:
            flash("Your passwords must match")
        elif hash_password(request.form["oldPassword"]) == g.user.password_hash:
            User.query.get(g.user.id).password_hash = hash_password(request.form["newPassword1"])
            db.session.commit()
            flash("Password succesfully changed")
        else:
            flash("Old password incorrect")
    return render_template("password_change.html", form=form)




