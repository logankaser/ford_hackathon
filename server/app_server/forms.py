"""Form validation classes."""

from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import (
    StringField, PasswordField, TextAreaField, SubmitField, BooleanField
)
=======
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
>>>>>>> added tos form
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    """Register Form."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(4)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(6)])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    """Login Form."""

    identity = StringField("identity", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Continue")


class AppCreationForm(FlaskForm):
    """Application Creation Form."""

    name = StringField("App Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired(),
                                Length(max=1000)])
    app = FileField("Upload App Package", validators=[FileRequired()])
    icon = FileField("App Icon", validators=[FileRequired()])
    submit = SubmitField("Submit App")


class AdminSearchForm(FlaskForm):
    """Admin Search Form."""

<<<<<<< HEAD
    search = StringField("", validators=[])
    submit = SubmitField("Search")


class ChangePasswordForm(FlaskForm):
    """Password Change Form."""

    oldPassword = PasswordField("Old Password", validators=[DataRequired()])
    newPassword1 = PasswordField(
        "New Password", validators=[DataRequired(), Length(6)])
    newPassword2 = PasswordField(
        "Confirm New Password", validators=[DataRequired(), Length(6)])
    submit = SubmitField("Change Password")


class ResetPasswordForm(FlaskForm):
    """Password Reset Form."""

    newPassword1 = PasswordField(
        "New Password", validators=[DataRequired(), Length(6)])
    newPassword2 = PasswordField(
        "Confirm New Password", validators=[DataRequired(), Length(6)])
    submit = SubmitField("Set Password")


class DevTOSForm(FlaskForm):
    """Dev TOS acceptance form."""

    submit = SubmitField("I agree to the Terms of Service")
=======
    search = StringField("", validators=[DataRequired()])
    submit = SubmitField("Search")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> edit for linter pycodestyle
=======
=======
>>>>>>> edit for linter pycodestyle
=======
>>>>>>> server


class DevTOSForm(FlaskForm):
    """Dev TOS acceptance form"""

<<<<<<< HEAD
<<<<<<< HEAD
    accept = BooleanField("I Accept Developer TOS")
    sumbit = SubmitField("")
>>>>>>> added tos form
=======
    submit = SubmitField("I agree to the Terms of Service")
<<<<<<< HEAD
>>>>>>> added tos page
=======
    submit = SubmitField("I agree to the Terms of Service")
=======
>>>>>>> edit for linter pycodestyle
>>>>>>> edit for linter pycodestyle
=======
>>>>>>> server
