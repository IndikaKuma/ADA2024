import logging
import os

from message_puller import MessagePuller
from pub_sub_util import create_topic, create_subscription
from resources.order import Order, Orders

logging.basicConfig(level=logging.INFO)
orders = Orders()
order = Order()
project_id = os.environ['project_id']
mp = MessagePuller(project=project_id, subscription="inventory_status_sub", orders=orders)
mp.run()
