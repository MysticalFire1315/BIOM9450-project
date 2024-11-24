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

CREATE TYPE ml_metric_type AS ENUM (
    'training',
    'testing'
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
    time_accessed TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    method varchar(10) NOT NULL,
    url_path varchar(255) NOT NULL,
    remote_addr varchar(45) NOT NULL,
    agent varchar(255) NOT NULL,
    status_code integer NOT NULL,

    user_id integer,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE machine_learning_models (
    id SERIAL PRIMARY KEY,
    name varchar(64),
    time_created TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    num_epoch_pretrain integer NOT NULL,
    num_epoch integer NOT NULL,
    lr_e_pretrain double precision NOT NULL,
    lr_e double precision NOT NULL,
    lr_c double precision NOT NULL,
    num_classes integer NOT NULL
);

CREATE TABLE machine_learning_performance (
    id SERIAL PRIMARY KEY,
    metric_type ml_metric_type NOT NULL,
    epoch integer NOT NULL,
    acc double precision NOT NULL,
    f1_weighted double precision NOT NULL,
    f1_macro double precision NOT NULL,
    auc double precision NOT NULL,
    precision_val double precision NOT NULL,
    loss double precision NOT NULL,

    model_id integer NOT NULL,
    CONSTRAINT fk_model FOREIGN KEY (model_id) REFERENCES machine_learning_models (id)
);

CREATE TABLE features (
    id SERIAL PRIMARY KEY,
    name varchar(64) UNIQUE NOT NULL
);

CREATE TABLE machine_learning_features (
    id SERIAL PRIMARY KEY,
    feat_id integer NOT NULL,
    omics integer NOT NULL,
    imp double precision NOT NULL,
    feedback text,

    CONSTRAINT fk_feature FOREIGN KEY (feat_id) REFERENCES features (id),
    model_id integer NOT NULL,
    CONSTRAINT fk_model FOREIGN KEY (model_id) REFERENCES machine_learning_models (id)
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
