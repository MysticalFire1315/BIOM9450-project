INSERT INTO people (firstname, lastname, date_of_birth, sex)
    VALUES ('John', 'Doe', '1985-04-15', 'male'),
    ('Jane', 'Smith', '1978-11-22', 'female'),
    ('Alex', 'Johnson', '1990-03-10', 'other'),
    ('Maria', 'Gonzalez', '1989-07-30', 'female'),
    ('Liam', 'Brown', '1995-12-05', 'male');

INSERT INTO oncologists (specialization, phone, email, people_id)
    VALUES ('Medical Oncology', '+61 400 111 111', 'alice.smith@example.com', 1),
    ('Radiation Oncology', '+61 400 222 222', 'bob.jones@example.com', 2),
    ('Pediatric Oncology', '+61 400 333 333', 'carol.taylor@example.com', 3);

INSERT INTO oncologist_affiliations (hospital, oncologist_id) 
    VALUES ('Royal Melbourne Hospital', 1),
    ('St Vincent''s Hospital Sydney', 1),
    ('Peter MacCallum Cancer Centre', 2),
    ('Royal Children''s Hospital', 3),
    ('Sydney Children''s Hospital', 3);

INSERT INTO researchers (people_id)
    VALUES (2),
    (5);

INSERT INTO routes (uri, method, patient, oncologist, researcher, no_role, everyone)
    VALUES ('/auth/register', 'POST', false, false, false, false, true),
    ('/auth/login', 'POST', false, false, false, false, true),
    ('/auth/logout', 'POST', true, true, true, true, false),

    -- /user routes
    ('/user/link', 'GET', true, true, true, true, false),
    ('/user/link', 'POST', false, false, false, true, false),
    ('/user/profile', 'GET', true, true, true, true, false),

    -- /patient routes
    ('/patient/create', 'POST', false, true, true, false, false),
    ('/patient/profile', 'GET', true, false, false, false, false),
    ('/patient/profile/<id>', 'GET', false, true, true, false, false),
    ('/patient/list', 'GET', false, true, true, false, false),

    -- /oncologist routes
    ('/oncologist/profile', 'GET', false, true, false, false, false),
    ('/oncologist/profile/<id>', 'GET', true, true, true, true, true),
    ('/oncologist/list', 'GET', true, true, true, true, true),

    -- /researcher routes
    ('/researcher/profile', 'GET', false, false, true, false, false),
    ('/researcher/profile/<id>', 'GET', true, true, true, true, true),
    ('/researcher/list', 'GET', true, true, true, true, true);
