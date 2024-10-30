# Retail Store Data Engineering Pipeline

## Project Overview
This project demonstrates a complete end-to-end data engineering pipeline designed for a retail store's sales data. It covers every stage from data ingestion to transformation and quality checks, culminating in data storage and analytics-ready tables in BigQuery. The pipeline is built using Apache Airflow, integrated with dbt for data transformation, and Astro CLI for local environment management. The project includes automated data quality checks using Soda, modular task handling, and dependency isolation.

## Tools and Technologies
- **Orchestration**: Apache Airflow
- **Data Transformation**: dbt (Data Build Tool)
- **Data Quality**: Soda for data quality checks
- **Storage**: Google Cloud Storage, BigQuery
- **Deployment and Dependencies**: Astro CLI, Docker
- **Languages**: SQL, Python

## Pipeline Architecture
The pipeline is structured into the following modular components:

1. **Data Ingestion**
   - **Objective**: To automate the ingestion of raw CSV files into Google Cloud Storage and load data into BigQuery.
   - **Tools**: Astro SDK, Google Cloud Storage, BigQuery.

2. **Data Transformation with dbt**
   - **Objective**: Transform raw data into analytics-ready tables by running dbt models within Airflow.
   - **Tools**: dbt, Airflow, Comos.
   - **Key Steps**:
     - Model creation to normalize and structure data
     - Data enrichment and creation of aggregates for further analytics

3. **Data Quality Checks with Soda**
   - **Objective**: Ensure data integrity by implementing checks at various pipeline stages.
   - **Tools**: Soda.
   - **Quality Checks**:
     - Column null-checks
     - Distribution analysis for sales figures

4. **Dependency Isolation**
   - **Objective**: Minimize task dependency conflicts for reliable pipeline performance.
   - **Implementation**: Isolation of Airflow tasks using Astro CLI and Docker to prevent conflicts across dbt, Astro SDK, and BigQuery dependencies.

## Key Features

- **Modular Pipeline Design**: Each task (ingestion, transformation, quality check) is modular and reusable for future retail data.
- **Data Quality Assurance**: Automated data quality checks with Soda ensure high data reliability.
- **Environment Management with Astro CLI**: Set up a local Airflow environment from scratch using Astro CLI, with clear environment isolation for reproducibility.
- **Data Ingestion Automation**: Seamlessly uploads CSV files into Google Cloud Storage and BigQuery tables, leveraging the Astro SDK for streamlined ingestion.
- **End-to-End Orchestration with Airflow**: Manages the entire data pipeline from ingestion to storage, handling daily and batch runs effectively.

## Pipeline Workflow

1. **Setting Up the Airflow Environment with Astro CLI**
2. **CSV Upload to Google Cloud Storage**
3. **BigQuery Ingestion**
4. **Running Data Quality Checks with Soda**
5. **Data Transformation with dbt**

## End-Results
**Scalable Pipelines**: Designed for retail data ingestion and transformation on a large scale.
**Enhanced Data Quality**: Data quality checks integrated into each stage to ensure consistency.
**Optimized Analytics**: Final dataset optimized for quick analytics, compatible with popular BI tools for insights on product performance, sales trends, and regional performance.
