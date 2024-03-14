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


def publish_message(project, topic, message, event_type):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    future = publisher.publish(topic_path, message, event_type=event_type)
    try:
        future.result()
    except Exception as ex:
        logging.info(ex)
        future.cancel()
    logging.info(f"Published event {event_type} to {topic_path}.")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    data = {
        "product_type": "Phone",
        "quantity": 10,
        "unit_price": 232.00
    }
    data = json.dumps(data).encode("utf-8")
    publish_message(project="your_project_id", topic="order_req", message=data, event_type="OrderReq")
