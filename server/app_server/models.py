from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_msearch import Search
from flask_marshmallow import Marshmallow
from flask import current_app, jsonify
from datetime import datetime, timedelta
import jwt

db = SQLAlchemy()
bcrypt = Bcrypt()
search = Search()
ma = Marshmallow()


def hash_password(plain_text):
    hashed = bcrypt.generate_password_hash(
        plain_text, current_app.config.get('BCRYPT_LOG_ROUNDS')
    )
    return hashed.decode()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    dev = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, password, dev=False, admin=False):
        """
        Create a new user
        :returns: A new user
        """
        self.username = username
        self.email = email
        self.password_hash = hash_password(password)
        self.created = datetime.now()
        self.admin = admin
        self.dev = dev

    def get_token(self, user_id):
        """
        Generates an API auth token
        :returns: string
        """
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1),
                "iat": datetime.utcnow(),
                "sub": self.id
            }
            return jwt.encode(
                payload,
                app.config.get("SECRET_KEY"),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def check_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :returns: User|none
        """
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"))
            return payload["sub"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None


class AppEntry(db.Model):
    __tablename__ = "app_entry"
    __searchable__ = ["name", "description"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)
    downloads = db.Column(db.Integer, nullable=False)
    icon_ext = db.Column(db.String(), nullable=False)
    approved = db.Column(db.Boolean, nullable=False)
    checksum = db.Column(db.String(), nullable=True)
    dev_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class AppSchema(ma.ModelSchema):
    class Meta:
        model = AppEntry



