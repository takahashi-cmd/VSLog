DROP DATABASE myapp;
DROP USER 'testuser';

CREATE USER 'testuser'@'%' IDENTIFIED BY 'pass1234';
CREATE DATABASE myapp;
USE myapp;
GRANT ALL PRIVILEGES ON myapp.* TO 'testuser'@'%';
SET NAMES utf8mb4;

CREATE TABLE users(
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAUlT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE fields(
    field_id INT PRIMARY KEY,
    fieldname VARCHAR(20) NOT NULL,
    color_code VARCHAR(7) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAUlT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE study_logs(
    study_log_id INT PRIMARY KEY,
    study_date DATE NOT NULL,
    hours DECIMAL(6,1) NOT NULL,
    field_id INT NOT NULL,
    FOREIGN KEY (field_id) REFERENCES fields(field_id) ON DELETE CASCADE,
    content TEXT NULL,
    user_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



