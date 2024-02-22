import json
import os

from google.cloud import storage
from keras.models import load_model

import functions_framework
import base64
import pandas as pd
from pub_sub_util import publish_message


@functions_framework.cloud_event
def predict_diabetes(cloud_event):
    """Background Cloud Function to be triggered by Pub/Sub
       See https://cloud.google.com/functions/docs/tutorials/pubsub
    """
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    print('Event ID: {}'.format(event_id))
    print('Event type: {}'.format(event_type))

    decodedStr = base64.b64decode(data["message"]["data"]).decode()
    print('Message data : {}'.format(decodedStr))

    prediction_input = json.loads(decodedStr)

    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    model_bucket_name = os.environ.get('MODEL_REPO', 'Specified environment variable is not set.')
    print('Project Id: {}'.format(project_id))

    # Open a channel to read the file from GCS
    df = pd.read_json(json.dumps(prediction_input), orient='records')

    # Download model
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(model_bucket_name)
    blob = bucket.blob('model.h5')
    temp_model_filename = os.path.join('/tmp', 'model.h5')
    blob.download_to_filename(temp_model_filename)
    model = load_model(temp_model_filename)

    print(df)
    y_pred = model.predict(df)
    status = (y_pred[0] > 0.5)

    print('Result : {}'.format(status))

    # Publish the result to the topic diabetes_req. Note, here, we assume the topic already exists.
    data = {'result': str(status[0])}
    data = json.dumps(data).encode("utf-8")  # always need to send base64 binary data
    publish_message(project=project_id, topic="diabetes_res", message=data)

    # Do clean up
    os.remove(temp_model_filename)
