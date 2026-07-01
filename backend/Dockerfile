FROM python:3.12-slim

WORKDIR /codigo

# Dependencias del sistema para psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Puerto de la API FastAPI
EXPOSE 8000
