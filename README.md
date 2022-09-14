
<h1 align='center'>
  <br>
  <a href='https://github.com/pyccy/'><img src='https://i.imgur.com/NfWkZje.jpg' width=500 weigth=500 alt='YaMDb'></a>
  <br>
  YaMDb REST API
  <br>
</h1>
<h4 align='center'>Review database platform API</h4>
<p align='center'>
    <img src='https://img.shields.io/badge/Python-3.10.0-blue?style=flat&logo=python&logoColor=white'>
    <img src='https://img.shields.io/badge/Django-2.2.16-blue?style=flat&logo=Django&logoColor=white'>
    <img src='https://img.shields.io/badge/Django_REST_Framework-3.12.4-blue?style=flat&logo=Django&logoColor=white'>
    <img src='https://img.shields.io/badge/Simple_JWT-5.2.0-blue?style=flat&logo=JSON-Web-Tokens&logoColor=white'>
    <img src='https://img.shields.io/badge/SQLite3-2.6.0-blue?style=flat&logo=SQLite&logoColor=white'>
</p>

---
## What is YaMDb REST API?
YaMDb is an open source review database API with Django Rest Framework
 
## How to Install & Setup YaMDb API?
1. Clone this repository:
```
git clone git@github.com:pyccy/api_yamdb.git
```
2. Cd into api_yamdb:
```
cd api_yamdb
```
3. Create virtual environment: 
```
python -m venv venv
```
4. Acivate venv:
```
source venv/bin/activate
```
5. Install all dependencies from the requirements: 
```
pip install -r requirements.txt
```
6. Migrate Database:
```
python manage.py migrate
```
7. Load Test Data
```
python manage.py csv_load
```
## .env
create .env file and fill it 
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=yourloggin
POSTGRES_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=5432
SECRET_KEY=yoursecretkey
```
## How to Dockerfile and container?
1. Cd into api_yamdb
```
cd api_yamdb
```
2. Build Docker image
```
docker build -t yamdb .  
```
3. Cd into /infra
```
cd ../infra
```
4. Build container
```
docker-compose up
```
5. Make migrations
```
docker-compose exec web python manage.py migrate
```
6. Make superuser
```
docker-compose exec web python manage.py createsuperuser
```
7. Make static
```
docker-compose exec web python manage.py collectstatic --no-input
```
8. Make fixture
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
## How to Run YaMDb API?
```
python manage.py runserver
```
Navigate to the site in your local rest client: http://127.0.0.1:8000
 
## Available endpoints
 
| Endpoint | User | Moderator | Admin | Description |
|---|---|---|---|------------|
| /api/v1/categories/ | GET | GET | GET, POST, PUT, PATCH, DELETE | Categories |
| /api/v1/genres/ | GET | GET | GET, POST, PUT, PATCH, DELETE | Genres     |
| /api/v1/titles/ | GET | GET | GET, POST, PUT, PATCH, DELETE | Titles     |
| /api/v1/titles/{title_id}/reviews/ | GET, POST, PUT, PATCH, DELETE  | GET, POST, PUT, PATCH, DELETE | GET, POST, PUT, PATCH, DELETE | Reviews    |
| /api/v1/titles/{title_id}/reviews/{review_id}/comments/ | GET, POST, PUT, PATCH, DELETE  | GET, POST, PUT, PATCH, DELETE | GET, POST, PUT, PATCH, DELETE | Comments   |
| /api/v1/auth/signup/ | POST | POST | POST | Signup     |
| /api/v1/auth/token/ | POST | POST | POST | Token      |
| /api/v1/users/ |  |  | GET, POST, PUT, PATCH, DELETE | Users      |
| /api/v1/users/me/ | GET, PATCH | GET, PATCH | GET, POST, PUT, PATCH, DELETE | User`s info |
 
## Contributors
For anyone who is interested in contributing to YaMDb REST API, please make sure you fork the project and make a pull request.


![example workflow](https://github.com/Alex-Develepor/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Ссылка на сайт [http://ub1ka.ddns.net/redoc/]