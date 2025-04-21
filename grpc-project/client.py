import grpc
import service_pb2
import service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)

        while True:
            print("\\nPilih jenis RPC:")
            print("1. Unary")
            print("2. Server Streaming")
            print("3. Client Streaming")
            print("4. Bidirectional Streaming (Chat)")
            print("0. Exit")
            choice = input("Pilihan: ")

            if choice == "1":
                name = input("Masukkan nama: ")
                response = stub.UnaryHello(service_pb2.HelloRequest(name=name))
                print(f"[Server]: {response.message}")

            elif choice == "2":
                name = input("Masukkan nama: ")
                for response in stub.ServerStreamHello(service_pb2.HelloRequest(name=name)):
                    print(f"[Server]: {response.message}")

            elif choice == "3":
                print("Ketik nama, ketik 'done' untuk mengirim:")
                def client_stream():
                    while True:
                        name = input("Nama: ")
                        if name.lower() == "done":
                            break
                        yield service_pb2.HelloRequest(name=name)
                response = stub.ClientStreamHello(client_stream())
                print(f"[Server]: {response.message}")

            elif choice == "4":
                print("Masuk ke mode chat (ketik 'exit' untuk keluar):")
                def generate_messages():
                    name = input("Nama Anda: ")
                    while True:
                        msg = input("Anda: ")
                        if msg.lower() == 'exit':
                            break
                        yield service_pb2.HelloRequest(name=name, message=msg)

                responses = stub.Chat(generate_messages())
                try:
                    for response in responses:
                        print(f"[Server]: {response.message}")
                except grpc.RpcError:
                    print("Koneksi chat selesai.")

            elif choice == "0":
                break
            else:
                print("Pilihan tidak dikenali.")

if __name__ == '__main__':
    run()
