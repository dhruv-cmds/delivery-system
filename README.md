# Delivery System

A FastAPI-based backend for a food delivery platform. The project is being built around a clean service-oriented backend structure with async SQLAlchemy models, Pydantic validation schemas, JWT authentication, Dockerized MySQL, and planned support for orders, payments, tracking, notifications, and realtime websocket updates.

## Current Status

This project is under active development. Core database models, validation schemas, authentication helpers, and several service-layer modules are in place. Order creation, lookup, update, status transition, and deletion logic has also been added at the service layer. API route handlers, tests, websocket handlers, background tasks, frontend work, and load test scripts are currently scaffolded or pending implementation.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2 async ORM
- MySQL 8.0
- aiomysql
- Pydantic v2
- passlib and bcrypt for password hashing
- python-jose for JWT access tokens
- Docker and Docker Compose
- k6 planned for load testing

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │    └── routes/       # FastAPI route modules
│   │   ├── core/              # Config, security, constants, logging, exceptions
│   │   ├── db/                # Async database session and SQLAlchemy models
│   │   ├── repositories/      # Repository layer placeholders
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Business logic modules
│   │   ├── tasks/             # Background task placeholders
│   │   ├── tests/             # Test placeholders
│   │   └── websocket/         # Realtime event and handler placeholders
│   └── requirements.txt
├── docker/                    # Dockerfiles
├── frontend/                  # Frontend placeholder
├── k6/                        # Load test placeholders
├── nginx/                     # Nginx placeholder
├── scripts/                   # Utility script placeholders
├── docker-compose.yml
└── docker-compose.dev.yml
```

## Implemented Domain Model

The backend currently defines SQLAlchemy models for:

- Users
- Restaurants
- Menu items
- Orders
- Order items
- Payments
- Delivery partners
- Order tracking updates
- Notifications

Relationships are defined between users, restaurants, orders, menu items, delivery partners, tracking updates, and notifications.

## Implemented Backend Work

- Async SQLAlchemy database engine and session factory for MySQL.
- Environment-based database host selection for local and Docker execution.
- JWT access token creation.
- Password hashing and verification.
- Custom HTTP exception classes with structured error responses.
- Pydantic schemas for users, auth, restaurants, menu items, orders, payments, delivery partners, notifications, and websocket messages.
- User service for creating users and fetching users by id, email, or username.
- Auth service for signup and login.
- Restaurant service for create, read, update, and delete operations with ownership checks.
- Menu service for create, read, update, delete, and availability status changes with owner authorization.
- Notification service for creating, listing, marking as read, and deleting notifications.
- Order query service for fetching available menu items for orders and retrieving customer-scoped orders.
- Order service for single-item order creation, updating order items, status changes, and deletion with final-state guards.

## Environment Variables

Create `backend/.env` before running the project.

```env
ENV=docker
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_USER=delivery_user
DB_PASSWORD=delivery_password
DB_NAME=delivery_db

MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=delivery_db
MYSQL_USER=delivery_user
MYSQL_PASSWORD=delivery_password
```

For local execution outside Docker, set `ENV=dev`. The database session currently expects MySQL on `127.0.0.1:3010` in development mode.

## Running With Docker

```bash
docker compose up --build
```

The API container is configured to expose FastAPI on:

```text
http://localhost:8003
```

The MySQL container is exposed on:

```text
127.0.0.1:3010
```

For SELinux-aware local development, use:

```bash
docker compose -f docker-compose.dev.yml up --build
```

## Local Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the API once `backend/app/main.py` is implemented:

```bash
uvicorn backend.app.main:app --reload
```

## Development Notes

- `backend/app/main.py` is currently empty, so the FastAPI app entrypoint still needs to be created.
- API route files are currently placeholders.
- Repository modules are currently placeholders.
- Payment, tracking, websocket, Redis, analytics, and background task services are currently placeholders.
- Order service currently supports one menu item per order and still needs route integration and broader workflow handling.
- Test files are currently placeholders.
- Frontend, nginx, k6 load tests, and utility scripts are currently placeholders.

## Suggested Next Steps

1. Implement the FastAPI application entrypoint in `backend/app/main.py`.
2. Add dependency wiring for async database sessions and authenticated users.
3. Implement route handlers for auth, users, restaurants, menu, notifications, orders, payments, tracking, and websockets.
4. Add migrations with Alembic or a clear database initialization strategy.
5. Expand order business logic beyond the current single-item service flow and complete payment business logic.
6. Add tests for services and API routes.
7. Seed useful development data.
8. Implement k6 load tests after stable API endpoints exist.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
