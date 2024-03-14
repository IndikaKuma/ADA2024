import random

orderRecords = [
    {
        "id": "id1",
        "product_type": "Laptop",
        "quantity": 4000,
        "unit_price": 444.50
    }
]


class Order:
    def get(self, id):
        for record in orderRecords:
            if id == record["id"]:
                return record, 200
        return {"message": "Order record not found"}

    def put(self, id, rating):
        for record in orderRecords:
            if id == record["id"]:
                record["rating"] = rating
                return record, 200
        return {"message": "Order record not found"}

    def delete(self, id):
        to_be_deleted = None
        for record in orderRecords:
            if id == record["id"]:
                to_be_deleted = record
                break
        if to_be_deleted:
            orderRecords.remove(to_be_deleted)
            return {"message": "{} is deleted.".format(id)}
        return {"message": "Order record not found"}


class Orders:
    def post(self, request):
        record_to_be_created = request.get_json(force=True)
        id1 = "id" + str(random.randint(1, 100001))
        record_to_be_created["id"] = id1
        for record in orderRecords:
            if id1 == record["id"]:
                return {"message": "Order with id {} already exists".format(id)}
        orderRecords.append(record_to_be_created)
        return record_to_be_created

    def create_order(self, data):
        record_to_be_created = data
        id1 = "id" + str(random.randint(1, 100001))
        record_to_be_created["id"] = id1
        for record in orderRecords:
            if id1 == record["id"]:
                return {"message": "Order with id {} already exists".format(id)}
        orderRecords.append(record_to_be_created)
        return record_to_be_created

    def put(self, request):
        record_to_be_created = request.get_json(force=True)
        id = record_to_be_created['id']
        to_be_deleted = None
        for record in orderRecords:
            if id == record["id"]:
                to_be_deleted = record
                break
        if to_be_deleted:
            orderRecords.remove(to_be_deleted)
        orderRecords.append(record_to_be_created)
        return record_to_be_created

    def get(self):
        results = []
        for record in orderRecords:
            results.append(record["id"])
        return results
