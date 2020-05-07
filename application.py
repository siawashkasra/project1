import os
import requests

from flask import Flask, session, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, request
from flask_login import LoginManager, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm



app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)
csrf = CSRFProtect(app)
KEY = "dyzaWnHdIdb8VG2oGwSUcw"
URL = "https://www.goodreads.com/book"
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'\x11\x1d\\>\x1a3\x806N\xb1\x1fk=\xe39\xb5'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# # Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.route("/register", methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            save(form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.gender.data)
            return redirect(url_for("login"))

    return render_template("pages/register.html", form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            if is_credentials_valid(form.user_name.data, form.password.data):
                session["username"] = form.user_name.data
                flash("You are successfully logged in.")
                return redirect(url_for('index'))
            render_template("pages/login.html", form=form, error="Wrong credentials!")
    return render_template("pages/login.html", form=form)

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect(url_for("login"))


@app.route("/")
def index():
    if "username" in session:    
        print(session["username"])
    else:
        return redirect(url_for("login"))
    
    if user_searched():
        if get_searched_book(user_searched()):
            return render_template('index.html', books=get_searched_book(user_searched()), message={"success":user_searched()})
        else:
            return render_template('index.html', books=get_all_books(), message={"error":user_searched()})
    return render_template('index.html', books=get_all_books(), session=session["username"])




def get_searched_book(search):
    book = db.execute(f"select * from books where title ilike '%{search}%' or author ilike '%{search}%' or isbn ilike '%{search}%';").fetchall()
    if book:
        return book
    return False


@app.route("/book/<string:isbn>", methods=['GET', 'POST'])
def show(isbn):
    if request.method=="POST":
        store_review(isbn)

    book = db.execute("select * from books where isbn = :isbn", {"isbn": isbn}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": f"{KEY}", "isbns": f"{book.isbn}"})
    ratings = res.json()["books"][0]
    return render_template('pages/book.html', book=book, ratings=ratings)

def store_review(isbn):
    if request.form:
        review = request.form.get("review")
        ratings = request.form.get("ratings")

def get_all_books():
    books = db.execute("select * from books limit 9 offset 1").fetchall()
    return books

def user_searched():
    if request.args.get("search"):
        return request.args.get("search")
    return False

def save(first_name, last_name, email, password, gender):
    print(first_name)
    if first_name and last_name and email and password and gender:
        db.execute("insert into users (user_name, password) values(:user_name, :password)", {"user_name": email, "password": password})
        user = db.execute("select id from users where user_name= :user_name", {"user_name": email}).fetchone()
        db.execute("insert into profiles (first_name, last_name, gender, user_id) values(:first_name, :last_name, :gender, :user_id)",
                                            {
                                            "first_name": first_name, 
                                            "last_name": last_name, 
                                            "gender": gender, 
                                            "user_id": user.id})
        db.commit()


def is_credentials_valid(user_name, password):
    if user_name and password:
        credentials = db.execute("select id from users where user_name = :user_name and password = :password", 
                                                {"user_name": user_name, "password": password}).fetchone()
        if credentials:
            return True
    return False
