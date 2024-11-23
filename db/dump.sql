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

INSERT INTO machine_learning_models (name)
    VALUES ('BCRA'),
    ('ROSMAP');

INSERT INTO machine_learning_features (feat_name, omics, imp, model_id)
VALUES
    -- BCRA
    ('SOX11|6664', 0, 38.258362838147875, 1),
    ('AMY1A|276', 0, 33.001920373967764, 1),
    ('UGT8|7368', 0, 31.123536706376022, 1),
    ('SLC6A2|6530', 0, 30.78399864345971, 1),
    ('SLC6A15|55117', 0, 26.46499185865736, 1),
    ('SOX21', 1, 25.44051626083954, 1),
    ('CDH26', 1, 25.44051626083954, 1),
    ('ROPN1', 1, 25.44051626083954, 1),
    ('ATP10B', 1, 25.44051626083954, 1),
    ('MIR563', 1, 25.44051626083954, 1),
    ('OR1J4', 1, 25.44051626083954, 1),
    ('ANKRD45|339416', 0, 24.706767251228445, 1),
    ('FABP7|2173', 0, 24.585353471772265, 1),
    ('FGFBP1|9982', 0, 24.585353471772265, 1),
    ('hsa-mir-9-1', 2, 21.53650971031739, 1),
    ('TMEM207', 1, 21.04044402700833, 1),
    ('GPR37L1', 1, 20.99338574284704, 1),
    ('IL12RB2|3595', 0, 20.982852158969333, 1),
    ('hsa-mir-9-2', 2, 20.84610632315726, 1),
    ('SLC6A14|11254', 0, 20.120216862506425, 1),
    ('hsa-mir-204', 2, 18.571714568370897, 1),
    ('COL11A2|1302', 0, 18.4825916401139, 1),
    ('CAPN13|92291', 0, 18.4825916401139, 1),
    ('SLC43A3|29015', 0, 18.4825916401139, 1),
    ('PHGDH|26227', 0, 18.4825916401139, 1),
    ('PSAT1|29968', 0, 18.4825916401139, 1),
    ('FLJ41941', 1, 18.209243670607055, 1),
    ('DSG1|1828', 0, 18.159989430294065, 1),
    ('hsa-mir-205', 2, 17.588734910487243, 1),
    ('MDGA2|161357', 0, 15.294878830052205, 1),
    -- ROSMAP
    ('SOX11|6664', 0, 38.258362838147875, 2),
    ('AMY1A|276', 0, 33.001920373967764, 2),
    ('UGT8|7368', 0, 31.123536706376022, 2),
    ('SLC6A2|6530', 0, 30.78399864345971, 2),
    ('SLC6A15|55117', 0, 26.46499185865736, 2),
    ('SOX21', 1, 25.44051626083954, 2),
    ('CDH26', 1, 25.44051626083954, 2),
    ('ROPN1', 1, 25.44051626083954, 2),
    ('ATP10B', 1, 25.44051626083954, 2),
    ('MIR563', 1, 25.44051626083954, 2),
    ('OR1J4', 1, 25.44051626083954, 2),
    ('ANKRD45|339416', 0, 24.706767251228445, 2),
    ('FABP7|2173', 0, 24.585353471772265, 2),
    ('FGFBP1|9982', 0, 24.585353471772265, 2),
    ('hsa-mir-9-1', 2, 21.53650971031739, 2),
    ('TMEM207', 1, 21.04044402700833, 2),
    ('GPR37L1', 1, 20.99338574284704, 2),
    ('IL12RB2|3595', 0, 20.982852158969333, 2),
    ('hsa-mir-9-2', 2, 20.84610632315726, 2),
    ('SLC6A14|11254', 0, 20.120216862506425, 2),
    ('hsa-mir-204', 2, 18.571714568370897, 2),
    ('COL11A2|1302', 0, 18.4825916401139, 2),
    ('CAPN13|92291', 0, 18.4825916401139, 2),
    ('SLC43A3|29015', 0, 18.4825916401139, 2),
    ('PHGDH|26227', 0, 18.4825916401139, 2),
    ('PSAT1|29968', 0, 18.4825916401139, 2),
    ('FLJ41941', 1, 18.209243670607055, 2),
    ('DSG1|1828', 0, 18.159989430294065, 2),
    ('hsa-mir-205', 2, 17.588734910487243, 2),
    ('MDGA2|161357', 0, 15.294878830052205, 2);


INSERT INTO routes (uri, method, patient, oncologist, researcher, no_role, everyone)
    VALUES ('/auth/register', 'POST', false, false, false, false, true),
    ('/auth/login', 'POST', false, false, false, false, true),
    ('/auth/logout', 'POST', true, true, true, true, false),

    -- /user routes
    ('/user/link', 'GET', true, true, true, true, false),
    ('/user/link', 'POST', false, false, false, true, false),
    ('/user/profile', 'GET', true, true, true, true, false),
    ('/user/history/<n>', 'GET', true, true, true, true, false),

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
