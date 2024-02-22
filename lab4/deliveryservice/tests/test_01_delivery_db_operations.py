import datetime

import os
import pytest

from constant import STATUS_CREATED
from daos.delivery_dao import DeliveryDAO
from daos.status_dao import StatusDAO
from db import Session, engine, Base


class TestDeliveryDBOP:

    @pytest.fixture(scope="session", autouse=True)
    def execute_before_any_test(self):
        os.environ['DB_URL'] = 'sqlite:///delivery_test.db'
        # 2 - generate database schema
        Base.metadata.create_all(engine)

    # your setup code goes here, executed ahead of first test
    def test_add_query_record(self):
        session = Session()
        status_1 = StatusDAO(STATUS_CREATED, datetime.datetime.now())
        delivery_1 = DeliveryDAO("cus_1", "thaifood", "pack1", datetime.datetime.now(),
                                 datetime.datetime(2021, 3, 17, 23, 45),
                                 status_1)
        session.add(status_1)
        session.add(delivery_1)
        # 10 - commit and close session
        session.commit()

        deliveries = session.query(DeliveryDAO).all()
        print('\n### All deliveries:')
        print(len(deliveries))
        for delivery in deliveries:
            print(
                f'{delivery.id} was created by {delivery.customer_id}. Its current status is {delivery.status.status}')
        print('')
        assert deliveries is not None
        session.close()
