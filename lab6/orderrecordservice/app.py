from flask import Flask, request
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Response
from resources.order import Order, Orders

app = Flask(__name__)

orders = Orders()
placeRecord = Order()


# Thanks https://www.maskaravivek.com/post/how-to-add-http-cachecontrol-headers-in-flask/
def docache(minutes=5, content_type='application/json; charset=utf-8'):
    """ Flask decorator that allow to set Cache headers. """

    def fwrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            r = f(*args, **kwargs)
            then = datetime.now() + timedelta(minutes=minutes)
            rsp = Response(r, content_type=content_type)
            rsp.headers.add('Cache-Control', 'public,max-age=%d' % int(60 * minutes))
            return rsp

        return wrapped_f

    return fwrap


@app.route('/orders/<string:id>', methods=['GET'])
@docache(minutes=1, content_type='application/json')
def get_order(id):
    return placeRecord.get(id)


@app.route('/orders/<string:id>', methods=['PUT'])
def update_order(id):
    return placeRecord.put(id, int(request.args.get('rating')))


@app.route('/orders/<string:id>', methods=['DELETE'])
def delete_orders(id):
    return placeRecord.delete(id)


@app.route('/orders/', methods=['POST'])
def create_order():
    return orders.post(request)


app.run(host='0.0.0.0', port=5000, debug=True)
