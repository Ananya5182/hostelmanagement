# CampusStay — Enterprise Hostel Management System

A production-grade, containerized **Hostel Management & Room Allocation System** built with **FastAPI (Python 3.11)**, **Vanilla JS / CSS3 (Nginx 1.25)**, **Supabase PostgreSQL**, **Docker Compose**, **Jenkins CI/CD**, and **Nagios Core** health monitoring.

---

## Architecture Overview

CampusStay follows a 12-factor cloud-native microservices architecture:

1. **Frontend & Ingress**: High-performance Nginx 1.25 Alpine reverse proxy serving responsive, glassmorphic UI assets on Port 80 and forwarding `/api/*` and `/health` requests to the application layer.
2. **Application Backend**: Python 3.11 FastAPI asynchronous service on Port 8000 with Pydantic v2 schemas and transaction-safe room allocation logic.
3. **Database Layer**: Managed Supabase PostgreSQL with real-time room capacity tracking and relational foreign key constraints.
4. **DevOps & Automation**: Automated multi-stage Docker builds, isolated bridge networking, Declarative Jenkins CI/CD pipeline with JUnit XML reporting, and Nagios Core service probes.

---

## Directory Structure

```text
hostel-management/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Application package definition
│   │   ├── main.py               # FastAPI router, CORS & lifecycle
│   │   ├── database.py           # Supabase client singleton & health probe
│   │   ├── schemas.py            # Pydantic v2 data validation models
│   │   └── crud.py               # Transactional allocation & DB queries
│   ├── tests/
│   │   ├── __init__.py           # Test suite package
│   │   └── test_main.py          # Pytest suite with Supabase mocks & JUnit XML
│   ├── Dockerfile                # Hardened Python 3.11-slim non-root image
│   └── requirements.txt          # Python production dependencies
├── frontend/
│   ├── static/
│   │   ├── index.html            # Dark-slate responsive dashboard
│   │   ├── styles.css            # Glassmorphism, CSS Grid & animations
│   │   └── app.js                # Vanilla JS reactive client logic
│   ├── Dockerfile                # Lightweight Nginx 1.25 Alpine image
│   └── nginx.conf                # Port 80 server with API reverse proxy
├── nagios-config/
│   └── hostel_services.cfg       # Nagios Core disk, web & health probes
├── database_schema.sql           # PostgreSQL DDL with RLS policies & indexes
├── docker-compose.yml            # Multi-container orchestration & network
├── Jenkinsfile                   # Declarative CI/CD pipeline
├── .gitignore                    # Git ignore rules
├── .env                          # Active credentials
└── README.md                     # Technical reference documentation
```

---

## Technical Specifications

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **API Framework** | FastAPI / Starlette | `>= 0.115` | High-throughput REST API with OpenAPI autodocs |
| **ASGI Server** | Uvicorn | `>= 0.32` | Asynchronous web server |
| **Data Validation** | Pydantic | `>= 2.9` | Strict input parsing & response serialization |
| **Database SDK** | `supabase-py` | `>= 2.10` | PostgREST client for PostgreSQL |
| **Web Server / Ingress** | Nginx | `1.25-alpine` | Reverse proxy & static content caching |
| **Orchestration** | Docker & Compose | v2+ | Container runtime & network isolation |
| **CI/CD Automation** | Jenkins | Declarative | Linting, Pytest, Docker Push, Zero-downtime Deploy |
| **System Monitoring** | Nagios Core | 4.x | Active host disk, HTTP 80 & API /health polling |

---

## Quickstart: Running Locally

### 1. Direct Local Execution (Python & Browser)

Ensure Python 3.11+ is installed, then run:

```bash
# 1. Install backend requirements
pip install -r backend/requirements.txt

# 2. Run test suite to verify everything passes
python -m pytest backend/tests/test_main.py -v --junitxml=test-reports/junit.xml -o pythonpath=backend

# 3. Start the FastAPI development server
uvicorn app.main:app --app-dir backend --reload --port 8000
```

- API Docs: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`
- Frontend: Open `frontend/static/index.html` directly in your browser or serve via HTTP.

### 2. Docker Compose (Full Production Stack)

Run the entire containerized architecture with a single command:

```bash
# Build and launch all services in detached mode
docker compose up -d --build

# View container runtime status
docker compose ps

