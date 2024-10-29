# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Run migrations, collect static files, and start the Django development server
CMD ["python", "manage.py", "runserver", " 0.0.0.0:8000"]
