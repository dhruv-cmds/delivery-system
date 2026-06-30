# Architecture

This document describes the overall architecture, design principles, and request lifecycle of the Food Delivery Management System.

---

# System Overview

The application follows a layered architecture to keep business logic, API routes, and data access cleanly separated. This improves maintainability, scalability, and testability while making it easier to extend the project with new features.

```text
                   Client
                      │
              HTTP / JSON Requests
                      │
              FastAPI Application
                      │
      ┌───────────────┼────────────────┐
      │               │                │
 Authentication   Middleware      API Routes
      │               │                │
      └───────────────┼────────────────┘
                      │
               Service Layer
                      │
             Repository Layer
               │             │
               │             │
      SQLAlchemy ORM     Redis Cache
               │             ▲
               └──────┬──────┘
                      │
                    MySQL
```

---

# Request Lifecycle

The following illustrates the lifecycle of a typical API request.

```text
Client
   │
   ▼
FastAPI Router
   │
   ▼
Authentication Middleware
   │
   ▼
Authorization (RBAC)
   │
   ▼
Request Validation (Pydantic)
   │
   ▼
Service Layer
   │
   ▼
Repository / Database Access
   │
   ├────────► Redis Cache
   │
   ▼
MySQL Database
   │
   ▼
Business Logic Processing
   │
   ▼
Response Serialization
   │
   ▼
Client
```

Each layer has a single responsibility, reducing coupling between application components.

---

# Design Principles

The project is built around several architectural principles:

- Async-first backend design
- Layered service architecture
- Separation of concerns
- Repository pattern for data access
- Configuration-driven business rules
- Stateless JWT authentication
- Redis-backed caching
- Production-ready Docker deployment

---

# Project Layers

The API layer exposes REST endpoints using FastAPI.

Responsibilities include:

- Request validation
- Response serialization
- Dependency injection
- Authentication
- Authorization
- HTTP status handling

Business logic is intentionally kept out of the route handlers.

---

## Service Layer

The Service Layer contains the application's business logic.

Responsibilities include:

* Validation
* Ownership checks
* Business rules
* Cache management
* Database coordination
* Exception handling

Example responsibilities:

* Creating orders
* Updating payment status
* Assigning delivery partners
* Sending notifications

---

## Repository Layer

The Repository Layer handles communication with the database.

Responsibilities include:

- CRUD operations
- Query abstraction
- Data persistence
- Database interaction

Separating repositories from services makes testing significantly easier.

---

## Database Layer

Persistent data is stored in MySQL using SQLAlchemy 2.x Async ORM.

Current entities include:

- delivery_partners
- menu_items
- notifications
- order_items
- order_tracking
- orders
- payments
- restaurants
- users

Relationships are implemented using SQLAlchemy ORM with foreign key constraints and ownership validation.

---

## Cache Layer

Redis is used to improve performance by reducing unnecessary database queries.

Current responsibilities include:

- Frequently accessed data caching
- Shared infrastructure support
- Future session and rate-limiting extensions

---

# Domain Model

The system currently contains the following entities.

| Entity           | Description                   |
| ---------------- | ----------------------------- |
| User             | Application users             |
| Restaurant       | Restaurant information        |
| Menu Item        | Restaurant menu items         |
| Order            | Customer orders               |
| Order Item       | Individual order items        |
| Payment          | Payment transactions          |
| Delivery Partner | Delivery personnel            |
| Order Tracking   | Delivery tracking information |
| Notification     | User notifications            |

Relationships are implemented using SQLAlchemy ORM with proper foreign key constraints.

---

# Core Components

## Authentication

Authentication is implemented using JWT tokens.

Features include:

- User signup
- User login
- Password hashing using bcrypt
- Protected routes
- JWT access tokens

---

## Authorization

Role-Based Access Control (RBAC) protects privileged endpoints.

Supported roles include:

- Customer
- Delivery partner
- Admin
- Restaunrat owner

Administrative operations are restricted to authorized users.

---

## Restaurant Module

Responsibilities:

* Restaurant CRUD
* Status updates
* Ownership validation
* Cache refresh

---

## Menu Module

Responsibilities:

* Menu item CRUD
* Availability updates
* Restaurant ownership validation
* Cache management

---

## Order Module

Responsibilities:

* Order creation
* Order updates
* Status transitions
* Customer ownership checks
* Restaurant visibility
* Delivery visibility

---

## Payment Module

Responsibilities:

* Payment creation
* Payment lookup
* Payment history
* Status synchronization
* Order payment updates

---

## Delivery Module

Responsibilities:

* Partner registration
* Location updates
* Delivery assignments
* Profile management

---

## Notification Module

Responsibilities:

* Notification creation
* Read status updates
* Administrative access
* User notifications

---

## Administration

Administrative functionality includes:

- View all users
- View all accounts
- Close accounts
- Protected admin endpoints

---

# Business Rules

The application enforces several validation rules to maintain data integrity.

Examples include:

- Prevent negative payment amounts.
- Prevent payments that exceed the configured maximum amount.
- Prevent self-transfers between accounts.
- Allow only **ACTIVE** customers to place orders.
- Enforce a maximum number of items per order.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| API | FastAPI |
| ORM | SQLAlchemy 2.x Async |
| Database | MySQL |
| Cache | Redis |
| Authentication | JWT |
| Authorization | RBAC |
| Password Hashing | bcrypt + passlib |
| Validation | Pydantic |
| Containerization | Docker |

---

# Architecture Highlights

- Fully asynchronous request handling
- Layered service architecture
- Repository pattern
- JWT-secured API
- RBAC authorization
- Async SQLAlchemy integration
- Redis caching support
- Dockerized infrastructure
- Production-ready deployment design
- Configuration-driven business rules

---

# Caching Strategy

The application implements the Cache-Aside pattern.

```text
                Client
                   │
                   ▼
                FastAPI
                   │
                   ▼
            Check Redis Cache
             │            │
         Cache Hit    Cache Miss
             │            │
             ▼            ▼
        Return Data    Query MySQL
                           │
                           ▼
                    Store in Redis
                           │
                           ▼
                      Return Data
```

After updates or deletions, cached entries are refreshed or invalidated to ensure consistency.

---

# Future Improvements

The architecture is designed to support future enhancements, including:

- Background task queues
- Horizontal scaling
- Database replication
- Distributed caching
- Event-driven architecture
- Observability with Grafana and Prometheus

---

# Related Documentation

- `README.md`
- `docs/docker.md`
- `docs/deployment.md`
- `docs/security.md`
- `docs/testing.md`
- `docs/load-testing.md`
- `docs/performance.md`