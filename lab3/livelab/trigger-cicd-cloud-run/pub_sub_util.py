import logging

from google.cloud import pubsub_v1


# Code is based on the following examples from Google. Please check them for more information.
# https://github.com/googleapis/python-pubsub/blob/master/samples/snippets/publisher.py
# https://github.com/googleapis/python-pubsub/blob/master/samples/snippets/subscriber.py

def create_topic(project, topic):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project, topic)
        topic = publisher.create_topic(request={"name": topic_path})
        print("Created topic: {}".format(
            topic.name))  # instead, can check if there is a topic already, and only if not create a new one
    except Exception as ex:
        logging.info(ex)


def publish_message(project, topic, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    future = publisher.publish(topic_path, message)
    try:
        future.result()
    except Exception as ex:
        logging.info(ex)
        future.cancel()