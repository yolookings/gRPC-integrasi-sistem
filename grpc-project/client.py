import grpc
import service_pb2
import service_pb2_grpc

def run_unary():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        response = stub.UnaryMethod(service_pb2.RequestMessage(name="Alice"))
        print(f"Unary response: {response.message}")

def run_server_streaming():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        response_stream = stub.ServerStreamingMethod(service_pb2.RequestMessage(name="Bob"))
        for response in response_stream:
            print(f"Server Streaming response: {response.message}")

def run_client_streaming():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        responses = stub.ClientStreamingMethod(iter([
            service_pb2.RequestMessage(name="Charlie"),
            service_pb2.RequestMessage(name="David")
        ]))
        print(f"Client Streaming response: {responses.message}")

def run_bidirectional_streaming():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        responses = stub.BidirectionalStreamingMethod(iter([
            service_pb2.RequestMessage(name="Eve"),
            service_pb2.RequestMessage(name="Dan")
        ]))
        for response in responses:
            print(f"Bidirectional Streaming response: {response.message}")

if __name__ == '__main__':
    print("Running Unary Method:")
    run_unary()
    print("\nRunning Server Streaming Method:")
    run_server_streaming()
    print("\nRunning Client Streaming Method:")
    run_client_streaming()
    print("\nRunning Bidirectional Streaming Method:")
    run_bidirectional_streaming()
