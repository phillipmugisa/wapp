# Dockerfile for Django app

# Use the official Python image as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /code

# Install dependencies
COPY ./code/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django code files to the container
COPY ./code /code

# Start the Django development server
CMD python manage.py runserver 0.0.0.0:8000
