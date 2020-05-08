from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, ValidationError
import email_validator
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

class RegistrationForm(FlaskForm):
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [Email(message='Not a valid email address!'), DataRequired()])
    password = PasswordField('Password', [DataRequired(message="Please enter a password.")])
    confirm_password = PasswordField('Repeat Password', [EqualTo('password', message='Passwords must match!')])
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])  
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

    def validate_email(self, field):
        email = RegistrationForm.db.execute("select user_name from users where user_name= :user_name",  {"user_name": field.data}).fetchone()
        if email:
            raise ValidationError("Email is already in use!")


class LoginForm(FlaskForm):
    user_name = StringField('User Name', [Email(message='Not a valid email address!'), DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Submit')
    



class ReviewForm(FlaskForm):
    reviews = TextAreaField('Review', [DataRequired()], render_kw={"placeholder": "Please enter your review"})
    submit = SubmitField('Leave a review')
