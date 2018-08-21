import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    Response
)
from app_server import db, bcrypt
from app_server.models import User, hash_password
from app_server.forms import RegisterForm, LoginForm

bp = Blueprint("auth", __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not g.user.admin:
            flash("Not authorized, must be admin")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@bp.route("/register", methods=["GET", "POST"])
def register():
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
        flash("New user created")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
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
        flash(user.username + " Logged in")
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/get_token", methods=["POST"])
def get_token():
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
