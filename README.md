# Tech Stack

**Backend:** FastAPI

**Frontend:** Jinja2, Pure JS

**Server:** Gunicorn

**Services:** Docker, MySQL


# Run Locally with docker-compose


```bash
  git clone -b master https://github.com/vladgenyuk/Library_test_m2m
```
```bash
  cd Test1AK
```
```bash
  docker-compose up -d
```

# Run Locally without docker-compose


```bash
  git clone -b master https://github.com/vladgenyuk/Library_test_m2m
```
```
alembic upgrade head
```
```bash
  docker run --name webtronics_db -d -p 5432:5432 -e POSTGRES_USER=vlad -e POSTGRES_PASSWORD=qseawdzxc1 postgres
```

```bash
  uvicorn backend.main:app --reload
```

## Registration and Authorization

For register and authorization User needs only to Enter his name and email, email for each user is unique.
## Frontend

I used build-in in FastAPI Jinja2 template generator and pure JS to display information on web pages and add active behaviour on pages. Endpoints with pages run on the same host and port as the main application.

To imitate the suspended Frontend application, the endpoints and HTML templates makes additional requests to backend.

## Folder structure 

I tried to make a clear and expandable folder structure with methods with headen realization that easy to use and expand, Exception invokers and others to simplify the programming process.
