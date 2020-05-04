import os
import requests

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template

app = Flask(__name__)

KEY = "dyzaWnHdIdb8VG2oGwSUcw"
URL = "https://www.goodreads.com/book"
# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # # Configure session to use filesystem
# # app.config["SESSION_PERMANENT"] = False
# # app.config["SESSION_TYPE"] = "filesystem"
# # Session(app)

# # Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "dyzaWnHdIdb8VG2oGwSUcw", "isbns": "9781632168146"})
    print(res.json()["books"][0]["id"])
    book_id = res.json()["books"][0]["isbn"]

    books = db.execute("select * from books limit 10").fetchall()
    # for book in books:
    #     print(books)
    return render_template('index.html', books=books)
