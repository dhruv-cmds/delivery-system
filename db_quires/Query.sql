-- Create database
CREATE DATABASE IF NOT EXISTS delivery;

-- =====================================================
-- Development Database Setup
-- Replace DB_PASSWORD_FROM_ENV with your own password.
-- Do NOT use production credentials.
-- =====================================================

-- Create application user
-- Set user name and user passowrd that you set in .env DB_PASSWORD nad DB_NAME
CREATE USER IF NOT EXISTS 'delivery_user'@'%'
IDENTIFIED BY 'DB_PASSWORD_FROM_ENV';

-- Grant full access to the delivery database
GRANT ALL PRIVILEGES ON delivery.* TO 'delivery_user'@'%';

-- Reload privilege tables
FLUSH PRIVILEGES;

-- Verify granted permissions
SHOW GRANTS FOR 'delivery_user'@'%';

-- Verify user exists
SELECT User, Host
FROM mysql.user
WHERE User = 'delivery_user';


-- =====================================================
-- Optional Maintenance Commands
-- Uncomment only if you know what you're doing
-- =====================================================

-- DROP DATABASE delivery;

USE delivery;

-- View data
SELECT * FROM delivery_partners;
SELECT * FROM menu_items;
SELECT * FROM notifications;
SELECT * FROM order_items;
SELECT * FROM order_tracking;
SELECT * FROM orders;
SELECT * FROM payments;
SELECT * FROM restaurants;
SELECT * FROM users;

-- Manually promote first user to ADMIN
UPDATE users
SET role = 'ADMIN'
WHERE id = 1;

-- Verify admin user
SELECT id, name, email, role
FROM users
WHERE id = 1;