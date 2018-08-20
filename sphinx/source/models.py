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


def public_fn_with_googley_docstring(name, state=None):
    """This function does something. This is an example, no worries

    Args:
       name (str):  The name to use.

    Kwargs:
       state (bool): Current state to be in.

    Returns:
       int.  The return code::

          0 -- Success!
          1 -- No good.
          2 -- Try again.

    Raises:
       AttributeError, KeyError

    A really great idea.  A way you might use me is

    >>> print public_fn_with_googley_docstring(name='foo', state=None)
    0

    BTW, this always returns 0.  **NEVER** use with :class:`MyPublicClass`.

    """
    return 0

def hash_password(plain_text):
	"""
	This is a test #9000
	returns decoded hash (I need an example here)::
		(test here)

	"""
