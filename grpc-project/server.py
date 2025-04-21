import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc

class MyService(service_pb2_grpc.MyServiceServicer):
    def UnaryHello(self, request, context):
        return service_pb2.HelloResponse(message=f"Hello, {request.name}!")

    def ServerStreamHello(self, request, context):
        for i in range(5):
            yield service_pb2.HelloResponse(message=f"Hello {request.name}, message {i+1}")

    def ClientStreamHello(self, request_iterator, context):
        names = [req.name for req in request_iterator]
        return service_pb2.HelloResponse(message=f"Hello, {' & '.join(names)}!")

    def Chat(self, request_iterator, context):
        for req in request_iterator:
            print(f"[Client]: {req.name}: {req.message}")
            response = input("[Server]: ")
            yield service_pb2.HelloResponse(message=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
