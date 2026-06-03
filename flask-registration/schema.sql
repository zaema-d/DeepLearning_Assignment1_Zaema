DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY ,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    photo1 BLOB,
    photo2 BLOB
);
