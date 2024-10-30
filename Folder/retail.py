from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType
from airflow.models.baseoperator import chain


@dag(
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['retail'],
)
def retail():
    # Task 1: Upload CSV to GCS
    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='/usr/local/airflow/include/dataset/Online_Retail.csv',
        dst='raw/Online_Retail.csv',
        bucket='vasanth_online_retail',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    # Task 2: Create BigQuery Dataset
    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail',
        gcp_conn_id='gcp',
    )

    # Task 3: Load GCS file to BigQuery with specified encoding
    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://vasanth_online_retail/raw/Online_Retail.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='raw_invoices',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )

    # Define the check_load task
    @task.external_python('/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check  # Moved inside the function
        return check(scan_name, checks_subpath)

    # Define the DBT transform task group
    from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
    from cosmos.airflow.task_group import DbtTaskGroup
    from cosmos.constants import LoadMode
    from cosmos.config import RenderConfig
    
    transform = DbtTaskGroup(
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']
        )
    )

    # Define the check_transform task
    @task.external_python('/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check  # Moved inside the function
        return check(scan_name, checks_subpath)

    # Define the DBT report task group
    report = DbtTaskGroup(
        group_id='report',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        )
    )

    # Define the check_report task
    @task.external_python('/usr/local/airflow/soda_venv/bin/python')
    def check_report(scan_name='check_report', checks_subpath='transform'):
        from include.soda.check_function import check  # Moved inside the function
        return check(scan_name, checks_subpath)

    # Set up task dependencies
    chain(
        upload_csv_to_gcs,
        create_retail_dataset,
        gcs_to_raw,
        check_load(),
        transform,
        check_transform(),
        report,
        check_report(),
    )

# Define the DAG without calling retail()
retail_dag = retail
