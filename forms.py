from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, RadioField, TextAreaField, SelectField
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
    submit = SubmitField('Login')
    

    def validate_username(self, field):
        if field is None:
            raise ValidationError("Please provide a username!")

    def validate_password(self, field):
        if field is None:
            raise ValidationError("Please provide a password!")


class ReviewForm(FlaskForm):
    reviews = TextAreaField('Review', [DataRequired()], render_kw={"placeholder": "Please write a review", "rows": 4})
    rating = RadioField('Rating', choices = [(5,'5'),(4,'4'),(3,'3'),(2,'2'),(1,'1')], coerce=int) 
    submit = SubmitField('Leave a review')


    def validate_rating(self, field):
        if field.data is None:
            raise ValidationError("Please provide a rating!")

    def validate_reviews(self, field):
        if len(field.data) < 50:
            raise ValidationError("Review must not be less than 50 characters!")