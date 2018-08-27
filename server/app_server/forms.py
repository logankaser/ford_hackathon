"""Form validation classes."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
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

    email = StringField("email", validators=[DataRequired(), Email()])
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
