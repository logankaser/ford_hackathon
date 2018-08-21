"""
.. module:: models
   :platform: OSX, Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Logan Walton <lolwalton@huehue.lol>

Libraries::

	from flask_sqlalchemy import SQLAlchemy
	from flask_bcrypt import Bcrypt
	from flask import current_app
	from datetime import datetime, timedelta
	import jwt

Global variables::

	db = SQLAlchemy()
	bcrypt = Bcrypt()

"""

def hash_password(plain_text):
	"""
	Hashes the given string from the parameter

	:param plain_text: something something
	:type plain_text: str.

	:returns: hashed.decode()

	As you see, we will need to use our :func:: hash_password to encode and secure passwords
	
	"""

class User(object):
	"""
	This is a public class with the user database's methods::

		__init__(self, email, username, password, dev=False, admin=False)
		get_token(self, user_id)
		check_token(auth_token)

	"""

	def __init__(self, email, username, password, dev=False, admin=False):
		"""
		Create a new registered user

		:param email: user's email
		:type email: str.

		:param username: user's login name
		:type username: str.

		:param password: user's password
		:type password: str.

		:param dev: flag state if user is developer
		:type dev: bool.

		:param admin: flag state if user is admin
		:type admin: bool.

		Class details::

			self.username = username
			self.email = email
			self.password_hash = hash_password(password)
			self.created = datetime.now()
			self.admin = admin
			self.dev = dev

		"""

	def get_token(self, user_id):
		"""
		Generates an API auth token

		:returns: string -- the return code

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

		:param auth_token: secret key
		:type auth_token: str.

		:returns: User|none

		"""

class AppEntry(object):
	"""
	Class with the app details::

		__tablename__ = "app_entry"
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String(50), nullable=False)
		description = db.Column(db.String(1000), nullable=False)
		created = db.Column(db.DateTime, nullable=False)
		updated = db.Column(db.DateTime, nullable=False)
		downloads = db.Column(db.Integer, nullable=False)
		dev_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

	"""
