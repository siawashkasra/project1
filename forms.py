from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL
import email_validator

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [Email(message='Not a valid email address!'), DataRequired()])
    password = PasswordField('Password', [DataRequired(message="Please enter a password.")])
    confirm_password = PasswordField('Repeat Password', [EqualTo('password', message='Passwords must match!')])
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])  
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_name = StringField('User Name', [Email(message='Not a valid email address!'), DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Submit')