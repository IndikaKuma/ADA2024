import json
import logging
import time
from threading import Thread

import schedule
from google.cloud import pubsub_v1

from pub_sub_util import publish_message


class Callable:
    def __init__(self, project, product):
        self.project = project
        self.product = product

    def callback(self, message):
        logging.info(f"Received {message.data}.")
        event_type = message.attributes.get("event_type")  # event type as a message attribute
        data = json.loads(message.data.decode("utf-8"))
        if event_type == "OrderReq":
            quantityAva = self.product.get_quantity(data["product_type"])
            if quantityAva < data["quantity"]:
                data = {
                    "message": "The requested quantity cannot be satisfied"
                }
                data = json.dumps(data).encode("utf-8")
                publish_message(project=self.project, topic="inventory_status", message=data,
                                event_type="StockUnavailable")
            else:
                data = json.dumps(data).encode("utf-8")
                publish_message(project=self.project, topic="inventory_status", message=data,
                                event_type="StockAvailable")
        elif event_type == "OrderCreated":
            self.product.put(data["product_type"], data["quantity"])
            data = {
                "message": "The inventory was updated"
            }
            data = json.dumps(data).encode("utf-8")
            publish_message(project=self.project, topic="inventory_status", message=data, event_type="InventoryUpdated")
        message.ack()


def pull_message(project, subscription, product):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=Callable(product=product, project=project).callback,
        await_callbacks_on_shutdown=True,
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
    def __init__(self, project, subscription_order_req, subscription_order_status, product):
        self.project_id = project
        self.subscription_order_req = subscription_order_req
        self.subscription_order_status = subscription_order_status
        self.product = product

    def run(self):
        schedule.every().minute.at(':00').do(pull_message, self.project_id, self.subscription_order_req, self.product)
        schedule.every().minute.at(':00').do(pull_message, self.project_id, self.subscription_order_status,
                                             self.product)
        while True:
            try:
                schedule.run_pending()
                time.sleep(.1)
            except Exception as ex:
                logging.info(ex)
