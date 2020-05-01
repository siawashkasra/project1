import os
from sqlalchemy import exc

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



class Schema:
    # database engine object from SQLAlchemy that manages connections to the database
    # DATABASE_URL is an environment variable that indicates where the database lives
    engine = create_engine(os.getenv("DATABASE_URL")) 

    # create a 'scoped session' that ensures different users' interactions with the
    db = scoped_session(sessionmaker(bind=engine))



    #Reads from a file and returns its contents
    def read_file(self, file):
        with open(file) as queries_sql:
            queries = queries_sql.read()
        return queries


    #Executes a query
    def execute(self, queries):
        try:
            Schema.db.execute(queries)
            self.success()
        except exc.SQLAlchemyError as e:
            self.error()
            print(e)

    #Prints success information to users
    def success(self):
        print("Migration was executed successfully!")
    

    #Prints error information to users
    def error(self):
        print("Migrations was not executed successfully!")



if __name__ == "__main__":
    sch = Schema()
    sch.execute(sch.read_file("queries.sql")) 
    Schema.db.commit()