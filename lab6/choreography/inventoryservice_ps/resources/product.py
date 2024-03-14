inventories = [
    {
        "name": "Laptop",
        "quantity": 1000
    },
    {
        "name": "Phone",
        "quantity": 5000
    }
]


class Product:
    def get_quantity(self, pname):
        for record in inventories:
            if pname == record["name"]:
                return record["quantity"]

    def get(self, pname):
        for record in inventories:
            if pname == record["name"]:
                return record
        return {"message": "No product for " + pname}

    def put(self, pname, value):
        for record in inventories:
            if pname == record["name"]:
                record["quantity"] = record["quantity"] - value
                return record
        return {"message": "No product for " + pname}


class Products:
    def post(self, request):
        record_to_be_created = request.get_json(force=True)
        pname = record_to_be_created["name"]
        for record in inventories:
            if pname == record["name"]:
                return {"message": "There is a product with the name " + pname}
        inventories.append(record_to_be_created)
        return record_to_be_created

    def post_query(self, request):
        pname = request.args.get('name')
        quantity = request.args.get('quantity')
        for record in inventories:
            if pname == record["name"]:
                return {"message": "There is a product with the name " + pname}
        record_to_be_created = {"name": pname, "quantity": quantity}
        inventories.append(record_to_be_created)
        return record_to_be_created
