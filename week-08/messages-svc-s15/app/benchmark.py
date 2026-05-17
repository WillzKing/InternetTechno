import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import grpc
import requests
import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc

GRPC_HOST = "localhost:50051"
REST_URL = "http://localhost:8253/messages/"

PROJECT_CODE = "messages-s15"


def benchmark_grpc(num_requests=1000):
    channel = grpc.insecure_channel(GRPC_HOST)
    stub = pb2_grpc.MessagesServiceStub(channel)
    
    start = time.time()
    for i in range(num_requests):
        stub.CreateMessage(pb2.CreateMessageRequest(
            name=f"gRPC message {i}",
            topic="benchmark"
        ))
    end = time.time()
    
    total = end - start
    avg = total / num_requests * 1000
    return total, avg


def benchmark_rest(num_requests=1000):
    start = time.time()
    for i in range(num_requests):
        requests.post(REST_URL, json={
            "name": f"REST message {i}",
            "topic": "benchmark"
        })
    end = time.time()
    
    total = end - start
    avg = total / num_requests * 1000
    return total, avg


if __name__ == "__main__":
    print(f"Project: {PROJECT_CODE}")
    print("=" * 50)
    
    print("\nЗапуск gRPC бенчмарка (1000 запросов)...")
    grpc_total, grpc_avg = benchmark_grpc(1000)
    print(f"gRPC общее время: {grpc_total:.3f} сек")
    print(f"gRPC среднее на запрос: {grpc_avg:.3f} мс")
    
    print("\nЗапуск REST бенчмарка (1000 запросов)...")
    print("Убедитесь, что REST сервер запущен на порту 8253!")
    print("Если сервер не запущен, запустите его из week-01 или week-02.")
    
    try:
        rest_total, rest_avg = benchmark_rest(1000)
        print(f"REST общее время: {rest_total:.3f} сек")
        print(f"REST среднее на запрос: {rest_avg:.3f} мс")
        
        print("\n" + "=" * 50)
        print("СРАВНЕНИЕ:")
        print(f"gRPC быстрее REST в {rest_total/grpc_total:.2f} раз(а)")
    except Exception as e:
        print(f"REST сервер недоступен: {e}")