import base64
import json
import logging
import os
import functions_framework

from pub_sub_util import create_topic, publish_message


@functions_framework.cloud_event
def receive_order_status(cloud_event):
    logging.basicConfig(level=logging.INFO)
    event_id = cloud_event["id"]
    logging.info("""This Function was triggered by EventId {}""".format(event_id))
    logging.info(cloud_event)
    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    custom_event_type = cloud_event.data["message"]["attributes"]["event_type"]
    logging.info("""The application specific event type is {}""".format(custom_event_type))
    if custom_event_type == "OrderCreated":
        data_payload = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8'))
        logging.info(data_payload)
        order_id = data_payload["id"]
        data = {
            "message": "The order was accepted. The order id is {}.".format(order_id)
        }
        data = json.dumps(data).encode("utf-8")
        publish_message(project=project_id, topic="order_status_user", message=data, event_type="OrderAccepted")
    elif custom_event_type == "StockUnavailable":
        data = {
            "message": "Sorry, we can not meet your order at the moment. Please try later."
        }
        data = json.dumps(data).encode("utf-8")
        publish_message(project=project_id, topic="order_status_user", message=data, event_type="OrderRejected")
