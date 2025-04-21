import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc

class MyServiceServicer(service_pb2_grpc.MyServiceServicer):
    
    # Unary method
    def UnaryMethod(self, request, context):
        return service_pb2.ResponseMessage(message=f"Hello, {request.name}")
    
    # Server streaming method
    def ServerStreamingMethod(self, request, context):
        for i in range(3):
            yield service_pb2.ResponseMessage(message=f"Streaming response {i+1} to {request.name}")
            time.sleep(1)  # Simulate delay
    
    # Client streaming method
    def ClientStreamingMethod(self, request_iterator, context):
        names = []
        for request in request_iterator:
            names.append(request.name)
        return service_pb2.ResponseMessage(message=f"Received names: {', '.join(names)}")
    
    # Bidirectional streaming method
    def BidirectionalStreamingMethod(self, request_iterator, context):
        for request in request_iterator:
            yield service_pb2.ResponseMessage(message=f"Hi {request.name}, how can I assist you?")
            time.sleep(1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
