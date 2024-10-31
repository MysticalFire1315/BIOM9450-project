-- Database Design:
-- As a foundation, your database should have a minimum of these tables:
-- Mutation Variants Table: Contains details like mutation ID, gene involved, location, type, and potential impact.
-- Cancer Types Table: List of cancer types like breast cancer, lung cancer, etc.
-- Patient Table: Contains patient data including ID, name, photo, diagnosis, and associated mutations.
-- Researcher/Oncologist Table: Info about the professionals using the system, including their specialties.

----------
-- Types
----------

CREATE TYPE sex as ENUM ('male', 'female', 'other');
CREATE TYPE person_role as ENUM ('patient', 'oncologist', 'researcher');

----------
-- Tables
----------

CREATE TABLE people (
    id serial PRIMARY KEY,
    firstname varchar(100) NOT NULL,
    lastname varchar(100) NOT NULL,
    date_of_birth TIMESTAMP NOT NULL,
    sex sex NOT NULL,
    person_role person_role NOT NULL
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    email varchar(255) UNIQUE NOT NULL,
    username varchar(255) UNIQUE NOT NULL,
    password_hash varchar(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    person_id INTEGER UNIQUE,
    CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES people(id)
);

CREATE TABLE blacklist_tokens (
    id serial PRIMARY KEY,
    token varchar(500) NOT NULL,
    blacklisted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    id serial PRIMARY KEY,
    photo BYTEA,
    address TEXT,
    country VARCHAR(50),
    emergency_contact_name VARCHAR(50),
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    person_id INTEGER UNIQUE,
    CONSTRAINT fk_person FOREIGN KEY (person_id) REFERENCES people(id)
);