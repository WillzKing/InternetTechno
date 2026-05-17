import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import grpc
from concurrent import futures
from datetime import datetime
import time
import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc

messages_db = []
id_counter = 1


class MessagesService(pb2_grpc.MessagesServiceServicer):
    
    def CreateMessage(self, request, context):
        global id_counter
        message = {
            "id": id_counter,
            "name": request.name,
            "topic": request.topic,
            "created_at": datetime.now().isoformat()
        }
        messages_db.append(message)
        id_counter += 1
        
        return pb2.MessageResponse(
            id=message["id"],
            name=message["name"],
            topic=message["topic"],
            created_at=message["created_at"]
        )
    
    def GetMessage(self, request, context):
        message = next((m for m in messages_db if m["id"] == request.id), None)
        if not message:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Сообщение с ID {request.id} не найдено")
            return pb2.MessageResponse()
        
        return pb2.MessageResponse(
            id=message["id"],
            name=message["name"],
            topic=message["topic"],
            created_at=message["created_at"]
        )
    
    def ListMessages(self, request, context):
        response = pb2.ListMessagesResponse()
        for message in messages_db:
            response.messages.append(pb2.MessageResponse(
                id=message["id"],
                name=message["name"],
                topic=message["topic"],
                created_at=message["created_at"]
            ))
        return response
    
    def SubscribeMessages(self, request, context):
        for message in messages_db:
            yield pb2.MessageResponse(
                id=message["id"],
                name=message["name"],
                topic=message["topic"],
                created_at=message["created_at"]
            )
            time.sleep(0.1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MessagesServiceServicer_to_server(MessagesService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()