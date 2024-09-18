# Use an official Python runtime as a parent image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD gunicorn --bind :8080 main:app --timeout 5000