"""Database models."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AppInstallation(db.Model):
    """Stores information about an installation."""

    __tablename__ = "app_installation"
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer)
    name = db.Column(db.String(50), nullable=False)
    checksum = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
