# Project Progress

Last updated: 2026-05-29

## Summary

The Delivery System project currently has a backend-first foundation. The database model layer, Pydantic schemas, core security helpers, custom exceptions, and several business services have been added. The project also has Docker Compose support for the API and MySQL database.

The main remaining work is to connect these backend pieces through FastAPI route handlers, complete missing service modules, add database migrations or initialization flow, write tests, and build the frontend/realtime/load-testing layers.

## Completed So Far

### Project Setup

- Added backend, frontend, Docker, nginx, scripts, and k6 project folders.
- Added Docker Compose configuration for:
  - `delivery-api`
  - `delivery-db`
- Added a backend Dockerfile using Python 3.11 and Uvicorn.
- Added MIT license.

### Backend Core

- Added environment configuration through `backend/.env`.
- Added async MySQL database session setup using SQLAlchemy and aiomysql.
- Added password hashing and verification helpers.
- Added JWT access token creation.
- Added shared constants for user roles, order status, payment status, and limits.
- Added application logger.
- Added structured custom exceptions for users, auth, restaurants, menus, orders, payments, delivery partners, permissions, and database errors.

### Database Models

Implemented SQLAlchemy models for:

- `User`
- `Restaurant`
- `Menu`
- `Order`
- `OrderItem`
- `Payment`
- `DeliveryPartner`
- `OrderTracking`
- `Notification`

Relationships have been added across the main delivery workflow:

- Users own restaurants.
- Users place orders.
- Restaurants have menu items and orders.
- Orders have order items and tracking updates.
- Delivery partners can be assigned to orders.
- Users can receive notifications.

### Schemas

Added Pydantic schemas for:

- Auth login and token responses.
- Shared name, phone, email, and password constraints.
- Users.
- Restaurants.
- Menu items.
- Order items.
- Payments.
- Delivery partners.
- Notifications.
- Websocket subscribe, location update, and error payloads.

### Services

Implemented or partially implemented service-layer logic for:

- User creation and lookup.
- Signup and login.
- Restaurant creation, lookup, update, and deletion.
- Menu item creation, lookup, update, deletion, and status changes.
- Notification creation, listing, mark-as-read, and deletion.

## Current Placeholders

These files or areas exist but still need implementation:

- `backend/app/main.py`
- `backend/app/lifespan.py`
- `backend/app/api/routes/*.py`
- `backend/app/repositories/*.py`
- `backend/app/services/order_service.py`
- `backend/app/services/payment_service.py`
- `backend/app/services/tracking_service.py`
- `backend/app/services/websocket_service.py`
- `backend/app/services/redis_service.py`
- `backend/app/services/analytics_service.py`
- `backend/app/tasks/*.py`
- `backend/app/websocket/handlers/*.py`
- `backend/app/websocket/events/*.py`
- `backend/app/tests/*.py`
- `frontend/src/main.jsx`
- `k6/*.js`
- `nginx/nginx.conf`
- `scripts/*.py`
- `scripts/wait_for_db.sh`

## Known Issues To Fix

- API route files exist, but they are empty. This means the service functions are written, but no HTTP endpoints are available yet for Postman, a browser, or the frontend to call.
- Tests are not implemented yet.

## Recommended Next Milestones

1. Build the FastAPI app entrypoint in `backend/app/main.py`.
2. Add route handlers for auth, users, restaurants, menu, and notifications first because their services already exist.
3. Add database dependency and current-user authentication dependency.
4. Fix naming and schema issues that would currently break imports or validation.
5. Add minimal service tests for auth, user, restaurant, menu, and notifications.
6. Implement order creation and order item pricing.
7. Implement payment creation and payment status transitions.
8. Implement delivery tracking and live location updates.
9. Add websocket connection management and event broadcasting.
10. Add seed data and admin creation scripts.
11. Add k6 scripts after endpoints stabilize.
12. Start frontend implementation after backend API contracts are stable.

## Recent Git Progress

Recent commits show progress in this order:

- Added restaurant service and improved menu service.
- Fixed schema exports and added notification service.
- Added notification schema and cleaned schema/model spacing.
- Added menu service and improved auth/user type hints and username normalization.
- Added custom error exceptions.
- Added auth service with signup and login logic.
- Added user service and improved custom errors.
- Added websocket schema.
- Refactored delivery partner schemas.
- Added payment schema and increased payment method length.
