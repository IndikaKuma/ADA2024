import json
import logging
import time
from threading import Thread

import schedule
from google.cloud import pubsub_v1

from pub_sub_util import publish_message


def pull_message(project, subscription, orders):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    def callback(message):
        logging.info(f"Received {message.data}.")
        event_type = message.attributes.get("event_type")  # event type as a message attribute
        data = json.loads(message.data.decode("utf-8"))
        if event_type == "StockAvailable":
            logging.info("The event StockAvailable received")
            results = orders.create_order(data)
            results = json.dumps(results).encode("utf-8")
            publish_message(project=project, topic="order_status", message=results, event_type="OrderCreated")
        message.ack()

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, await_callbacks_on_shutdown=True,
    )
    logging.info(f"Listening for messages on {subscription_path}..\n")
    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=60.0)
        except Exception as ex:
            logging.info(ex)
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


class MessagePuller:
    def __init__(self, project, subscription, orders):
        self.project_id = project
        self.subscription_id = subscription
        self.orders = orders

    def run(self):
        schedule.every().minute.at(':00').do(pull_message, self.project_id, self.subscription_id, self.orders)
        while True:
            try:
                schedule.run_pending()
                time.sleep(.1)
            except Exception as ex:
                logging.info(ex)
