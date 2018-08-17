from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),Email()])
    username = StringField("username", validators=[DataRequired(), Length(4)])
    password = PasswordField("password", validators=[DataRequired(), Length(6)])

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),Email()])
    password = PasswordField("password", validators=[DataRequired()])