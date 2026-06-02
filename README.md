# Delivery System

A FastAPI-based backend for a food delivery platform. The project is being built around a clean service-oriented backend structure with async SQLAlchemy models, Pydantic validation schemas, JWT authentication, Dockerized MySQL, and planned support for orders, payments, tracking, notifications, and realtime websocket updates.

## Current Status

This project is under active development. Core database models, validation schemas, authentication helpers, dependency wiring, and several service-layer modules are in place. Auth, user, health, and menu API routes are wired into the FastAPI application. Order creation, lookup, update, status transition, deletion, and payment logic has also been added at the service layer. Tests, websocket handlers, background tasks, frontend work, and load test scripts are currently scaffolded or pending implementation.

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
- FastAPI application entrypoint with database table initialization during app lifespan.
- API dependency helpers for database sessions, JWT-authenticated users, admin-only access, and menu manager access.
- Auth API routes for signup and login.
- User API routes for authenticated lookup and admin-only user listing.
- Health API route with database connectivity check.
- Menu API routes for create, lookup, restaurant-scoped listing, update, delete, and status changes.
- User service for creating users and fetching users by id, email, or username.
- Auth service for signup and login.
- Restaurant service for create, read, update, and delete operations with ownership checks, including customer promotion to restaurant owner during restaurant creation.
- Menu service for create, read, update, delete, and availability status changes with admin and restaurant owner authorization.
- Notification service for creating, listing, marking as read, and deleting notifications.
- Order query service for fetching available menu items for orders and retrieving customer-scoped orders.
- Order service for single-item order creation, updating order items, status changes, and deletion with final-state, quantity, and order-value guards.
- Payment service for creating order payments, fetching payments by payment id or order id, and updating payment status while syncing the related order.

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

Then run the API:

```bash
uvicorn backend.app.main:app --reload
```

## Development Notes

- `backend/app/main.py` currently recreates database tables during application startup. This is useful for early development but should be replaced with migrations before production use.
- Auth, user, health, and menu route files are implemented and registered.
- Restaurant, notification, order, payment, tracking, and websocket route modules still need integration or completion.
- Repository modules are currently placeholders.
- Tracking, websocket, Redis, analytics, and background task services are currently placeholders.
- Payment service is implemented, but payment API routes and tests still need to be added.
- Order service currently supports one menu item per order and still needs route integration and broader workflow handling.
- Test files are currently placeholders.
- Frontend, nginx, k6 load tests, and utility scripts are currently placeholders.

## Suggested Next Steps

1. Replace startup table recreation with Alembic migrations or a clear database initialization strategy.
2. Implement route handlers for restaurants, notifications, orders, payments, tracking, and websockets.
3. Add focused tests for auth, user, menu, restaurant, order, and payment flows.
4. Fix menu route path overlap between menu id and restaurant id lookups.
5. Expand order business logic beyond the current single-item service flow.
6. Seed useful development data.
7. Implement k6 load tests after stable API endpoints exist.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
