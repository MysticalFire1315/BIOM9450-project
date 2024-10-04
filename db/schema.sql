-- Database Design:
-- As a foundation, your database should have a minimum of these tables:
-- Mutation Variants Table: Contains details like mutation ID, gene involved, location, type, and potential impact.
-- Cancer Types Table: List of cancer types like breast cancer, lung cancer, etc.
-- Patient Table: Contains patient data including ID, name, photo, diagnosis, and associated mutations.
-- Researcher/Oncologist Table: Info about the professionals using the system, including their specialties.
DROP DATABASE IF EXISTS "BIOM9450_project";

CREATE DATABASE IF NOT EXISTS "BIOM9450_project";

USE "BIOM9450_project";

----------
-- Table structure for table "users"
----------

CREATE TABLE "users" (
  "id" INTEGER NOT NULL AUTO_INCREMENT,
  "username" VARCHAR(255),
  "password_hash" VARCHAR(255),
  "salt" VARCHAR(255),
  "created_at" TIMESTAMP,
  "role" ENUM('admin', 'researcher', 'oncologist'),
  PRIMARY KEY ("id")
);

----------
-- Table structure for table "People"
----------
DROP TABLE IF EXISTS "People";

CREATE TABLE "People" (
  "id" INTEGER NOT NULL AUTO_INCREMENT,
  "name" VARCHAR(255) NOT NULL,
  "age" INTEGER,
  PRIMARY KEY ("id")
);

----------
-- Table structure for table "Patients"
----------
DROP TABLE IF EXISTS "Patients";

CREATE TABLE "Patients" (
  "id" INTEGER NOT NULL AUTO_INCREMENT,
  "photo" LONGBLOB,
  "diagnosis" VARCHAR(255),
  "mutation_id" INTEGER,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("id") REFERENCES "People"("id"),
  FOREIGN KEY ("mutation_id") REFERENCES "Mutation_Variants"("id")
);