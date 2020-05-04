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
# engine = create_engine(os.getenv("postgres://uiefwmibakeakm:662c66f65687c9418a7011fe4ffc709b0574cc588a4a2b60518d6553d0e69491@ec2-50-17-21-170.compute-1.amazonaws.com:5432/d37pte45s6aeno"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    res = requests.get("https://www.goodreads.com/search/index.xml", params={"key": "dyzaWnHdIdb8VG2oGwSUcw"})
    print(res.json())
    return render_template('index.html')
