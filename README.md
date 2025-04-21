## generate file proto

```bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/greeter.proto
```

## run server

navigate to `grpc-project`

```bash
python server.py
```

## run client

navigate to `grpc-project`

```bash
python client.py
```
