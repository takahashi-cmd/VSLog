DROP DATABASE myapp;
DROP USER 'testuser';

CREATE USER 'testuser'@'%' IDENTIFIED BY 'pass1234';
CREATE DATABASE myapp;
USE myapp;
GRANT ALL PRIVILEGES ON myapp.* TO 'testuser'@'%';
SET NAMES utf8mb4;

CREATE TABLE users(
    user_id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAUlT CURRENT_TIMESTAMP
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

