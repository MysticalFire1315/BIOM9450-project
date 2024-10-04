-- Database Design:
-- As a foundation, your database should have a minimum of these tables:
-- Mutation Variants Table: Contains details like mutation ID, gene involved, location, type, and potential impact.
-- Cancer Types Table: List of cancer types like breast cancer, lung cancer, etc.
-- Patient Table: Contains patient data including ID, name, photo, diagnosis, and associated mutations.
-- Researcher/Oncologist Table: Info about the professionals using the system, including their specialties.
----------
-- Table structure for table "users"
----------
DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR(255),
  "password_hash" VARCHAR(255),
  "salt" VARCHAR(255),
  "created_at" TIMESTAMP DEFAULT current_timestamp
);

-- ----------
-- -- Table structure for table "People"
-- ----------
-- DROP TABLE IF EXISTS "People";

-- CREATE TABLE "People" (
--   "id" SERIAL,
--   "name" VARCHAR(255) NOT NULL,
--   "age" INTEGER,
--   PRIMARY KEY ("id")
-- );

-- ----------
-- -- Table structure for table "Patients"
-- ----------
-- DROP TABLE IF EXISTS "Patients";

-- CREATE TABLE "Patients" (
--   "id" SERIAL,
--   "photo" BYTEA,
--   "diagnosis" VARCHAR(255),
--   "mutation_id" INTEGER,
--   PRIMARY KEY ("id"),
--   FOREIGN KEY ("id") REFERENCES "People"("id") -- FOREIGN KEY ("mutation_id") REFERENCES "Mutation_Variants"("id")
-- );