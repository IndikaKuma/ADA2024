# MLP for Pima Indians Dataset saved to single file
# see https://machinelearningmastery.com/save-load-keras-deep-learning-models/
import logging
import os

from flask import jsonify
from keras.layers import Dense
from keras.models import Sequential
from google.cloud import storage


def train(dataset):
    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    model_repo = os.environ.get('MODEL_REPO', 'Specified environment variable is not set.')
    model_name = os.environ.get('MODEL_NAME', 'Specified environment variable is not set.')
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:8]
    Y = dataset[:, 8]
    # define model
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
    # evaluate the model
    scores = model.evaluate(X, Y, verbose=0)
    text_out = {
        "accuracy:": scores[1],
        "loss": scores[0],
    }
    logging.info(text_out)

    model_path = os.path.join('/tmp', model_name)
    model.save(model_path, save_format='h5')
    # Save to GCS
    client = storage.Client(project=project_id)
    bucket = client.get_bucket(model_repo)
    blob = bucket.blob(model_name)
    blob.upload_from_filename(model_path)
    # Do clean up
    os.remove(model_path)

    # Saving model in a given location provided as an env. variable
    return jsonify(text_out), 200
