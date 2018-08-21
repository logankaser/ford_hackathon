from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(4)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(6)])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Continue")


class AppCreationForm(FlaskForm):
    name = StringField("App Title", validators=[DataRequired()])
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(max=1000)])
    app = FileField("Upload App Package", validators=[FileRequired()])
    submit = SubmitField("Submit App")
