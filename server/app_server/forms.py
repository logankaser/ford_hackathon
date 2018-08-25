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

    search = StringField("", validators=[DataRequired()])
    submit = SubmitField("Search")