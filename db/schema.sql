-- Database Design:
-- As a foundation, your database should have a minimum of these tables:
-- Mutation Variants Table: Contains details like mutation ID, gene involved, location, type, and potential impact.
-- Cancer Types Table: List of cancer types like breast cancer, lung cancer, etc.
-- Patient Table: Contains patient data including ID, name, photo, diagnosis, and associated mutations.
-- Researcher/Oncologist Table: Info about the professionals using the system, including their specialties.

----------
-- Types
----------

CREATE TYPE sex AS ENUM (
    'male',
    'female',
    'other'
);

----------
-- Tables
----------

CREATE TABLE people (
    id serial PRIMARY KEY,
    firstname varchar(100) NOT NULL,
    lastname varchar(100) NOT NULL,
    date_of_birth TIMESTAMP NOT NULL,
    sex sex NOT NULL
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    email varchar(255) UNIQUE NOT NULL,
    username varchar(255) UNIQUE NOT NULL,
    password_hash varchar(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    people_id integer UNIQUE,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE blacklist_tokens (
    id serial PRIMARY KEY,
    token varchar(500) NOT NULL,
    blacklisted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    id serial PRIMARY KEY,
    photo bytea,
    address text,
    country varchar(50),
    emergency_contact_name varchar(50),
    emergency_contact_phone varchar(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    people_id integer UNIQUE NOT NULL,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE oncologists (
    id serial PRIMARY KEY,

    people_id integer UNIQUE NOT NULL,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE researchers (
    id serial PRIMARY KEY,

    people_id integer UNIQUE NOT NULL,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE logs (
    id serial PRIMARY KEY,
    user_id integer UNIQUE NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id),

    route varchar(255),
    time_accessed TIMESTAMP,
    data_id integer
);



-------------------------------------
-- For documentation purposes only --
-------------------------------------

CREATE TYPE http_method AS ENUM (
    'GET',
    'POST'
);

CREATE TABLE routes (
    uri varchar(255) NOT NULL,
    method http_method NOT NULL,
    patient boolean,
    oncologist boolean,
    researcher boolean,
    no_role boolean,
    everyone boolean
);
