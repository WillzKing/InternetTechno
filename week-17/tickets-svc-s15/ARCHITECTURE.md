# System Architecture

**Project code:** tickets-s15

## Overview

The system consists of 3 services:
1. **tickets-api** (REST) ? Public API for frontend clients
2. **tickets-grpc** (gRPC) ? Internal service for inter-service communication
3. **Nginx** ? API Gateway / Reverse Proxy

## Architecture Diagram
+----------+
| Client   |
+-----+----+
      |
HTTP (REST)
      |
+-----v----+
| Nginx    |
| :80      |
+-----+----+
      |
+-----+-----+
      | 
/api/tickets/* /health
        |                 |
+-------v--------+ +------v-------+
| tickets-api    | | Nginx        |
| (REST :8144)   | | Health       |
+-------+--------+ +--------------+
        |
gRPC (internal)
        |
+-------v--------+
| tickets-grpc   |
| (gRPC :50051)  |
+----------------+

## Services

### tickets-api (REST)
- **Protocol:** REST/HTTP
- **Port:** 8144
- **Purpose:** Public API for CRUD operations on tickets
- **Endpoints:**
  - POST /tickets/ ? Create ticket
  - GET /tickets/ ? List all tickets
  - GET /tickets/{id} ? Get ticket by ID
  - GET /health ? Health check

### tickets-grpc (gRPC)
- **Protocol:** gRPC (Protobuf)
- **Port:** 50051
- **Purpose:** Internal service for high-performance ticket operations
- **Methods:**
  - CreateTicket
  - GetTicket
  - ListTickets
  - SubscribeTickets (streaming)

### Nginx (Gateway)
- **Protocol:** HTTP
- **Port:** 80
- **Purpose:** Reverse proxy, routing requests to appropriate services

## Communication Patterns

| From         | To            | Protocol | Purpose                |
|--------------|---------------|----------|------------------------|
| Client       | Nginx         | REST     | All external requests  |
| Nginx        | tickets-api   | REST     | Route /api/tickets/*   |
| tickets-api  | tickets-grpc  | gRPC     | Internal operations    |

## Technology Stack

- **Languages:** Python 3.11
- **Frameworks:** FastAPI, gRPC
- **Protocols:** REST (HTTP/1.1), gRPC (HTTP/2)
- **Serialization:** JSON (REST), Protobuf (gRPC)
- **Containerization:** Docker, Docker Compose
- **Reverse Proxy:** Nginx

## Deployment

All services run in Docker containers:
- Single docker-compose.yml for local development
- Nginx routes external traffic to internal services
- Services communicate over internal Docker network

## Security

- Non-root users in all containers
- Input validation via Pydantic (REST) and Protobuf (gRPC)
- Health checks for all services
- Rate limiting ready (via Nginx)

## Data Flow

1. Client sends POST request to Nginx
2. Nginx routes to tickets-api
3. tickets-api validates input and forwards to tickets-grpc via gRPC
4. tickets-grpc processes and stores data
5. Response flows back: gRPC -> REST -> Nginx -> Client
