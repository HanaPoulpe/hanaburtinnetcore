# Create a docker image for local testing
FROM python:3.11-slim-bookworm

# Set variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /src

# Copy files
COPY . .

# Setup environment
RUN pip install poetry
RUN poetry install