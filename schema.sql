CREATE DATABASE IF NOT EXISTS exchange_db;
USE exchange_db;

CREATE TABLE IF NOT EXISTS exchange_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    currency VARCHAR(10) NOT NULL,
    rate DECIMAL(10, 4) NOT NULL,
    base_currency VARCHAR(10) NOT NULL,
    date DATE NOT NULL
);
