import logging
import time

import schedule
from google.cloud import pubsub_v1


def pull_message(project, subscription):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        logging.info(f"Received {message.data}.")
        event_type = message.attributes.get("event_type")
        logging.info(f" Event Type {event_type}..\n")
        logging.info(f" Messages {message.data}..\n")
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
            streaming_pull_future.result(timeout=60)
        except Exception as ex:
            logging.info(ex)
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete..
            logging.info("Streaming pull future canceled.")


class MessagePuller:
    def __init__(self, project, subscription):
        self.project_id = project
        self.subscription_id = subscription

    def run(self):
        schedule.every().minute.at(':00').do(pull_message, self.project_id, self.subscription_id)
        while True:
            try:
                schedule.run_pending()
                time.sleep(.1)
            except Exception as ex:
                logging.info(ex)
