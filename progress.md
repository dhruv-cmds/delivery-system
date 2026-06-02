# Project Progress

Last updated: 2026-06-03

## Summary

The Delivery System project currently has a backend-first foundation. The database model layer, Pydantic schemas, core security helpers, custom exceptions, dependency wiring, API route handlers for auth/users/health/menu, and several business services have been added. The project also has Docker Compose support for the API and MySQL database.

The main remaining work is to connect the remaining service modules through FastAPI route handlers, add database migrations or a safer initialization flow, write tests, and build the frontend/realtime/load-testing layers.

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
- Added FastAPI app entrypoint that registers auth, user, health, and menu routers.
- Added API dependency helpers for database sessions, JWT-authenticated users, admin access, and menu manager access.
- Added `RESTAURANT_OWNER` user role for restaurant/menu ownership flows.

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
- Order menu item validation and customer-scoped order lookup.
- Single-item order creation, order item updates, status updates, and order deletion with checks for delivered, cancelled, and other final states.
- Order creation guards for maximum item quantity and maximum order value.
- Payment creation for orders, payment lookup by payment id and order id, and admin payment status updates that sync the related order payment status.

### API Routes

Implemented API route handlers for:

- Auth signup and login.
- User lookup by id, email, and username.
- Admin-only user listing.
- Health check with database connectivity.
- Menu item creation, lookup by menu id, listing by restaurant id, update, delete, and status changes.

Menu management is restricted to admins and restaurant owners. Customer users are promoted to restaurant owners when they create a restaurant.

## Current Placeholders

These files or areas exist but still need implementation:

- `backend/app/lifespan.py`
- `backend/app/api/routes/restaurants.py`
- `backend/app/api/routes/orders.py`
- `backend/app/api/routes/payment.py`
- `backend/app/api/routes/tracking.py`
- `backend/app/api/routes/websocket.py`
- `backend/app/repositories/*.py`
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

- Restaurant, order, payment, tracking, and websocket API route modules still need to be completed and registered.
- Menu routes currently use overlapping `"/id/{...}"` paths for menu id and restaurant id lookups, so the restaurant-scoped listing path should be renamed.
- Order service currently handles a single menu item per order. Multi-item order creation and richer order lifecycle handling still need to be designed.
- Payment service is implemented, but it still needs API route integration and tests.
- `backend/app/main.py` currently drops and recreates all tables during startup, which should be replaced before any persistent environment is used.
- Tests are not implemented yet.

## Recommended Next Milestones

1. Replace startup table recreation with migrations or a safer initialization flow.
2. Fix the overlapping menu lookup route paths.
3. Add route handlers for restaurants, notifications, orders, and payments.
4. Add minimal service and API tests for auth, user, restaurant, menu, notifications, and orders.
5. Expand order creation to support multi-item carts if that is part of the intended API.
6. Add payment route handlers and service tests.
7. Implement delivery tracking and live location updates.
8. Add websocket connection management and event broadcasting.
9. Add seed data and admin creation scripts.
10. Add k6 scripts after endpoints stabilize.
11. Start frontend implementation after backend API contracts are stable.

## Recent Git Progress

Recent commits show progress in this order:

- Added menu routes and restaurant owner permissions.
- Added auth and user API routes.
- Completed payment service functions for create, lookup, and status updates.
- Added order creation limits for quantity and total transfer amount.
- Split order lookup helpers into an order query service.
- Added order service flow for create, update, status changes, and deletion.
- Added backend environment example.
- Updated project docs and backend setup notes.
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
