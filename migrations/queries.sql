
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
CREATE TABLE books (

                    id SERIAL PRIMARY KEY,
                    isbn VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL, 
                    author VARCHAR(255) NOT NULL, 
                    year VARCHAR(255) NOT NULL
);
CREATE TABLE users (

                    id SERIAL PRIMARY KEY,
                    user_name VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                                
);

CREATE TABLE profiles (

                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(255) NOT NULL,
                        last_name VARCHAR(255) NOT NULL,
                        gender VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL, 
                        password VARCHAR(255) NOT NULL,
                        user_id INTEGER REFERENCES users

);
CREATE TABLE reviews (

                        id SERIAL PRIMARY KEY,
                        review VARCHAR(255) NOT NULL,
                        rate VARCHAR(255) NOT NULL,
                        book_id INTEGER REFERENCES books,
                        user_id INTEGER REFERENCES users

);