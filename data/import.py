import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import exc

class Import:
    # database engine object from SQLAlchemy that manages connections to the database
    # DATABASE_URL is an environment variable that indicates where the database lives
    engine = create_engine(os.getenv("DATABASE_URL")) 

    # create a 'scoped session' that ensures different users' interactions with the
    db = scoped_session(sessionmaker(bind=engine))

    #Initialize
    def __init__(self):
        print("Class initialized!")
        query1 = ("DROP TABLE IF EXISTS books")
        query2 = """CREATE TABLE books (
            id SERIAL PRIMARY KEY,
            isbn VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL, 
            author VARCHAR(255) NOT NULL, 
            year VARCHAR(255) NOT NULL
            );"""

        Import.db.execute(query1)
        Import.db.execute(query2)

    #Read the contents of the file
    #Populate the table with the contents
    def populate(self, file):
        print("Population started!")
        with open(file) as books_csv:
            books = csv.reader(books_csv)
            for isbn, title, author, year in books:
                if isbn=='isbn':
                    continue
                self.insert(isbn, title, author, year)
            
    #Insert into table
    def insert(self, isbn, title, author, year):
        print("Inserting...")
        try:
            Import.db.execute("INSERT INTO books (isbn, title, author, year) values (:isbn, :title, :author, :year)",
                 {"isbn": isbn, "title": title, "author": author, "year": year})

        except exc.SQLAlchemyError as e:
            print(e)


if __name__ == "__main__":
    impo = Import()
    impo.populate("books.csv")
    impo.db.commit()
