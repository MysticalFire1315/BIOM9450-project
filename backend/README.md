# Backend Documentation

## Getting Started

1. Ensure that Python is installed.
2. Install dependencies with `make install`.
3. Start the server with `make run`. It will be hosted at `http://127.0.0.1:5000/`.
4. Optionally, use `make all` to clean, install and run.

## Route Permissions Breakdown

Listed in database. Access using:

```sql
select * from routes;
```

## User Accounts

- Created through `POST /auth/register`, which returns an authorization token used for future
requests.
- Must be linked to an individual in the database through `POST /user/link` before access to
protected routes is granted.
- Can check currently logged in profile with `GET /user/profile`, which shows whether the user
is linked.

## Person Roles

- `Oncologist` and `Researcher`
  - Can only be created by database admins since these individuals can access sensitive
information.
  - Information about individual is public (login not required to see detailed information).
  - Has the ability to view detailed information about all individuals with role `Patient`.
  - Can upload mutation info related to any `Patient`.
  - Can use Machine Learning features (see `/ml` routes).
  - Can view all mutation data.
- `Patient`
  - Can be created by any user with the role `Oncologist` or `Researcher`.
  - Information about individual can only be seen by themselves or any `Oncologist`/`Researcher`.

## Sample Workflows

### Oncologist/Researcher workflow

1. Register user account with `POST /auth/register`, saving `Authorization` field in response.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "test@example.com",
  "password": "Passw0rd",
  "username": "TestUser1"
}'

# Response (Code 201)
{
  "status": "success",
  "message": "Successfully registered.",
  "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM"
}
```

2. Link user account to Oncologist in database with `POST /user/link`.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/user/link' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM' \
  -H 'Content-Type: application/json' \
  -d '{
  "person_id": 1
}'

# Response (Code 201)
{
  "status": "success",
  "message": "Successfully linked",
  "role": "oncologist"
}
```

3. Create a patient with `POST /patient/create`. Note here `photo` field in request should
be a byte string.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/patient/create' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM' \
  -H 'Content-Type: application/json' \
  -d '{
  "photo": "<byte string here>",
  "address": "13 Tuckwell Ave, Macquarie Park",
  "country": "Australia",
  "emergency_contact_name": "John Smith",
  "emergency_contact_phone": "0123456789",
  "person": {
    "firstname": "Bob",
    "lastname": "Smith",
    "date_of_birth": "2004-11-25",
    "sex": "male"
  }
}'

# Response (Code 201)
{
  "status": "success",
  "message": "Successfully created",
  "id": 6
}
```

4. View summary of all patients in the database with `GET /patient/list`.

```bash
# Request
curl -X 'GET' \
  'http://127.0.0.1:5000/patient/list' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM'

# Response (Code 200)
{
  "data": [
    {
      "id": 6,
      "firstname": "Bob",
      "lastname": "Smith",
      "date_of_birth": "2004-11-25",
      "sex": "Sex.MALE"
    }
  ]
}
```

5. View detailed information about patient with `id=6` using `GET /patient/profile/<id>`.

```bash
# Request
curl -X 'GET' \
  'http://127.0.0.1:5000/patient/profile/6' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM'

# Response (Code 200)
{
  "data": {
    "photo": "<memory at 0x7f745d273580>",
    "address": "13 Tuckwell Ave, Macquarie Park",
    "country": "Australia",
    "emergency_contact_name": "John Smith",
    "emergency_contact_phone": "0123456789",
    "person": {
      "id": 6,
      "firstname": "Bob",
      "lastname": "Smith",
      "date_of_birth": "2004-11-25",
      "sex": "Sex.MALE"
    }
  }
}
```

6. View detailed Oncologist profile about self with `GET /oncologist/profile`.

```bash
# Request
curl -X 'GET' \
  'http://127.0.0.1:5000/oncologist/profile' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM'

# Response (Code 200)
{
  "data": {
    "specialization": "Medical Oncology",
    "phone": "+61 400 111 111",
    "email": "alice.smith@example.com",
    "affiliations": [
      "Royal Melbourne Hospital",
      "St Vincent's Hospital Sydney"
    ],
    "person": {
      "id": 1,
      "firstname": "John",
      "lastname": "Doe",
      "date_of_birth": "1985-04-15",
      "sex": "Sex.MALE"
    }
  }
}
```

7. Train a ROSMAP (Alzheimer's Disease) model using default learning parameters with `POST /ml/train`.
Response `id` corresponds to the id of the model being trained, while `estimated_time` is how long
the server thinks it will take to train the model in seconds.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/ml/train' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "ROSMAP",
  "num_epoch_pretrain": 500,
  "num_epoch": 500
}'

# Response (Code 202)
{
  "status": "success",
  "id": 3,
  "estimated_time": 720
}
```

8. After waiting the estimated time, retrieve information about the model with `GET ml/model/<id>`.

```bash
# Request
curl -X 'GET' \
  'http://127.0.0.1:5000/ml/model/3' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM'

# Response (Code 200)
{
  "data": {
    "name": "ROSMAP",
    "time_created": "2024-11-26T10:51:40.020859+11:00",
    "features": [
      {
        "feat_name": "hsa-miR-132",
        "omics": 2,
        "imp": 58.90909090909089
      },
      {
        "feat_name": "hsa-miR-129-5p",
        "omics": 2,
        "imp": 55.11961722488037
      },
      {
        "feat_name": "hsa-miR-146b-5p",
        "omics": 2,
        "imp": 51.42857142857142
      },
      {
        "feat_name": "cg04126866",
        "omics": 1,
        "imp": 46.233766233766225
      },
      ...
    ],
    "num_epoch_pretrain": 500,
    "num_epoch": 500,
    "lr_e_pretrain": 0.001,
    "lr_e": 0.0005,
    "lr_c": 0.001
  }
}
```

