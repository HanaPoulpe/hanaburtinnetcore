# Personal website for [Hana Burtin](https://hanaburtin.net/)

![python](https://img.shields.io/static/v1?label=Python&message=3.11&logo=Python&color=3776AB)
![django](https://img.shields.io/static/v1?label=Django&message=4.2&logo=Django&color=092E20)

## Install and run

### Prepare your devdesk

#### Prerequisites

_**TODO:** Update tests to use docker PostgreSQL container_

* PostgreSQL server installed
* User with `CREATEDB` permission and access to PostgreSQL socket

Setup PostgreSQL role:
```shell
echo "CREATE USER $(whoami) WITH CREATEDB;" | psql -U postgres
```

#### Install dependencies
```shell
# Install poetry
pip install poetry

# Install dependencies
cd src
poetry install
poetry run install-frontend-dependencies
```

#### Activate virtual environment
```shell
poetry shell
```

### Configure local environment

```shell
cp src/.env.example src/.env
```

* Configure relevant API Keys

### Run the server locally

Start the server with docker compose
```shell
poetry run docker-start
```

Stop docker compose
```shell
poetry run docker-stop
```

Run django migrations
```shell
poetry run docker-migrate
```

Full django build
```shell
poetry run docker-build
```

## Useful commands

### Linters

All linters:
```shell
poetry run python-linters
```

**isort**: Sort imports
```shell
poetry run python-linter-isort
```

**black**: Standard python linter
```shell
poetry run python-linter-black
```

### Typing
```shell
poetry run python-type-checker
```

## Tests

### Python tests
```shell
poetry run python-tests
```
