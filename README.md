

# Food Delivery Management System

A production-oriented food delivery backend built with FastAPI, SQLAlchemy Async ORM, MySQL, JWT authentication, role-based access control, Docker, and a service-layer architecture.

The system supports restaurant management, menu management, order processing, payments, delivery partner management, notifications, and order tracking.

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

### Menu Management

* Create menu items
* Retrieve menu items
* Retrieve restaurant menus
* Update menu items
* Change menu availability status
* Delete menu items

### Order Management

* Create orders
* Retrieve orders
* Update order status
* Delete orders
* Customer-specific order visibility
* Restaurant-specific order visibility
* Delivery partner order visibility

### Payment Management

* Create payments for orders
* Retrieve payment by payment ID
* Retrieve payment by order ID
* List payment history
* Update payment status
* Automatic order payment status synchronization

### Delivery Partner Management

* Register delivery partners
* Update partner profile
* Update delivery location
* Retrieve partner information
* Delete delivery partners

### Notifications

* Create notifications
* Retrieve notifications
* Mark notifications as read
* Mark all notifications as read
* Delete notifications
* Administrative notification access

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

### Security

* python-jose
* passlib
* bcrypt

### Infrastructure

* Docker
* Docker Compose
* Nginx

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
│   │   ├── db/                             # Async database session and SQLAlchemy models
│   │   ├── repositories/                   # Repository layer placeholders
│   │   ├── schemas/                        # Pydantic request/response schemas
│   │   ├── services/                       # Business logic modules
│   │   ├── tasks/                          # Background task placeholders
│   │   ├── tests/                          # Test placeholders
│   │   └── websocket/                      # Realtime event and handler placeholders
│   └── requirements.txt
│
├── docker/                                 # Dockerfiles   
├── frontend/                               # Frontend
├── k6/                                     #Load test
├── nginx/                                  # Nginx placeholder
├── scripts/                                # Utility script
│
├── docker-compose.yml
├── docker-compose.dev.yml
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

## Implemented API Modules

### Authentication

```text
POST /api/auth/signup
POST /api/auth/login
```

### Users

```text
GET /api/user
GET /api/user/{user_id}
GET /api/user/email/{email}
GET /api/user/username/{username}
```

### Restaurants

```text
POST   /api/restaurant
GET    /api/restaurant/{restaurant_id}
PUT    /api/restaurant/{restaurant_id}
PATCH  /api/restaurant/{restaurant_id}/status
DELETE /api/restaurant/{restaurant_id}
```

### Menu

```text
POST   /api/menus
GET    /api/menus/{menu_id}
GET    /api/restaurants/{restaurant_id}/menus
PUT    /api/menus/{menu_id}
PATCH  /api/menus/{menu_id}/status
DELETE /api/menus/{menu_id}
```

### Orders

```text
POST   /api/order
GET    /api/order/{order_id}
GET    /api/order/all
PATCH  /api/order/{order_id}/status
DELETE /api/order/{order_id}
```

### Payments

```text
POST   /api/order/{order_id}/payment
GET    /api/order/{order_id}/payment

GET    /api/payment/all
GET    /api/payment/{payment_id}

PATCH  /api/payment/{payment_id}/status
```

### Delivery Partners

```text
POST   /api/delivery_partner

GET    /api/delivery_partner/{partner_id}
GET    /api/delivery_partner/user/{user_id}
GET    /api/delivery_partner/all

PUT    /api/delivery_partner/{partner_id}
PUT    /api/delivery_partner/{partner_id}/location

DELETE /api/delivery_partner/{partner_id}
```

### Notifications

```text
GET    /api/notification
GET    /api/notification/{notification_id}

PATCH  /api/notification/{notification_id}/read
PATCH  /api/notification/read-all

DELETE /api/notification/{notification_id}
```

### Admin Notifications

```text
GET /api/admin/notification/all
GET /api/admin/notification/user/{user_id}
```

### Health

```text
GET /api/health
```

---

## Environment Variables

Create:

```text
backend/.env
```

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

For local development:

```env
ENV=dev
```

---

## Running with Docker

```bash
docker compose up --build
```

API:

```text
http://localhost:8003
```

Database:

```text
127.0.0.1:3010
```

Development environment:

```bash
docker compose -f docker-compose.dev.yml up --build
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
uvicorn backend.app.main:app --reload
```

---

## Current Development Status

### Completed

* Async SQLAlchemy setup
* MySQL integration
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
* Notification management
* Health monitoring endpoints
* Docker configuration
* OpenAPI / Swagger documentation

### In Progress

* Order tracking workflows
* WebSocket support
* Background task processing
* Frontend application

### Planned

* pytest test suite
* k6 load testing
* Redis integration
* Real-time order tracking
* Analytics dashboard
* CI/CD pipeline
* Production deployment

---

## Development Notes

* Database tables are currently initialized during application startup.
* Alembic migrations should replace automatic table creation before production deployment.
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
