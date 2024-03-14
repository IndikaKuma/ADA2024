import logging

from user_consumer import create_subscription
from user_publisher import create_topic

logging.getLogger().setLevel(logging.INFO)
create_topic("your_project_id", "order_req") # make sure to change the project id
create_subscription("your_project_id", "order_req", "order_req_sub")
create_topic("your_project_id", "inventory_status")
create_topic("your_project_id", "order_status")
create_topic("your_project_id", "order_status_user")
create_subscription("your_project_id", "order_status_user", "order_status_user_sub")
create_topic("your_project_id", "order_req")
create_topic("your_project_id", "inventory_status")
create_subscription("your_project_id", "inventory_status",
                    "inventory_status_sub")
create_subscription("your_project_id", "order_status","order_status_sub")
