import datetime

from airflow import models
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

from custom_ops import CustomTransformationOperator

# If you are running Airflow in more than one time zone
# see https://airflow.apache.org/docs/apache-airflow/stable/timezone.html
# for best practices
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    'owner': 'ADA',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': YESTERDAY,
}

with models.DAG(
        'simple_etl',
        catchup=False,
        default_args=default_args,
        schedule_interval=datetime.timedelta(days=1)) as dag:
    download_from_gcs = GCSToLocalFilesystemOperator(
        task_id="download_from_gcs",
        object_name="sales.csv",
        bucket="adadata",
        filename="local_sales.csv"
    )

    transform = CustomTransformationOperator(
        task_id='transform_data', file_name='local_sales.csv')

    upload_to_gsc = LocalFilesystemToGCSOperator(
        task_id='upload_to_gsc',
        bucket='adadata',
        src="{{ task_instance.xcom_pull(task_ids='transform_data') }}",
        # See https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html for Xcoms
        dst='sales_sum.csv'
    )

    create_bq_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_bq_dataset', dataset_id="sales"
    )

    load_to_table = GCSToBigQueryOperator(
        task_id='load_to_bq_table',
        bucket='adadata',
        source_objects=['sales_sum.csv'],
        destination_project_dataset_table="sales.summary",
        schema_fields=[
            {'name': 'customer_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'unit_sales', 'type': 'INTEGER', 'mode': 'NULLABLE'}
        ],
        write_disposition='WRITE_TRUNCATE'
    )

    # About control flow, https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html#control-flow
    download_from_gcs >> transform >> upload_to_gsc >> create_bq_dataset >> load_to_table
