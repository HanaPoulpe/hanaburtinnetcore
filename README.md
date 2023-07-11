# Personal website for [Hana Burtin](https://hanaburtin.net/)

![python](https://img.shields.io/static/v1?label=Python&message=3.11&logo=Python&color=3776AB)
![django](https://img.shields.io/static/v1?label=Django&message=4.2&logo=Django&color=092E20)

## Install and run

### Prepare your devdesk

#### Install dependencies
```shell
# Install poetry
pip install poetry

# Install dependencies
cd src
poetry install
```

#### Activate virtual environment
```shell
poetry shell
```

### Run the server locally

```shell
cd src
./manage runserver 8000
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
