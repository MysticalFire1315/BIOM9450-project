# Database Documentation

## Getting Started

1. Make sure PostgreSQL is installed.
2. Set `$PGPASSWORD` environment variable as the password for your `postgres` user.
3. Run `make all` to create the database (called `biom_project_test`), apply the
schema and load initial data.
4. To clean up the database, run `make clean`.

## Normalization

The provided SQL schema demonstrates a well-normalized database design, emphasizing
clarity, consistency, and reduced redundancy. Each entity is encapsulated in its own
table, adhering to principles of first, second, third and Boyce-Codd normal forms 
(1NF, 2NF, 3NF, BCNF). Shared attributes are abstracted into common tables, such as
the people table, which connects to specialized entities like `patients`, `oncologists`,
and `researchers` through unique foreign key relationships. Enum types (`sex` and
`ml_metric_type`) standardize categorical values, ensuring data integrity. Many-to-many
and hierarchical relationships are represented using join tables (e.g.,
`machine_learning_features`), and foreign key constraints enforce referential integrity.
The schema effectively supports complex domain-specific relationships while minimizing
data duplication.
