# FAST API BACKEND TEMPLATE

This repository contains a template for all types of backend projects.


## Fast Initial Deploy 

```bash
docker-compose up --build -d 
docker compose run --rm backend alembic revision --autogenerate -m "initial migration"
docker compose run --rm backend alembic upgrade head

docker compose up backend
```

## Run Test

Just run this script 

```bash
.\run_tests.bat
```