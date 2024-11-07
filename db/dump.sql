INSERT INTO people (firstname, lastname, date_of_birth, sex)
    VALUES ('John', 'Doe', '1985-04-15', 'male'),
    ('Jane', 'Smith', '1978-11-22', 'female'),
    ('Alex', 'Johnson', '1990-03-10', 'other'),
    ('Maria', 'Gonzalez', '1989-07-30', 'female'),
    ('Liam', 'Brown', '1995-12-05', 'male');

INSERT INTO oncologists (people_id)
    VALUES (1),
    (3);

INSERT INTO researchers (people_id)
    VALUES (2),
    (5);

