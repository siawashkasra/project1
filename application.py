import os
import requests
from flask import jsonify

from flask import Flask, session, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, request
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm, ReviewForm
from controller import Controller





app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['JSON_SORT_KEYS'] = False
KEY = "dyzaWnHdIdb8VG2oGwSUcw"
URL = "https://www.goodreads.com/book"
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'\x11\x1d\\>\x1a3\x806N\xb1\x1fk=\xe39\xb5'
controller = Controller()


# Check for environment variable
if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")







@app.route("/")
def welcome():
    if "username" in session:
        return redirect(url_for('index'))
    return render_template("landing.html")

##########################################################################################
#Routes

#Register
@app.route("/register", methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            controller.save(form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.gender.data)
            return redirect(url_for("login"))

    return render_template("pages/register.html", form=form)


#Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            if controller.is_credentials_valid(form.user_name.data, form.password.data):
                controller.add_session(form.user_name.data)
                flash("You are successfully logged in.")
                return redirect(url_for('index'))
            render_template("pages/login.html", form=form, error="Wrong credentials!")
    return render_template("pages/login.html", form=form)


#Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for("welcome"))



#Index
@app.route("/index")
def index():
    if "username" in session:    
        if controller.user_searched():
            if controller.get_searched_book(controller.user_searched()):
                return render_template('index.html', books=controller.get_searched_book(controller.user_searched()), message={"success":controller.user_searched()})
            else:
                return render_template('index.html', books=controller.get_random_books(), message={"error":controller.user_searched()})
        return render_template('index.html', books=controller.get_random_books())
    return redirect(url_for("login"))



#Show
@app.route("/book/<int:id>", methods=['GET', 'POST'])
def show(id):
    form = ReviewForm()
    if "username" in session:
        if request.method=="POST":
            if form.validate_on_submit():
                controller.add_review(id, form.reviews.data, form.rating.data)
        book = controller.get_book_by_id(id)
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": f"{KEY}", "isbns": f"{book.isbn}"})
        ratings = res.json()["books"][0]
        return render_template('pages/book.html', book=book, ratings=ratings, form =form, reviews={"all_reviews": controller.get_reviews_by_id(book.id), "current_user_submitted": controller.is_review_submitted(book.id)})
    return redirect(url_for("login"))



#API
@app.route("/api")
def doc():
    return render_template('pages/api.html')

#API
@app.route("/api/<string:isbn>", methods=['GET'])
def api(isbn):    
    return jsonify(controller.get_book_by_isbn(isbn))
