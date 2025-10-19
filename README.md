# ⚡ ChronoServe++

**ChronoServe++** is an adaptive API gateway that monitors real-time latency, stores telemetry in PostgreSQL, and uses a reinforcement learning (RL) loop to dynamically optimize request routing across backend services.  
It combines **FastAPI**, **PostgreSQL**, **Prometheus**, and **Grafana** into a self-optimizing, observable microservice ecosystem.

---

## Features
- **Smart API Gateway** dynamically routes traffic using RL decisions.  
- **Telemetry Database** every request logs endpoint, latency, region, and timestamp.  
- **Live Observability** Prometheus metrics + Grafana dashboards.  
- **Reinforcement Learning Loop** learns which backend minimizes latency for the current state.  
- **A/B Testing Ready** compare static vs adaptive routing performance.

---

## Architecture

```
flowchart TD
    A[Client (curl / hey)] --> B[API Gateway (FastAPI)]
    B -->|RL Decision| C[RL Agent (Q-learning)]
    C -->|Chosen Route| D[Backend Service (service1 / service2)]
    D -->|Response + Latency| E[Telemetry Logger]
    E --> F[PostgreSQL (telemetry table)]
    F --> G[Materialized View (latency_stats)]
    G -->|Scrape Metrics| H[Prometheus]
    H --> I[Grafana Dashboard]
    B -->|/metrics| H
```

| Service                             | Role                                           | Tech Stack                 |
| ----------------------------------- | ---------------------------------------------- | -------------------------- |
| **API Gateway (`chornoserve-api`)** | Routes requests, logs telemetry, runs RL agent | FastAPI, HTTPX, SQLAlchemy |
| **Backend Service(s)**              | Simple test endpoints (`/test`)                | FastAPI                    |
| **Database (`db`)**                 | Stores telemetry + aggregated latency stats    | PostgreSQL                 |
| **Prometheus**                      | Scrapes and stores metrics                     | Prometheus                 |
| **Grafana**                         | Dashboards and latency visualizations          | Grafana                    |



| Column       | Type      | Description            |
| ------------ | --------- | ---------------------- |
| `id`         | SERIAL    | Primary key            |
| `endpoint`   | VARCHAR   | API path               |
| `latency_ms` | FLOAT     | Request latency in ms  |
| `region`     | VARCHAR   | Region label           |
| `timestamp`  | TIMESTAMP | When request completed |



## Files Structure
```
chornoserve/
├── app/
│   ├── main.py                 # FastAPI gateway entrypoint
│   ├── proxy.py                # Core proxy logic + telemetry hook
│   ├── telemetry.py            # Logs latency to Postgres
│   ├── db.py                   # Async SQLAlchemy setup
│   ├── models.py               # Telemetry model
│   ├── rl_agent.py             # Q-learning RL controller
│   ├── config.py               # DB/Prometheus configuration
│   └── init_db.py              # Table creation / migrations
├── service1/
│   └── main.py                 # Example backend with /test endpoint
├── docker-compose.yml          # Defines services
├── Dockerfile                  # API gateway container build
├── requirements.txt            # Python dependencies
└── README.md                   # (this file)
```



##Quick Commands

# Build and run
docker compose build --no-cache api
docker compose up -d

# Initialize DB schema
docker compose exec api python app/init_db.py

# Load test
hey -n 1000 -c 20 http://localhost:8080/service1/test

# Check telemetry
docker compose exec db psql -U chronouser -d chronoserve -c "SELECT * FROM telemetry LIMIT 10;"


$ docker compose exec db psql -U chronouser -d chronoserve -c "SELECT * FROM latency_stats;"

  | endpoint      | region  | minute_window        | requests | p95_latency | avg_latency |
  |----------------|----------|----------------------|-----------|--------------|--------------|
  | service1/test | us-east | 2025-10-19 06:10:00 | 500       | 15.43 ms     | 10.22 ms     |




