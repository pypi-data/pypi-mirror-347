# 🧩 grpc-orchestrator

**`grpc-orchestrator`** is a lightweight, gRPC-based Saga orchestration system for coordinating distributed transactions across microservices. It helps ensure data consistency by executing a series of steps with compensating rollbacks in case of failures.

---

## 🚀 Key Features

- **Saga Pattern Implementation**: Coordinates multi-step transactions with compensation support for failures.
- **gRPC-Native Architecture**: Fast and type-safe communication using Protocol Buffers and gRPC.
- **Flexible Step Definition**: Each step supports service, method, timeout, and optional compensation logic.
- **Asynchronous Orchestration**: Steps execute in order, compensation runs in reverse on failure.
- **In-Memory Storage**: Ideal for prototyping and testing. Easily swappable for custom persistent backends.
- **Execution Logging**: Tracks timestamps, success/failure, payloads, and error messages per step.

---

## 📦 Components

### 1. Protobuf APIs

Defines the orchestrator and participant interfaces:

```proto
service SagaOrchestratorService {
  rpc StartSagaTransaction (StartSagaRequest) returns (StartSagaResponse);
  rpc GetSagaStatusTransaction (GetSagaStatusRequest) returns (GetSagaStatusResponse);
}

service SagaParticipant {
  rpc Execute (SagaParticipantRequest) returns (SagaParticipantResponse);
  rpc Compensate (SagaParticipantRequest) returns (SagaParticipantResponse);
}

###pip install grpc_orchestrator

```python

from grpc_orchestrator.core.client.client import GrpcOrchestratorClient

client = GrpcOrchestratorClient(orchestrator_host="localhost")
steps = [
    {
        "port": 50052,
        "rpc_method": "CleateOrder",
        "compensation_method": "RollbackOrder",
        "timeout_seconds": 5,
    },
    {
        "port": 50052,
        "rpc_method": "CheckoutOrder",
        "compensation_method": "CheckoutOrder",
        "timeout_seconds": 5,
    },
]
client.start_transaction(transaction_id="1234",steps=steps,payload={
    "id": "1",
    "name":"item1"
})

status = client.get_transaction_status(transaction_id="order_123")
print(status)

![Saga Flow Diagram](grpc_orchestrator/images/flow.png)
