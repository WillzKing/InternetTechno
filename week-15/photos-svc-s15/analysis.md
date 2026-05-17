# Load Testing Analysis

**Project code:** photos-s15

## Test Setup

- **Service:** REST API (FastAPI)
- **Endpoint:** GET /photos/
- **CPU Limit:** 0.5 core (Docker --cpus=0.5)
- **Workers:** 1 uvicorn worker
- **Tool:** PowerShell parallel requests

## Results

| Concurrency | Total Requests | Duration (s) | RPS   | Avg Latency (ms) |
|-------------|----------------|--------------|-------|------------------|
| 1           | 120            | 30.1         | 4.0   | 250.0            |
| 10          | 70             | 30.2         | 2.3   | 434.8            |
| 100         | 100            | 256.8        | 0.4   | 2500.0           |

## Analysis

### Latency vs RPS

- **Concurrency 1:** RPS = 4.0, Latency = 250ms ? optimal performance
- **Concurrency 10:** RPS = 2.3, Latency = 434.8ms ? performance degradation begins
- **Concurrency 100:** RPS = 0.4, Latency = 2500ms ? saturation point reached

### Saturation Point

The saturation point is reached at **~10 concurrent connections**.
- RPS stops growing and starts decreasing
- Latency increases sharply from 250ms to 2500ms
- CPU is fully saturated at 0.5 core limit

### Key Findings

1. With 1 worker and 0.5 CPU, the service handles ~4 RPS optimally
2. Adding more concurrent connections beyond 10 leads to queue buildup
3. At 100 concurrent connections, the system is overwhelmed ? RPS drops to 0.4
4. Latency at saturation point increases 10x (from 250ms to 2500ms)

### Recommendations

1. Increase CPU limit to 1-2 cores for production
2. Use multiple uvicorn workers (--workers 4) for better concurrency
3. Add load balancer (Nginx) to distribute traffic
4. Consider async database for I/O-bound operations
