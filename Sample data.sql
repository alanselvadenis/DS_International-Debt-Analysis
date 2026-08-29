
INSERT INTO branches (branch_name, branch_admin_name) VALUES 
('Chennai', 'Alan'),
('Delhi', 'Sabila'),
('Mumbai', 'Godwin');


INSERT INTO users (username, password, branch_id, role, email) VALUES 
('super_admin', 'hashed_pass_123', NULL, 'Super Admin', 'super@business.com'),
('alan_admin', 'hashed_pass_456', 1, 'Admin', 'alan@business.com'),
('sabila_admin', 'hashed_pass_789', 2, 'Admin', 'sabila@business.com');


INSERT INTO customer_sales (branch_id, date, name, mobile_number, product_name, gross_sales, status) VALUES 
(1, '2026-08-10', 'Nielsen Corp', '9876543210', 'FSD', 50000.00, 'Open'),
(1, '2026-08-12', 'Citi Bank', '9876543211', 'DS', 75000.00, 'Open'),
(2, '2026-08-15', 'Deutsche Bank', '9876543212', 'DA', 40000.00, 'Open'),
(3, '2026-08-18', 'Tech Corp', '9876543213', 'BA', 60000.00, 'Open');


INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES 
(1, '2026-08-11', 20000.00, 'UPI'),
(1, '2026-08-12', 15000.00, 'Card'); 


INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES 
(2, '2026-08-13', 75000.00, 'Card'); 


INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES 
(3, '2026-08-16', 10000.00, 'Cash');