9. Determine probability of someone getting Alzheimer's Disease by supplying
expression levels of each gene and model id to `POST /ml/probability`.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/ml/probability' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_id": 1,
  "hsa-miR-132": 99,
  "hsa-miR-129-5p": 77,
  "hsa-miR-146b-5p": 55,
  "cg04126866": 12,
  "cg08367223": 42,
  "cg19485804": 63,
  "hsa-miR-2114": 51,
  "hsa-miR-129-3p": 47,
  "cg18149207": 0,
  "hsa-miR-24": 53,
  "hsa-miR-143": 81,
  "cg03894103": 15,
  "hsa-miR-660": 72,
  "hsa-miR-185": 13,
  "cg13468685": 36,
  "cg08952029": 9,
  "cg01182697": 85,
  "hsa-miR-1308": 27,
  "cg15789095": 61,
  "cg20793071": 58,
  "ENSG00000105419.11": 91,
  "hsa-miR-448": 90,
  "hsa-miR-432": 8,
  "cg24192663": 57,
  "cg12556134": 95,
  "cg00754253": 75,
  "ENSG00000174607.6": 94,
  "ENSG00000165175.11": 30,
  "hsa-miR-130b": 16,
  "cg15775914": 3
}'

# Response (Code 200)
{
  "status": "success",
  "probability": 0.5123235309675355
}
```

10. View training metrics for ROSMAP model at every 50 epoch intervals with `POST /ml/metrics`.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/ml/metrics' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_id": 3,
  "metric_type": "training",
  "interval": 50
}'

# Response (Code 200)
[
  {
    "epoch": 0,
    "acc": 0.4816326530612245,
    "f1_weighted": 0.313127565075617,
    "f1_macro": 0.325068870523416,
    "auc": 0.3794875216869078,
    "precision_val": 0.24081632653061225,
    "loss": 0.9400287121534348
  },
  {
    "epoch": 50,
    "acc": 0.5224489795918368,
    "f1_weighted": 0.46867863792935094,
    "f1_macro": 0.47450915690480117,
    "auc": 0.6822367543040171,
    "precision_val": 0.5580619629127093,
    "loss": 0.8727030605077744
  },
  {
    "epoch": 100,
    "acc": 0.8734693877551021,
    "f1_weighted": 0.8735115583002685,
    "f1_macro": 0.8734356513189688,
    "auc": 0.9504203923662085,
    "precision_val": 0.8735505797680927,
    "loss": 0.8159472048282623
  },
  ...
]
```

11. Provide some feedback on the relevance of different features returned by the trained model
with `POST /ml/feedback`.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/ml/feedback' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM' \
  -H 'Content-Type: application/json' \
  -d '{
  "model_id": 3,
  "data": [
    {
      "feature": "hsa-miR-132",
      "feedback": "Great"
    },
    {
      "feature": "hsa-miR-129-5p",
      "feedback": "Inaccurate"
    }
  ]
}'

# Response (Code 201)
{
  "status": "success",
  "message": "Your feedback has been saved!"
}
```

12. See all mutations in the database with `GET /mutations/list`.

```bash
# Request
curl -X 'GET' \
  'http://127.0.0.1:5000/mutations/list' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM'

# Response (Code 200)
[
  "hsa-miR-132",
  "hsa-miR-129-5p",
  "hsa-miR-146b-5p",
  "cg04126866",
  "cg08367223",
  "cg19485804",
  "hsa-miR-2114",
  "hsa-miR-129-3p",
  "cg18149207",
  "hsa-miR-24",
  "hsa-miR-143",
  "cg03894103",
  "hsa-miR-660",
  "hsa-miR-185",
  "cg13468685",
  ...
]
```

13. Link patient to mutations by uploading a VCF file to `POST /patient/mutation/upload`.

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:5000/patient/mutation/upload' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@complex.vcf;type=text/x-vcard' \
  -F 'people_id=6'

# Response (Code 201)
{
  "status": "success",
  "genes": [
    "TP53",
    "BRCA1",
    "EGFR"
  ]
}
```

14. See more info about the gene called "TP53" from COSMIC database, along with any
patients linked to this mutation using `GET /mutations/<name>`.

```bash
# Request
curl -X 'GET' \
  'http://127.0.0.1:5000/mutations/TP53' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzI2NjEzNTMsImlhdCI6MTczMjU3NDk0OCwic3ViIjoiMiJ9.Nz1V3XFzMxY1QBlvlTcQP7iWtTUAQipzSWnEk2uKPFM'

# Response (Code 200)
{
  "COSMIC_data": [
    {
      "mutation_id": "22964589",
      "gene_name": "TP53",
      "primary_site": "skin"
    },
    {
      "mutation_id": "23085261",
      "gene_name": "TP53",
      "primary_site": "ovary"
    },
    {
      "mutation_id": "50910723",
      "gene_name": "TP53",
      "primary_site": "ovary"
    },
    {
      "mutation_id": "51191564",
      "gene_name": "TP53",
      "primary_site": "haematopoietic_and_lymphoid_tissue"
    },
    {
      "mutation_id": "59976813",
      "gene_name": "TP53",
      "primary_site": "skin"
    },
    {
      "mutation_id": "60592752",
      "gene_name": "TP53",
      "primary_site": "ovary"
    },
    {
      "mutation_id": "60733244",
      "gene_name": "TP53",
      "primary_site": "ovary"
    }
  ],
  "patients": [
    6
  ]
}
```
