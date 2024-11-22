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
    emergency_contact_phone varchar(32),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    people_id integer UNIQUE NOT NULL,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE oncologists (
    id serial PRIMARY KEY,
    specialization varchar(255),
    phone varchar(32),
    email varchar(100),

    people_id integer UNIQUE NOT NULL,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE oncologist_affiliations (
    id serial PRIMARY KEY,
    hospital varchar(255),

    oncologist_id integer NOT NULL,
    CONSTRAINT fk_oncologist FOREIGN KEY (oncologist_id) REFERENCES oncologists (id)
);

CREATE TABLE researchers (
    id serial PRIMARY KEY,

    people_id integer UNIQUE NOT NULL,
    CONSTRAINT fk_people FOREIGN KEY (people_id) REFERENCES people (id)
);

CREATE TABLE request_logs (
    id serial PRIMARY KEY,
    time_accessed TIMESTAMPTZ DEFAULT NOW(),
    method varchar(10),
    url_path varchar(255),
    remote_addr varchar(45),
    agent varchar(255),
    status_code integer,

    user_id integer,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE machine_learning_model (
    id SERIAL PRIMARY KEY,
    name varchar(64),
    time_created TIMESTAMPTZ DEFAULT NOW(),
    last_updated TIMESTAMPTZ DEFAULT NOW()

);

CREATE TABLE machine_learning_features (
    id SERIAL PRIMARY KEY,
    feat_name varchar(32),
    omics integer,
    imp double precision,

    model_id integer,
    CONSTRAINT fk_model FOREIGN KEY (model_id) REFERENCES machine_learning_model (id)
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
