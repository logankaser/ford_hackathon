from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
