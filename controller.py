import os
import requests, random

from flask import Flask, session, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, request
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm, ReviewForm
from werkzeug.security import generate_password_hash, check_password_hash



class Controller():

    def __init__(self):
        
        #Set up database
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.db = scoped_session(sessionmaker(bind=self.engine))
    


    #Session Management###################################################################
    #Store Session
    def add_session(self, user_name):
        try:
            user = self.db.execute("select id from users where user_name = :user_name", 
                                  {"user_name": user_name}).fetchone()
            if user:
                session["username"] = user_name
                session["user_id"] = user.id

        except Exception as e:
            self.db.close()

        else:    
            return False



    #Books Model############################################################################
    #Return the book searched by a user
    def get_searched_book(self, search):
        try:
            book = self.db.execute(f"select * from books where title ilike '%{search}%' or author ilike '%{search}%' or isbn ilike '%{search}%';").fetchall()
            
            if book:
                return book
        
        except Exception as e:
            self.db.close()

        else:
            return False



    #Return list of 9 random books
    def get_random_books(self):
        try:
            books = self.db.execute("select * from books where id in :random_ids;", 
                                   {"random_ids": tuple(random.sample([x for x in range(1, 5000)], 9))}).fetchall()
            
            return books

        except Exception as e:
            self.db.close()



    #Return a book by an ID
    def get_book_by_id(self, id):
        try:
            book = self.db.execute("select * from books where id = :id", {"id": id}).fetchone()
            if book:
                return book

        except Exception as e:
            self.db.close()

        else:
            return False
        
    #######################################################################################
   
   
   
    #Reviews Model#########################################################################
    #Add a review for a book
    def add_review(self, book_id, review, rating):

        try:
            self.db.execute("insert into reviews (text, rating, user_id, book_id, create_date) values (:text, :rating, :user_id, :book_id, :create_date)", 
            {"text": review, "rating": rating, "user_id": session["user_id"], "book_id": book_id, "create_date": "now()"})

            self.db.commit()
        except Exception as e:
            self.db.rollback()

        else:
            self.db.close()
        



    #Return list of all reviews for a book
    def get_reviews_by_id(self, book_id):
        try:
            reviews = self.db.execute("select concat(first_name, ' ', last_name) as full_name, user_name, text, rating, date_trunc('second', create_date) as create_date from users u join profiles p on p.user_id = u.id join reviews r on r.user_id = u.id where book_id = :book_id order by create_date desc;", 
                                     {"book_id": book_id}).fetchall()
            return reviews

        except Exception as e:
            self.db.close()


    #Check if user submitted a review
    def is_review_submitted(self, book_id):
        try:
            review = self.db.execute("select id from reviews where user_id = :user_id and book_id = :book_id", 
                                            {"user_id": session["user_id"], "book_id": book_id}).fetchone()
            if review:
                return False

        except Exception as e:
            self.db.close()
        
        else:
            return True


    #######################################################################################
   


    #Users Model###########################################################################
    #Sign up a user
    def save(self, first_name, last_name, email, password, gender):
        if first_name and last_name and email and password and gender:

            try:
                self.db.execute("insert into users (user_name, password) values(:user_name, :password)", {"user_name": email, "password": generate_password_hash(password, 'sha256')})
                user = self.db.execute("select id from users where user_name= :user_name", {"user_name": email}).fetchone()
                self.db.execute("insert into profiles (first_name, last_name, gender, user_id) values(:first_name, :last_name, :gender, :user_id)",
                                                {
                                                "first_name": first_name, 
                                                "last_name": last_name, 
                                                "gender": gender, 
                                                "user_id": user.id})
                self.db.commit()

            except Exception as e:                                    
                self.db.rollback()
            
            else:
                self.db.close()



    #Check if user provided correct credentials
    def is_credentials_valid(self, user_name, password):
        if user_name and password:

            try:
                credentials = self.db.execute("select user_name, password from users where user_name = :user_name",
                                                        {"user_name": user_name}).fetchone()
                if credentials:
                    if credentials[0] == user_name and check_password_hash(credentials [1], password):
                        return True

            except Exception as e:
                self.db.close()
                
        return False


    #######################################################################################



    #Util##################################################################################
    #Check if user tried to search
    def user_searched(self):
        if request.args.get("search"):
            return request.args.get("search")
        return False

    #API###################################################################################
    #Return book info
    def get_book_by_isbn(self, isbn):
        try:
            book = self.db.execute("select title, author, year, isbn, count(text) as review_count, CAST(COALESCE(trunc(avg(rating), 1), 0) as varchar) as average_score from books b left join reviews r on r.book_id = b.id where isbn = :isbn group by title, author, year, isbn;",
                                                                {"isbn": isbn}).fetchone()
            if book:
                return dict(book)

        except Exception as e:
            self.db.close()

        else:
            return "No books match those ISBNs."