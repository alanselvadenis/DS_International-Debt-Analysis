-- Create and use the database
CREATE DATABASE sales_management_system;
USE sales_management_system;


CREATE TABLE branches (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_name VARCHAR(100) NOT NULL,
    branch_admin_name VARCHAR(100) NOT NULL
);


CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    branch_id INT,
    role ENUM('Super Admin', 'Admin') NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);


CREATE TABLE customer_sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_id INT,
    date DATE NOT NULL,
    name VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(15) UNIQUE NOT NULL,
    product_name VARCHAR(30) NOT NULL,
    gross_sales DECIMAL(12,2) NOT NULL,
    received_amount DECIMAL(12,2) DEFAULT 0.00,
    -- pending_amount is a Generated Column that calculates automatically
    pending_amount DECIMAL(12,2) GENERATED ALWAYS AS (gross_sales - received_amount) STORED,
    status ENUM('Open', 'Close') NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);


CREATE TABLE payment_splits (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT,
    payment_date DATE NOT NULL,
    amount_paid DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL, -- Cash / UPI / Card
    FOREIGN KEY (sale_id) REFERENCES customer_sales(sale_id)
);