import json
import logging
import os

import functions_framework

# Triggered by a change in a storage bucket
from pub_sub_util import publish_message


@functions_framework.cloud_event
def notify_model_update(cloud_event):
    data = cloud_event.data
    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print('Bucket Name: {}'.format(bucket_name))
    print('File Name: {}'.format(file_name))

    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    print('Project Id: {}'.format(project_id))

    # Publish the result to the topic model-update. Note, here, we assume the topic already exists.
    data = [
        {"bucket": bucket_name},
        {"file": file_name}
    ]
    data = json.dumps(data).encode("utf-8")  # always need to send base64 binary data
    publish_message(project=project_id, topic="model-update", message=data)

    logging.info("A Message was sent to the model-update topic")
