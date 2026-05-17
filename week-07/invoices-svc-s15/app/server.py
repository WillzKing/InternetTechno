import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import grpc
from concurrent import futures
from datetime import datetime
import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc

invoices_db = []
id_counter = 1


class InvoicesService(pb2_grpc.InvoicesServiceServicer):
    
    def CreateInvoice(self, request, context):
        global id_counter
        invoice = {
            "id": id_counter,
            "name": request.name,
            "amount": request.amount,
            "created_at": datetime.now().isoformat()
        }
        invoices_db.append(invoice)
        id_counter += 1
        
        return pb2.InvoiceResponse(
            id=invoice["id"],
            name=invoice["name"],
            amount=invoice["amount"],
            created_at=invoice["created_at"]
        )
    
    def GetInvoice(self, request, context):
        invoice = next((i for i in invoices_db if i["id"] == request.id), None)
        if not invoice:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Инвойс с ID {request.id} не найден")
            return pb2.InvoiceResponse()
        
        return pb2.InvoiceResponse(
            id=invoice["id"],
            name=invoice["name"],
            amount=invoice["amount"],
            created_at=invoice["created_at"]
        )
    
    def ListInvoices(self, request, context):
        response = pb2.ListInvoicesResponse()
        for invoice in invoices_db:
            response.invoices.append(pb2.InvoiceResponse(
                id=invoice["id"],
                name=invoice["name"],
                amount=invoice["amount"],
                created_at=invoice["created_at"]
            ))
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_InvoicesServiceServicer_to_server(InvoicesService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()