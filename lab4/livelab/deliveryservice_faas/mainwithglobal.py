from db import Base, engine
from resources.delivery import Delivery
from resources.status import Status
import functions_framework
# Global (instance-wide) scope
# This computation runs at instance cold-start
# see https://cloud.google.com/functions/docs/bestpractices/tips
db_created = None


def init_db():
    global db_created  # see https://cloud.google.com/functions/docs/bestpractices/tips
    if not db_created:
        Base.metadata.create_all(engine)
        db_created = True

@functions_framework.http
def create_delivery(request):
    from flask import abort
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        init_db()
        return Delivery.create(request_json)
    else:
        return abort(405)

@functions_framework.http
def get_delivery(request):
    print(request.path)
    from flask import abort
    if request.method == 'GET':
        request_args = request.args
        d_id = request_args['d_id']
        init_db()
        return Delivery.get(d_id)
    else:
        return abort(405)

@functions_framework.http
def update_delivery_status(request):
    from flask import abort
    if request.method == 'PUT':
        request_args = request.args
        status = request_args['status']
        d_id = request_args['d_id']
        init_db()
        return Status.update(d_id, status)
    else:
        return abort(405)

@functions_framework.http
def delete_delivery(request):
    from flask import abort
    if request.method == 'DELETE':
        request_args = request.args
        d_id = request_args['d_id']
        init_db()
        return Delivery.delete(d_id)
    else:
        return abort(405)
