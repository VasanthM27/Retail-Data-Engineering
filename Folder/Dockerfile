# Base image with astro-runtime
FROM quay.io/astronomer/astro-runtime:12.2.0 AS astro

# Second stage for building and installing Soda dependencies
FROM python:3.12-slim AS soda-builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install soda in a virtual environment, along with pandas
RUN python -m venv /soda_venv && \
    . /soda_venv/bin/activate && \
    pip install --no-cache-dir pandas==1.5.3 && \
    pip install --no-cache-dir soda-core-bigquery==3.0.45 && \
    pip install --no-cache-dir soda-core-scientific==3.0.45 && \
    deactivate

# Copy soda virtual environment into astro runtime
FROM astro
COPY --from=soda-builder /soda_venv /usr/local/airflow/soda_venv

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery==1.5.3 && deactivate