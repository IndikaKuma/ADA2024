import logging
import os

import numpy
from google.cloud import storage
from keras.layers import Dense
from keras.models import Sequential

import functions_framework


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def build_diabetes_predictor(cloud_event):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.
      See https://cloud.google.com/functions/docs/tutorials/storage
    """

    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket_name = data["bucket"]
    file_name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket_name}")
    print(f"File: {file_name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    model_bucket_name = os.environ.get('MODEL_REPO', 'Specified environment variable is not set.')
    print('Project Id: {}'.format(project_id))
    print('Bucket Name: {}'.format(model_bucket_name))

    # Open a channel to read the file from GCS
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    temp_filename = os.path.join('/tmp', file_name)
    blob.download_to_filename(temp_filename)
    # See https://machinelearningmastery.com/save-load-keras-deep-learning-models/ for ML model
    # fix random seed for reproducibility
    numpy.random.seed(7)
    # load pima indians dataset
    dataset = numpy.loadtxt(temp_filename, delimiter=",")
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:8]
    Y = dataset[:, 8]
    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
    # evaluate the model
    scores = model.evaluate(X, Y, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    print(model.metrics_names)
    model_path = os.path.join('/tmp', "model.h5")
    model.save(model_path)
    # Save to GCS
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(model_bucket_name)
    blob = bucket.blob('model.h5')
    blob.upload_from_filename(model_path)
    # Do clean up
    os.remove(temp_filename)
    os.remove(model_path)
    logging.info("Saved the model to GCP bucket")
