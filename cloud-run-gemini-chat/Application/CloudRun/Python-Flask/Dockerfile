# Use the official Python 3 image.
# https://hub.docker.com/_/python
#
# python:3 builds a 1060 MB image - 342 MB in Google Container Registry
# FROM python:3
#
# python:3-slim builds a 172 MB image - 60 MB in Google Container Registry
# FROM python:3-slim
#
# python:3-alpine builds a 97 MB image - 32 MB in Google Container Registry
FROM python:3-alpine

# RUN apt-get update -y
# RUN apt-get install -y python-pip

# Create and change to the app directory.
WORKDIR /app

COPY . .

RUN chmod 444 app.py requirements.txt

RUN adduser app -D app

# Run the application as a non-root user.
USER app

# Fix warning message: WARNING: The script is installed in '/home/app/.local/bin' which is not on PATH.
ENV PATH=${PATH}:/home/app/.local/bin

RUN python -m pip install --no-cache-dir -r requirements.txt

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

ENV PYTHONUNBUFFERED True

# Run the web service on container startup.
# CMD [ "python", "app.py" ]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
