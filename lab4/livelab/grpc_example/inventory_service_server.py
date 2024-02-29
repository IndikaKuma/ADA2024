from concurrent import futures
import logging

import grpc

import inventory_service_pb2
import inventory_service_pb2_grpc


class InventoryService(inventory_service_pb2_grpc.InventoryServiceServicer):
    inventories = []

    def __init__(self):
        self.inventories = [
            {
                "name": "Laptop",
                "amount": 1000,
                "metric": "items"
            },
            {
                "name": "Phone",
                "amount": 5000,
                "metric": "items"
            }
        ]

    def GetProductQuantity(self, request, context):
        # request is ProductType message
        ptype = request.type
        for record in self.inventories:
            if ptype == record["name"]:
                return inventory_service_pb2.Quantity(amount=record["amount"], metric=record["metric"])
        return inventory_service_pb2.Quantity(amount=-1, metric="items")

    def GetStockSummary(self, request_iterator, context):
        # request is ProductType message
        product_stocks = {}
        for product_type in request_iterator:
            product_stocks[product_type.type] = self.GetProductQuantity(product_type, context)
        return inventory_service_pb2.StockSummary(productStocks=product_stocks)


def serve():
    # Create a gRPC server instance and register the service 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_service_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryService(), server)
    logging.info('InventoryService Deployed')
    server.add_insecure_port('[::]:5005') # HTTP transport
    server.start()
    logging.info('Server Started')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()