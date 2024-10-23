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
  "id" serial PRIMARY KEY,
  "email" varchar(255) UNIQUE NOT NULL,
  "username" varchar(255) UNIQUE NOT NULL,
  "password_hash" varchar(255) NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table blacklist_tokens (
  token varchar(500) unique not null,
  blacklisted_on timestamp default current_timestamp
);



