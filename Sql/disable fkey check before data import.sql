
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE payment_splits;
TRUNCATE TABLE customer_sales;
TRUNCATE TABLE users;
TRUNCATE TABLE branches;


SET FOREIGN_KEY_CHECKS = 1;


select * from users;