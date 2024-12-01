FROM python:3.12.6-alpine

# Set environment variables. Prevent Python from writing .pyc files and ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies, including pkg-config and MySQL/MariaDB client libraries
RUN apk update && apk add --no-cache \
    bash \
    build-base \
    curl \
    libffi-dev \
    mysql-dev \
    nodejs \
    npm \
    pkgconfig \
    && rm -rf /var/cache/apk/*

# Copy package.json and package-lock.json (if it exists) and install Node.js dependencies
COPY . .
# Install Node.js dependencies, run the copy-static script, install Python dependencies
RUN npm install && npm run copy-static && \
    pip install --no-cache-dir -r requirements.txt

# Expose the application port (default Django port)
EXPOSE 8000
