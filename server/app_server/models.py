"""App Server database models."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask import current_app, jsonify
from datetime import datetime, timedelta
from marshmallow import fields, Schema
from time import mktime
import jwt

db = SQLAlchemy()
bcrypt = Bcrypt()
search = Search()
ma = Marshmallow()


def hash_password(plain_text):
    """Hashes a password.

    :param plain_text: The password to be hashed
    :returns: Password hash
    """
    hashed = bcrypt.generate_password_hash(
        plain_text, current_app.config.get('BCRYPT_LOG_ROUNDS')
    )
    return hashed.decode()


class JsTime(fields.Field):
    """Converts a python datetime to a javascript datetime."""

    def _serialize(self, value, attr, obj):
        if value is None:
            return ""
        return mktime(value.timetuple()) * 1000


class User(db.Model):
    """User class representing a developer or admin."""

    __tablename__ = "user"
    __searchable__ = ["id", "username", "email"]
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    dev = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    reset_hash = db.Column(db.String(64), nullable=False, default="")

    def __init__(self, email, username, password, dev=False, admin=False,
                 reset_hash=""):
        """Create a new user.

        :returns: A new user
        """
        self.username = username
        self.email = email
        self.password_hash = hash_password(password)
        self.created = datetime.now()
        self.admin = admin
        self.dev = dev
        self.reset_hash = reset_hash

    def get_token(self):
        """Get a new API token.

        :returns: Token String
        """
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1),
                "iat": datetime.utcnow(),
                "sub": self.id
            }
            return jwt.encode(
                payload,
                current_app.config.get("SECRET_KEY"),
                algorithm="HS256"
            )
        except Exception as e:
            return None

    @staticmethod
    def check_token(auth_token):
        """Check if a token is valid.

        :param auth_token: auth token string to be checked
        :returns: User|None
        """
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get("SECRET_KEY"))
            return payload["sub"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None


class UserSchema(ma.ModelSchema):
    """Serialize a User to JSON."""

    created = JsTime()
    updated = JsTime()

    class Meta:
        model = User


class UserPublicSchema(ma.ModelSchema):
    """Serialize public UserSchema info to JSON."""

    created = JsTime()
    updated = JsTime()

    class Meta:
        """This is a test.""""
    fields = (
        "username",
        "created",
        "dev",
        "admin")


class AppEntry(db.Model):
    """Stores information about an app."""

    __tablename__ = "app_entry"
    __searchable__ = ["id", "name", "description"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)
    downloads = db.Column(db.Integer, nullable=False)
    icon_ext = db.Column(db.String(), nullable=False)
    approved = db.Column(db.Boolean, nullable=False)
    checksum = db.Column(db.String(64), nullable=True)
    dev_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class AppSchema(ma.ModelSchema):
    """Serialize an AppEntry to json."""

    created = JsTime()
    updated = JsTime()

    class Meta:
        """All fields."""

        model = AppEntry


class AppPublicSchema(ma.ModelSchema):
    """Serialize public AppEntry info to JSON."""

    created = JsTime()
    updated = JsTime()

    class Meta:
        """Public fields."""

        fields = (
            "id",
            "name",
            "checksum",
            "description",
            "created",
            "updated",
            "dev_name")
