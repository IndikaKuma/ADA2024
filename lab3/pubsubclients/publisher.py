import json
import logging

from google.cloud import pubsub_v1


# Code is based on the following examples from Google. Please check them for more information.
# https://github.com/googleapis/python-pubsub/blob/master/samples/snippets/publisher.py
# https://github.com/googleapis/python-pubsub/blob/master/samples/snippets/subscriber.py

def create_topic(project_id, topic_id):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        topic = publisher.create_topic(request={"name": topic_path})
        logging.info("Created topic: {}".format(topic.name))
    except Exception as ex:
        logging.info(ex)  # instead, can check if there is a topic already, and only if not create a new one


def publish_message(project_id, topic_id, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, message)
    try:
        future.result()  # see https://docs.python.org/3/library/concurrent.futures.html
    except Exception as ex:
        logging.info(ex)
    logging.info(f"Published messages to {topic_path}.")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    data = [
        {
            "ntp": 1,
            "pgc": 126,
            "dbp": 60,
            "tsft": 0,
            "si": 0,
            "bmi": 30.1,
            "dpf": 0.349,
            "age": 47
        }
    ]
    data = json.dumps(data).encode("utf-8")
    publish_message("ada2023", "diabetes_req", data)  # replace ada2023 with your project id