# Follow unified logs
docker compose logs -f
```

- **Frontend Web Portal**: [http://localhost](http://localhost) (Port 80)
- **Direct Backend API**: [http://localhost:8000](http://localhost:8000) (Port 8000)
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Healthcheck Probe**: [http://localhost/health](http://localhost/health)

---

## REST API Reference

### 1. System Health Probe
- **Endpoint**: `GET /health`
- **Description**: Actively pings Supabase PostgreSQL to verify end-to-end database connectivity.
- **Success Response (200 OK)**:
  ```json
  {
    "status": "UP",
    "database": "CONNECTED"
  }
  ```
- **Failure Response (503 Service Unavailable)**:
  ```json
  {
    "status": "DOWN",
    "database": "DISCONNECTED"
  }
  ```

### 2. List All Rooms
- **Endpoint**: `GET /api/rooms`
- **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "room_number": "A-101",
      "block_name": "Block A",
      "room_type": "SHARED_DOUBLE",
      "capacity": 2,
      "occupied": 2,
      "occupancy": 2,
      "monthly_fee": 6000.0,
      "status": "FULL"
    },
    {
      "id": 2,
      "room_number": "A-102",
      "block_name": "Block A",
      "room_type": "SHARED_DOUBLE",
      "capacity": 2,
      "occupied": 1,
      "occupancy": 1,
      "monthly_fee": 6000.0,
      "status": "AVAILABLE"
    }
  ]
  ```

### 3. List All Students (Joined with Room)
- **Endpoint**: `GET /api/students`
- **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "name": "Rohan Verma",
      "email": "rohan.verma@example.com",
      "phone": "+919820112233",
      "emergency_contact": "+919820119900",
      "room_id": 1,
      "check_in_date": "2026-07-15",
      "created_at": "2026-10-02T13:41:22.808924+00:00",
      "rooms": {
        "id": 1,
        "room_number": "A-101",
        "block_name": "Block A",
        "room_type": "SHARED_DOUBLE",
        "capacity": 2,
        "occupied": 2,
        "status": "FULL"
      }
    }
  ]
  ```

### 4. Allocate Student to Room
- **Endpoint**: `POST /api/students`
- **Payload**:
  ```json
  {
    "name": "Ananya Sharma",
    "email": "ananya.sharma@campus.edu",
    "phone": "+919876543210",
    "emergency_contact": "+919876543299",
    "room_id": 2,
    "check_in_date": "2026-10-02"
  }
  ```
- **Business Logic**:
  1. Validates room exists and is not under `MAINTENANCE`.
  2. Ensures `occupied < capacity`. Rejects with `400 Bad Request` if full.
  3. Increments `occupied = occupied + 1`.
  4. Automatically switches status to `'FULL'` if `occupied == capacity`.
  5. Inserts student record with foreign key reference.
  6. Automatically rolls back room occupancy if student insertion fails.

### 5. Hostel Analytics & KPIs
- **Endpoint**: `GET /api/stats`
- **Response (200 OK)**:
  ```json
  {
    "total_rooms": 11,
    "total_capacity": 22,
    "total_occupied": 9,
    "available_beds": 13,
    "occupancy_rate": 40.9
  }
  ```

---

## Testing & Quality Assurance

Pytest runs in complete isolation using mocked Supabase clients to guarantee 100% deterministic test execution.

```bash
python -m pytest backend/tests/test_main.py -v --junitxml=test-reports/junit.xml -o pythonpath=backend
```

### Test Coverage Highlights:
- `test_health_check_success`: Verifies HTTP 200 and `"status": "UP"`.
- `test_health_check_failure`: Verifies HTTP 503 and `"status": "DOWN"`.
- `test_list_rooms`: Validates capacity, occupancy, and status serialization.
- `test_list_students`: Validates relational room joins.
- `test_allocate_student_success`: Validates transactional capacity increment and auto-transition to `FULL`.
- `test_allocate_student_room_full`: Enforces capacity boundary checks.
- `test_allocate_student_room_maintenance`: Prevents allocations into offline rooms.
- `test_allocate_student_room_not_found`: Verifies HTTP 404 behavior.
- `test_allocate_student_invalid_payload`: Verifies Pydantic v2 validation (HTTP 422).
- `test_dashboard_stats`: Validates mathematical accuracy of KPI computations.

---

## CI/CD Pipeline (Jenkinsfile)

The `Jenkinsfile` provides an enterprise declarative pipeline:
1. **Checkout**: Pulls code from SCM.
2. **Unit Tests**: Spins up python virtual environment, executes test suite, and publishes `test-reports/junit.xml` to Jenkins.
3. **Docker Build**: Compiles Docker images for backend and frontend tagging with `${BUILD_NUMBER}` and `latest`.
4. **Docker Push**: Authenticates to Docker Hub using credential binding and pushes images.
5. **Deploy**: Invokes `docker compose down && docker compose up -d --build`.
6. **Smoke Test**: Executes active HTTP probes against `:80` and `:8000/health`.

---

## Monitoring (Nagios Core)

Configured in `nagios-config/hostel_services.cfg`:
- **Disk Utilization**: Warns at 20% free, alerts Critical at 10% free.
- **Frontend Web Portal**: Polls port 80 every 60 seconds with 2s warning threshold.
- **Backend API & Supabase Health**: Queries `http://127.0.0.1:8000/health` ensuring string `"UP"` is present.
- **Reverse Proxy Ingress**: Tests end-to-end routing through Nginx `/api/rooms`.
