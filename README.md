# Queenbees

![python](https://img.shields.io/static/v1?label=Python&message=3.11&logo=Python&color=3776AB)
![django](https://img.shields.io/static/v1?label=Django&message=5.0&logo=Django&color=092E20)

Queenbees is a CMS with django backend and react front end.
It's a personal project I want to use on multiple website projects, so it's definitely over-engineered.
I use it also as an experimental project.

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

# Install NVM and Node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
&& source $HOME/.nvm/nvm.sh \
&& nvm install 20.9.0

# Install dependencies
cd src
poetry install
poetry run install-frontend-dependencies --test
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

### Create super user
```shell
poetry run createsuperuser
```

## Useful commands

### Linters

All backend linters:
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

**import linter**: Checks import contracts
```shell
poetry run python-import-linter
```

### Typing
```shell
poetry run python-type-checker
```

Frontend linter and type checker:
```shell
npm run eslint
```

## Tests

### Python tests

Run tests for a specific target
```shell
DJANGO_CONFIGURATION=<config> poetry run python-tests <files>
```

Run all python tests
```shell
poetry run python-tests-all
```

Run unit tests
```shell
poetry run python-tests-unit
```

Run Interface agnostic tests
```shell
poetry run python-tests-interface-agnostic
```

Run backoffice tests
```shell
poetry run python-tests-backoffice
```

### Javascript/Typescript tests
```shell
poetry run js-tests
```
