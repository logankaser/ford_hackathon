from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileRequired

class RegisterForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),Email()])
    username = StringField("username", validators=[DataRequired(), Length(4)])
    password = PasswordField("password", validators=[DataRequired(), Length(6)])

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),Email()])
    password = PasswordField("password", validators=[DataRequired()])

class AppCreationForm(FlaskForm):
    name = StringField("App Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=1000)])
    app = FileField("Upload", validators=[FileRequired()])