# Use the official Python image as the base image
FROM python:3.10

# Set environment variables for Python and pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for MySQL client
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app files into the container
COPY . .

RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate

# Expose the port that Django runs on (change this if necessary)
EXPOSE 8000

# Run the Django development server when the container starts
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
