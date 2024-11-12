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
    date_of_birth DATE NOT NULL,
    sex sex NOT NULL
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    email varchar(255) UNIQUE NOT NULL,
    username varchar(255) UNIQUE NOT NULL,
    password_hash varchar(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    people_id integer UNIQUE,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE blacklist_tokens (
    id serial PRIMARY KEY,
    token varchar(500) NOT NULL,
    blacklisted_on TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    id serial PRIMARY KEY,
    photo bytea,
    address text,
    country varchar(50),
    emergency_contact_name varchar(50),
    emergency_contact_phone varchar(20),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

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

CREATE TABLE request_logs (
    id SERIAL PRIMARY KEY,
    time_accessed TIMESTAMPTZ DEFAULT NOW(),
    method varchar(10),
    url_path varchar(255),
    remote_addr varchar(45),
    agent varchar(255),
    status_code integer,

    user_id integer,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
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
