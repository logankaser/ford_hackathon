"""Database models."""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema
from time import mktime

db = SQLAlchemy()
ma = Marshmallow()


class AppInstallation(db.Model):
    """Stores information about an installation."""

    __tablename__ = "app_installation"
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer)
    name = db.Column(db.String(50), nullable=False)
    checksum = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime, nullable=False)


class JsTime(fields.Field):
    """Converts a python datetime to a javascript datetime."""

    def _serialize(self, value, attr, obj):
        if value is None:
            return ""
        return mktime(value.timetuple()) * 1000


class AppInstallationSchema(ma.ModelSchema):
    """Serialize a AppInstallation to JSON."""

    created = JsTime()

    class Meta:
        """Use all fields."""

        model = AppInstallation
