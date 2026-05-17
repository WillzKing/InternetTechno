import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import grpc
from concurrent import futures
from datetime import datetime
import time
import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc

tickets_db = []
id_counter = 1


class TicketsService(pb2_grpc.TicketsServiceServicer):
    
    def CreateTicket(self, request, context):
        global id_counter
        ticket = {
            "id": id_counter,
            "name": request.name,
            "status": request.status,
            "created_at": datetime.now().isoformat()
        }
        tickets_db.append(ticket)
        id_counter += 1
        
        return pb2.TicketResponse(
            id=ticket["id"],
            name=ticket["name"],
            status=ticket["status"],
            created_at=ticket["created_at"]
        )
    
    def GetTicket(self, request, context):
        ticket = next((t for t in tickets_db if t["id"] == request.id), None)
        if not ticket:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Тикет с ID {request.id} не найден")
            return pb2.TicketResponse()
        
        return pb2.TicketResponse(
            id=ticket["id"],
            name=ticket["name"],
            status=ticket["status"],
            created_at=ticket["created_at"]
        )
    
    def ListTickets(self, request, context):
        response = pb2.ListTicketsResponse()
        for ticket in tickets_db:
            response.tickets.append(pb2.TicketResponse(
                id=ticket["id"],
                name=ticket["name"],
                status=ticket["status"],
                created_at=ticket["created_at"]
            ))
        return response
    
    def SubscribeTickets(self, request, context):
        for ticket in tickets_db:
            yield pb2.TicketResponse(
                id=ticket["id"],
                name=ticket["name"],
                status=ticket["status"],
                created_at=ticket["created_at"]
            )
            time.sleep(0.1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_TicketsServiceServicer_to_server(TicketsService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()