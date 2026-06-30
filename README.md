# Food Delivery Management System

A production-oriented food delivery backend built with FastAPI, SQLAlchemy Async ORM, MySQL, JWT authentication, role-based access control, Docker, and a service-layer architecture.

The system supports restaurant management, menu management, order processing, payments, delivery partner management, notifications, and order tracking.

## Screenshots

### Swagger UI

![Swagger](images/about.png)

![Swagger](images/endpoints_1.png)

![Swagger](images/endpoints_2.png)

![Swagger](images/endpoints_3.png)

![Swagger](images/endpoints_3.png)

### Database Diagram

![Schema](images/erd_diagram.png)

## Features

### Authentication & Authorization

* User registration
* JWT-based authentication
* Password hashing with bcrypt
* Role-based access control
* Admin-only endpoints
* Restaurant owner authorization
* Delivery partner authorization

### Restaurant Management

* Create restaurants
* Retrieve restaurant details
* Update restaurant information
* Change restaurant status
* Delete restaurants
* Redis caching support


### Menu Management

* Create menu items
* Retrieve menu items
* Retrieve restaurant menus
* Update menu items
* Change menu availability status
* Delete menu items
* Redis caching support

### Order Management

* Create orders
* Retrieve orders
* Update order status
* Delete orders
* Customer-specific order visibility
* Restaurant-specific order visibility
* Delivery partner order visibility
* Redis caching support

### Payment Management

* Create payments for orders
* Retrieve payment by payment ID
* Retrieve payment by order ID
* List payment history
* Update payment status
* Automatic order payment status synchronization
* Redis caching support

### Delivery Partner Management

* Register delivery partners
* Update partner profile
* Update delivery location
* Retrieve partner information
* Delete delivery partners
* Redis caching support

### Notifications

* Create notifications
* Retrieve notifications
* Mark notifications as read
* Mark all notifications as read
* Delete notifications
* Administrative notification access

### Performance

* Redis caching layer
* Cache-aside strategy
* Cache refresh after updates
* Rate limiting using SlowAPI
* Health Monitoring
* API health checks
* Database connectivity checks
* Redis connectivity checks

### Health Monitoring

* API health checks
* Database connectivity checks

---

## Tech Stack

### Backend

* Python 3.11
* FastAPI
* SQLAlchemy 2.0 Async ORM
* Pydantic v2
* aiomysql
* MySQL 8
* Redis

### Security

* python-jose
* passlib
* bcrypt

### Infrastructure

* Docker
* Docker Compose
* Nginx
* Redis

### Testing & Performance

* pytest (planned)
* k6 load testing (planned)

---

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/                     # FastAPI route modules
│   │   ├── core/                           # Config, security, constants, logging, exceptions
│   │   ├── db/                             # Async database session 
│   │   │   └── models/                     # SQLAlchemy models
│   │   ├── repositories/                   # Repository layer placeholders
│   │   ├── schemas/                        # Pydantic request/response schemas
│   │   ├── services/                       # Business logic modules
│   │   ├── tasks/                          # Background task placeholders
│   │   ├── tests/                          # Test placeholders
│   │   ├── websocket/                      # Realtime event and handler placeholders
│   │   │
│   │   ├── docker-compose.dev.yml          # Api Container (for SELinux/Fedora etc...)
│   │   ├── docker-compose.yml              # Api Container
│   │   ├── lifespan.py
│   │   └── main.py
│   │
│   ├──.env.example
│   └── requirements.txt
│
├── db_quires/                              # Database setup tables creation and permissions 
├── docker/                                 # Dockerfiles   
├── frontend/                               # Frontend
├── image/                                  # Image about project 
├── k6/                                     # Load test
├── nginx/                                  # Nginx placeholder
├── scripts/                                # Utility script
│
├── docker-compose.dev.yml                  # Api Container (for SELinux/Fedora etc...)
├── docker-compose.yml                      # Api Container
├── LICENSE
├── progress.md
└── README.md
```

---

## Domain Model

The system currently includes the following entities:

* User
* Restaurant
* Menu Item
* Order
* Order Item
* Payment
* Delivery Partner
* Order Tracking
* Notification

Entity relationships are implemented using SQLAlchemy ORM with proper foreign key constraints and ownership validation.

---

# ⚙️ Environment Variables

## 🏗️ Shared Infrastructure (Recommended)

Use this configuration if you're running the separate `docker-infra` repository.

```env
COMPOSE_PROJECT_NAME=delivery-app

ENV=docker

DB_HOST=shared-mysql
DB_PORT=3306
DB_NAME=delivery
DB_USER=delivery_user
DB_PASSWORD=delivery_password

REDIS_HOST=shared-redis
REDIS_PORT=6379
REDIS_DB=1
REDIS_PASSWORD = changeme

SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Requires the `docker-infra` repository to be running.
**repo**: https://github.com/Dhruv-Cmds/docker-infra
---

## 🐳 Standalone Docker (Open Source)

Use this configuration when running the project with `docker-compose.oss.yml`.

```env
COMPOSE_PROJECT_NAME=delivery-app

ENV=docker

MYSQL_ROOTPASSWORD=chagneme
DB_HOST=mysql
DB_PORT=3306
DB_NAME=delivery
DB_USER=delivery_user
DB_PASSWORD=delivery_password

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=1
REDIS_PASSWORD = changeme

SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Works without the `docker-infra` repository.

## 💻 Local Development (Without Docker)

```env
COMPOSE_PROJECT_NAME=delivery-app

ENV=dev

MYSQL_ROOTPASSWORD=changeme
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=banking
DB_USER=banking_user
DB_PASSWORD=your_password

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=1

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

API:

```text
http://localhost:8003
```

Database:

```text
127.0.0.1:3010
```

---

## Local Development

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI:

```bash
uvicorn app.main:app --reload
```

---

## Current Development Status

### Completed

* Async SQLAlchemy setup
* MySQL integration
* Redis integration
* JWT authentication
* Password hashing
* Custom exception system
* Service-layer architecture
* Role-based access control
* Restaurant management
* Menu management
* Order management
* Payment processing
* Delivery partner management
* Order tracking
* Notification management
* Health monitoring endpoints
* Redis caching across services
* Rate limiting
* Docker configuration
* OpenAPI / Swagger documentation
* Middleware architecture
* Authentication middleware
* Request logging middleware
* Metrics middleware

### In Progress

* WebSocket support
* Background task processing
* Frontend application

### Planned

* pytest test suite
* k6 load testing
* Real-time order tracking
* Analytics dashboard
* CI/CD pipeline
* Production deployment

---

## Development Notes

* Database tables are currently initialized during application startup.
* Alembic migrations should replace automatic table creation before production deployment.
* Redis is used as the caching layer for frequently accessed resources.
* Cache entries are refreshed after update operations.
* Repository layer exists but is intentionally lightweight because business logic is handled through services.
* API endpoints are documented through FastAPI OpenAPI generation.
* Docker is the primary development environment.

---

## Roadmap

1. Complete remaining API modules.
2. Implement WebSocket order tracking.
3. Add Redis-based event handling.
4. Write pytest integration and service-layer tests.
5. Create k6 performance test suites.
6. Configure CI/CD workflows.
7. Complete frontend integration.
8. Deploy to a cloud environment.

---

## License

This project is licensed under the MIT License.

See LICENSE for details.the [LICENSE](LICENSE) file for details.
