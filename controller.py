import os
import requests

from flask import Flask, session, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, request
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm, ReviewForm


class Controller():

    def __init__(self):
        
        #Set up database
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.db = scoped_session(sessionmaker(bind=self.engine))
    


    #Session Management###################################################################
    #Store Session
    def add_session(self, user_name):
        user = self.db.execute("select id from users where user_name = :user_name", 
                                            {"user_name": user_name}).fetchone()
        if user:
            session["username"] = user_name
            session["user_id"] = user.id
        return False



    #Books Model############################################################################
    #Return the book searched by a user
    def get_searched_book(self, search):
        book = self.db.execute(f"select * from books where title ilike '%{search}%' or author ilike '%{search}%' or isbn ilike '%{search}%';").fetchall()
        if book:
            return book
        return False



    #Return list of all books
    def get_all_books(self):
        books = self.db.execute("select * from books limit 9 offset 1").fetchall()
        return books



    #Return a book by an ID
    def get_book_by_id(self, id):
        book = self.db.execute("select * from books where id = :id", {"id": id}).fetchone()
        return book
    #######################################################################################
   
   
   
    #Reviews Model#########################################################################
    #Add a review for a book
    def add_review(self, book_id):
        form = ReviewForm()
        if form.validate_on_submit():
            review = form.reviews.data
            print(review)
            self.db.execute("insert into reviews (review, rate, user_id, book_id, create_date) values (:review, :rate, :user_id, :book_id, :create_date)", 
                                            {"review": review, "rate": "This is rate", "user_id": session["user_id"], "book_id": book_id, "create_date": "now()"})
            self.db.commit()



    #Return list of all reviews for a book
    def get_reviews_by_id(self, book_id):
        reviews = self.db.execute("select concat(first_name, ' ', last_name) as full_name, user_name, review, date_trunc('second', create_date) as create_date from users u join profiles p on p.user_id = u.id join reviews r on r.user_id = u.id where book_id = :book_id order by create_date desc;", 
                                                    {"book_id": book_id}).fetchall()
        return reviews



    #Check if user submitted a review
    def is_review_submitted(self, book_id):
        review = self.db.execute("select id from reviews where user_id = :user_id and book_id = :book_id", 
                                            {"user_id": session["user_id"], "book_id": book_id}).fetchone()
        print(review)
        if review:
            return False
        return True


    #######################################################################################
   


    #Users Model###########################################################################
    #Sign up a user
    def save(self, first_name, last_name, email, password, gender):
        print(first_name)
        if first_name and last_name and email and password and gender:
            self.db.execute("insert into users (user_name, password) values(:user_name, :password)", {"user_name": email, "password": password})
            user = self.db.execute("select id from users where user_name= :user_name", {"user_name": email}).fetchone()
            self.db.execute("insert into profiles (first_name, last_name, gender, user_id) values(:first_name, :last_name, :gender, :user_id)",
                                                {
                                                "first_name": first_name, 
                                                "last_name": last_name, 
                                                "gender": gender, 
                                                "user_id": user.id})
            self.db.commit()



    #Check if user provided correct credentials
    def is_credentials_valid(self, user_name, password):
        if user_name and password:
            credentials = self.db.execute("select id from users where user_name = :user_name and password = :password", 
                                                    {"user_name": user_name, "password": password}).fetchone()
            if credentials:
                return True
        return False


    #######################################################################################



    #Util##################################################################################
    #Check if user tried to search
    def user_searched(self):
        if request.args.get("search"):
            return request.args.get("search")
        return False