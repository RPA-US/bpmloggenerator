# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9.2-slim-buster

RUN apt-get update
RUN apt-get install -y gcc postgresql-server-dev-all musl-dev libffi-dev cmake python-tk

# Allows docker to cache installed dependencies between builds
WORKDIR /bpmloggenerator
RUN /usr/local/bin/python -m venv venv
RUN ./venv/bin/python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN ./venv/bin/python -m pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . .

# runs the production server
RUN ["chmod", "+x", "./entry.sh"]
ENTRYPOINT ["./entry.sh"]