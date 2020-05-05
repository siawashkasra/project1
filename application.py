import os
import requests

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, request

app = Flask(__name__)
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


@app.route("/")
def index():
    books = []
    message = "message"
    books = db.execute("select * from books limit 9 offset 1").fetchall()
    search = request.args.get("search")
    if search:
        res = db.execute(f"select * from books where title ilike '%{search}%' or author ilike '%{search}%' or isbn ilike '%{search}%';").fetchall()
        if res:
            return render_template('index.html', books=res, message={"success":search})
        else:
            return render_template('index.html', books=res, message={"error":search})
    return render_template('index.html', books=books, message=message)

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
