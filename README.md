# agrocult_backend

First start a project with 2 workers for process images:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build api
docker-compose -f deploy/docker-compose.yml --project-directory . up --scale tasks-actors-ycc=2
```

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

## Migrations

If you want to migrate your database, you should run following commands:
```bash
# Upgrade database to the last migration.
aerich upgrade
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
aerich downgrade
```

### Migration generation

To generate migrations you should run:
```bash
aerich migrate
```


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml --project-directory . down
```

For running tests on your local machine.
1. you need to start a database.

I prefer doing it with docker:
```
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=agrocult_backend" -e "POSTGRES_USER=agrocult_backend" -e "POSTGRES_DB=agrocult_backend" postgres:13.4-buster
```


2. Run the pytest.
```bash
pytest -vv .
```
