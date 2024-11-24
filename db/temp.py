import psycopg2
from psycopg2.extras import execute_values

l1 = ['a', 'b', 'c']
l2 = ['d', 'e', 'f']
l3 = ['a', 'g', 'h']

db = psycopg2.connect(dbname="biom_project_test")
with db.cursor() as cur:
    cur.execute("CREATE TABLE keys (id SERIAL PRIMARY KEY, name varchar(64) UNIQUE NOT NULL);")
    print("Table created!")
    for l in [l1, l2, l3]:
        execute_values(cur, "INSERT INTO keys (name) VALUES %s;", l)
        print(f"Inserted {l}")

    cur.execute("SELECT * FROM keys;")
    print(cur.fetchall())
