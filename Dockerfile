# Create a docker image for local testing
FROM python:3.12-bookworm

SHELL ["/bin/bash", "--login", "-c"]

# Set variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NVM_DIR /nvm

# Set work directory
WORKDIR /src

# Copy files
COPY . .

# Setup environment
RUN pip install poetry
RUN poetry install
# RUN poetry export > requirements.txt
# RUN pip install -r requirements.txt
WORKDIR /nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
    && source /nvm/nvm.sh \
    && nvm install 20.9.0
WORKDIR /src
RUN poetry run install-frontend-requirements
