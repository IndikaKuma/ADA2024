import json
import logging
import os
from google.cloud import storage
import functions_framework
import google.cloud.aiplatform as aip


def run_pipeline_job(name, pipeline_def, pipeline_root, parameter_dict):
    # Opening JSON file
    f = open(parameter_dict)
    data = json.load(f)
    print(data)
    logging.info(data)
    job = aip.PipelineJob(
        display_name=name,
        enable_caching=False,
        template_path=pipeline_def,
        pipeline_root=pipeline_root,
        parameter_values=data)
    job.run()


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def trigger_vertexai_pipeline(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket_name}")
    print(f"File: {file_name}")

    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    name = os.environ.get('PIPELINE_NAME', 'Specified environment variable is not set.')
    pipeline_def = os.environ.get('PIPELINE_FILE', 'Specified environment variable is not set.')
    pipeline_root = os.environ.get('PIPELINE_ROOT', 'Specified environment variable is not set.')
    parameter_bucket = os.environ.get('PARAMETERS_BUCKET', 'Specified environment variable is not set.')
    parameter_file = os.environ.get('PARAMETERS_FILE', 'Specified environment variable is not set.')

    print('PIPELINE_NAME: {}'.format(name))
    print('PIPELINE_FILE: {}'.format(pipeline_def))
    print('PIPELINE_ROOT_BUCKET: {}'.format(pipeline_root))
    print('PARAMETERS_BUCKET: {}'.format(parameter_bucket))
    print('PARAMETERS_FILE: {}'.format(parameter_file))
    # Download the parameter file
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(parameter_bucket)
    blob = bucket.blob(parameter_file)
    temp_parameter_file = os.path.join('/tmp', parameter_file)
    blob.download_to_filename(temp_parameter_file)

    run_pipeline_job(name=name, pipeline_def=pipeline_def, pipeline_root=pipeline_root,
                     parameter_dict=temp_parameter_file)
    logging.info("Vertex AI Pipeline was submitted")
