# Makefile for setting up the database

# Ensure PGPASSWORD has been set as an environment variable
# export PGPASSWORD='postgres'

# Change this
DB_NAME = biom_project_test
DB_USER = postgres
DB_HOST = localhost

# Files
SCHEMA_FILE = schema.sql
DUMP_FILE = dump.sql
VIEWS_FILE = views.sql

# Default target
all: createdb apply_schema apply_views load_data

# Create the database
createdb:
	psql -h $(DB_HOST) -U $(DB_USER) -c "DROP DATABASE IF EXISTS $(DB_NAME);"
	psql -h $(DB_HOST) -U $(DB_USER) -c "CREATE DATABASE $(DB_NAME);"

# Apply schema
apply_schema: $(SCHEMA_FILE)
	psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -f $(SCHEMA_FILE)

# Apply views
apply_views: $(VIEWS_FILE)
	psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -f $(VIEWS_FILE)

# Load initial data
load_data: $(DUMP_FILE)
	psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -f $(DUMP_FILE)

# Clean up database
clean:
	psql -h $(DB_HOST) -U $(DB_USER) -c "DROP DATABASE IF EXISTS $(DB_NAME);"

# .PHONY target to avoid issues with files named like targets
.PHONY: all createdb apply_schema apply_functions apply_triggers load_data clean
