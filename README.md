# 5G Core Management Prototype

This repository contains a Python-based, microservice-aligned prototype of a 5G Core management platform. It simulates the most critical control-plane functions and exposes management APIs plus a React dashboard (to be added) for observability.

## Current Scope

Implemented services so far:

1. **Common backend utilities** (`backend/common`)
   - Centralized configuration (Pydantic Settings) with handy DB URL helpers.
   - SQLAlchemy base models and timestamp mixin.
   - Async/Sync database session helpers and Alembic environment hook-up.
2. **NRF Service** (`backend/nrf`)
   - NF registration and discovery endpoints:
     - `POST /nrf/register-nf`
     - `GET /nrf/nfs`
     - `GET /nrf/nfs/{nf_type}`
   - Persists NF metadata in PostgreSQL with status and heartbeat tracking.
   - Dockerfile: `docker/Dockerfile.nrf`
3. **UDM/AUSF Service** (`backend/udm_ausf`)
   - Dummy subscriber store with CRUD (basic list/create) and authentication endpoint.
     - `POST /auth/ue-auth`
     - `GET /auth/subscribers`
     - `POST /auth/subscribers`
   - Dockerfile: `docker/Dockerfile.udm-ausf`
4. **AMF Service** (`backend/amf`)
   - UE registration flow with UDM/AUSF authentication.
     - `POST /amf/ue/register`
     - `GET /amf/ue/{ue_id}`
     - `GET /amf/ues`
   - Dockerfile: `docker/Dockerfile.amf`

The remaining core functions (SMF, NSSF, PCF, UPF, Management API, React dashboard, docker-compose, Kubernetes manifests) will be added next following the staged plan.

## Development Environment

### Requirements
- Python 3.11+
- PostgreSQL 14+ (or compatible container)
- Node 18+ (for the frontend, upcoming)

### Python dependencies

```
pip install -r backend/requirements.txt
```

### Database

Use PostgreSQL and configure environment variables through `.env` (optional). Defaults:

```
POSTGRES_USER=core_admin
POSTGRES_PASSWORD=<set-in-.env>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=core_mgmt
```

Run Alembic migrations (placeholder until migration scripts are generated):

```
cd /home/ashish/CascadeProjects/5g-core-mgmt
alembic upgrade head
```

### Running services locally

Each FastAPI service exposes an ASGI app. Example for NRF:

```
uvicorn backend.nrf.main:app --reload --port 8000
```

Similarly:

- UDM/AUSF: `uvicorn backend.udm_ausf.main:app --reload --port 8010`
- AMF: `uvicorn backend.amf.main:app --reload --port 8001`

Ensure environment variables (`UDM_AUSF_BASE_URL`, DB URL, API keys) are set as needed.

### Docker

Each service has its own Dockerfile under `docker/`. Build examples:

```
docker build -f docker/Dockerfile.nrf -t 5g-nrf .
docker build -f docker/Dockerfile.udm-ausf -t 5g-udm-ausf .
docker build -f docker/Dockerfile.amf -t 5g-amf .
```

Docker Compose and Kubernetes manifests will be provided later to orchestrate the full stack.

## Next Steps
1. Implement SMF/NSSF/PCF/UPF microservices with PDU session flow.
2. Create Management API gateway and React dashboard.
3. Wire up docker-compose and K8s manifests for all services.
4. Expand README with end-to-end flow instructions and frontend usage.

---
This document will evolve as the remaining services and infrastructure pieces land.
