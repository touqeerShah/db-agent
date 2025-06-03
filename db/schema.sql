-- Table: vendors
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    address TEXT
);

-- Table: customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT
);

-- Table: products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    vendor_id INTEGER REFERENCES vendors(id),
    purchase_price DECIMAL(10, 2),
    selling_price DECIMAL(10, 2),
    stock_quantity INTEGER DEFAULT 0,
    warranty_period_months INTEGER DEFAULT 0  -- Warranty duration
);

-- Table: bills (represents customer bills/invoices)
CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    bill_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(12, 2),
    payment_status VARCHAR(50) DEFAULT 'Pending'  -- Paid, Pending, Overdue, etc.
);

-- Table: sales (sales made to customers)
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bills(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_at_sale DECIMAL(10, 2),
    sale_date DATE DEFAULT CURRENT_DATE
);

-- Table: product_warranty_status (tracks warranty per product sold)
CREATE TABLE product_warranty_status (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(id) ON DELETE CASCADE,
    warranty_start_date DATE NOT NULL,
    warranty_end_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Active'  -- Active, Expired, Claimed
);

-- Table: vendor_purchases (records purchases from vendors)
CREATE TABLE vendor_purchases (
    id SERIAL PRIMARY KEY,
    vendor_id INTEGER REFERENCES vendors(id),
    product_id INTEGER REFERENCES products(id),
    purchase_date DATE NOT NULL DEFAULT CURRENT_DATE,
    quantity INTEGER NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * purchase_price) STORED,
    payment_status VARCHAR(50) DEFAULT 'Unpaid'  -- Unpaid, Partial, Paid
);

-- Table: vendor_payments (records payments made to vendors)
CREATE TABLE vendor_payments (
    id SERIAL PRIMARY KEY,
    vendor_id INTEGER REFERENCES vendors(id),
    purchase_id INTEGER REFERENCES vendor_purchases(id) ON DELETE SET NULL,
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    amount_paid DECIMAL(12, 2) NOT NULL,
    payment_method VARCHAR(50),  -- e.g., Bank Transfer, Cash, Cheque
    note TEXT
);


CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL,                      -- e.g., 'admin', 'employee', 'customer'
    table_name VARCHAR(100) NOT NULL,               -- e.g., 'vendors', 'customers', 'inventory'
    can_select BOOLEAN DEFAULT FALSE,
    can_insert BOOLEAN DEFAULT FALSE,
    can_update BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE
);

INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Soto Ltd', 'ugarcia@peterson.com', '+1-971-001-5445x257', '54427 Jason Burgs
Susanmouth, VT 05087');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Green-Villarreal', 'lucas78@hotmail.com', '741.741.0926', 'PSC 3341, Box 2452
APO AP 26552');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Martinez, Castillo and Baker', 'cnavarro@gmail.com', '838.984.8837x664', '938 Megan Island
West Williamborough, VT 78149');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Powell-Williams', 'susan39@fox.biz', '001-565-928-8938x7592', '1760 Justin Vista Apt. 025
Port Elizabeth, MS 70295');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Miller-Fernandez', 'butlerbrittany@cox-gilbert.org', '627-490-1119', '012 Kelly Walks Suite 341
Lake Gabriella, MA 27656');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Bauer, Cruz and Stevens', 'adamsmith@wallace-estes.com', '+1-448-058-6304x9192', '420 Elizabeth Plaza Apt. 479
Sullivanchester, SD 65946');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Bernard-Jones', 'christopherrussell@gmail.com', '001-551-567-7613x9146', '15189 Jimmy Via
South Emily, VA 45919');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Rose-Williamson', 'johnbarnes@hotmail.com', '001-482-842-4245x274', '2713 Cooper Ranch
Mullentown, NM 71474');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Lee, Jackson and Nelson', 'paulbranch@gmail.com', '(546)133-4002', '847 Robinson Roads
Michaelbury, OH 09656');
INSERT INTO vendors (name, contact_email, contact_phone, address) VALUES ('Walters, Miller and Odom', 'wsmith@hotmail.com', '(778)281-5631x52235', '329 Martinez Oval Suite 550
Brittanyshire, FL 97592');
INSERT INTO customers (name, email, phone, address) VALUES ('Elizabeth Acevedo', 'atanner@weeks.com', '001-276-072-3204', 'PSC 8241, Box 4664
APO AP 74807');
INSERT INTO customers (name, email, phone, address) VALUES ('Holly Bailey', 'williamthompson@johnson.net', '001-632-160-7930x0325', '0079 Santos Spur Suite 251
Mclaughlintown, AK 01470');
INSERT INTO customers (name, email, phone, address) VALUES ('Deborah Morris', 'robert00@yahoo.com', '+1-794-887-9869x8105', '837 Deborah Viaduct
Port Amberside, MO 77424');
INSERT INTO customers (name, email, phone, address) VALUES ('Jennifer Fuller', 'nmiller@hicks-jackson.biz', '356-355-2554x240', '0994 Robert Club Suite 697
Lake Thomas, IA 59808');
INSERT INTO customers (name, email, phone, address) VALUES ('Shelley Russell', 'raybennett@gmail.com', '821.403.7192x9467', '901 Crawford Club Apt. 155
South Fredborough, LA 87475');
INSERT INTO customers (name, email, phone, address) VALUES ('Ronnie Jacobs', 'walkervicki@miller.info', '657.013.7297x6168', '96843 Bonilla Ridges Apt. 860
East James, DC 73680');
INSERT INTO customers (name, email, phone, address) VALUES ('Melanie Taylor', 'michele84@rose.info', '764.700.3119', '060 Joseph Street
East Christina, VA 83424');
INSERT INTO customers (name, email, phone, address) VALUES ('Charles Dixon', 'hernandezchad@gmail.com', '001-588-283-3659x89032', '464 Christopher Parkway
Rachelland, MA 20751');
INSERT INTO customers (name, email, phone, address) VALUES ('Randall Guerrero', 'greenekathryn@cantrell.biz', '390-980-6198x213', '699 Brandon Square
New Travisberg, ID 11017');
INSERT INTO customers (name, email, phone, address) VALUES ('Kelly Walker', 'thomasjohnson@pope.org', '315-107-2459', '82502 Jennifer Corners Apt. 673
South Joseph, AK 31803');
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Court Tan', 'SKU1000', 5, 51.56, 381.85, 100, 24);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Whose LightGreen', 'SKU1001', 5, 79.92, 383.47, 37, 12);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Fight LightSlateGray', 'SKU1002', 1, 60.71, 209.74, 10, 6);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Maintain GoldenRod', 'SKU1003', 6, 71.57, 314.66, 84, 6);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Strong Indigo', 'SKU1004', 7, 54.27, 369.67, 65, 12);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Very LightSalmon', 'SKU1005', 10, 113.76, 324.59, 54, 6);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Never YellowGreen', 'SKU1006', 3, 101.27, 260.16, 91, 6);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Base DarkGreen', 'SKU1007', 3, 66.69, 350.98, 79, 6);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Carry LightPink', 'SKU1008', 9, 55.66, 369.09, 23, 24);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Space Chocolate', 'SKU1009', 1, 129.36, 282.26, 59, 12);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Quite Orange', 'SKU1010', 9, 118.64, 265.21, 57, 6);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Key Maroon', 'SKU1011', 6, 92.97, 226.04, 78, 24);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Consider Gray', 'SKU1012', 4, 80.04, 358.85, 61, 12);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Once Magenta', 'SKU1013', 5, 83.47, 336.6, 95, 12);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Watch PaleGreen', 'SKU1014', 9, 105.96, 339.48, 38, 12);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Contain Chartreuse', 'SKU1015', 8, 71.64, 371.6, 79, 24);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Story LightGray', 'SKU1016', 5, 75.44, 242.91, 100, 24);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Agent MediumVioletRed', 'SKU1017', 8, 68.19, 214.31, 98, 12);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('Sport DimGray', 'SKU1018', 6, 90.67, 334.18, 91, 24);
INSERT INTO products (name, sku, vendor_id, purchase_price, selling_price, stock_quantity, warranty_period_months) VALUES ('State DeepSkyBlue', 'SKU1019', 2, 65.75, 344.89, 90, 6);
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (2, '2024-09-08', 1499.7, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (2, '2025-02-27', 311.34, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (9, '2024-11-19', 1223.73, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (3, '2024-09-17', 1196.01, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (5, '2024-10-15', 1160.31, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (5, '2024-12-09', 420.3, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (8, '2024-12-26', 1197.96, 'Paid');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (1, '2025-03-24', 1370.36, 'Paid');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (1, '2024-09-08', 552.02, 'Overdue');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (9, '2024-09-02', 675.52, 'Overdue');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (2, '2024-09-11', 554.78, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (1, '2025-04-08', 875.54, 'Pending');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (7, '2024-07-28', 893.42, 'Paid');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (9, '2025-05-28', 1114.23, 'Overdue');
INSERT INTO bills (customer_id, bill_date, total_amount, payment_status) VALUES (2, '2025-04-16', 795.75, 'Paid');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (6, 20, 3, 332.73, '2024-06-18');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (15, 6, 5, 305.78, '2025-02-10');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (2, 5, 2, 389.04, '2025-04-14');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (4, 10, 1, 244.43, '2025-03-30');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (10, 2, 2, 343.1, '2024-06-06');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (13, 15, 5, 256.12, '2024-10-21');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (5, 18, 2, 398.69, '2025-05-06');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (3, 2, 3, 252.78, '2025-04-25');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (5, 11, 5, 227.48, '2025-04-27');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (15, 14, 4, 320.49, '2025-02-24');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (7, 19, 1, 328.96, '2025-03-28');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (10, 5, 1, 351.44, '2025-01-17');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (15, 4, 3, 372.32, '2024-09-16');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (10, 19, 3, 338.06, '2025-03-02');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (6, 8, 1, 355.72, '2025-01-09');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (13, 8, 5, 237.47, '2024-07-21');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (4, 6, 4, 265.72, '2024-08-25');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (4, 9, 5, 329.74, '2024-10-11');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (15, 16, 4, 323.09, '2024-07-20');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (7, 10, 4, 229.48, '2024-08-10');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (12, 5, 2, 381.28, '2024-08-23');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (12, 3, 4, 284.81, '2024-06-10');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (9, 4, 3, 304.89, '2024-07-17');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (2, 20, 2, 245.08, '2025-02-14');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (1, 19, 2, 271.17, '2025-02-03');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (8, 1, 2, 386.25, '2024-08-01');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (8, 11, 4, 200.44, '2024-11-26');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (1, 5, 2, 254.1, '2024-12-11');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (15, 5, 3, 300.52, '2024-10-16');
INSERT INTO sales (bill_id, product_id, quantity, price_at_sale, sale_date) VALUES (13, 1, 3, 317.19, '2025-01-02');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (1, '2024-09-01', '2026-09-01', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (2, '2025-04-06', '2025-10-06', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (3, '2025-04-18', '2026-04-18', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (4, '2024-06-08', '2026-06-08', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (5, '2025-04-09', '2027-04-09', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (6, '2024-12-12', '2026-12-12', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (7, '2025-04-06', '2027-04-06', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (8, '2024-11-23', '2026-11-23', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (9, '2024-12-02', '2026-12-02', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (10, '2024-08-04', '2026-08-04', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (11, '2024-12-24', '2026-12-24', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (12, '2024-07-09', '2025-07-09', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (13, '2025-05-16', '2027-05-16', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (14, '2024-09-14', '2025-03-14', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (15, '2025-05-27', '2025-11-27', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (16, '2024-11-17', '2026-11-17', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (17, '2025-03-28', '2027-03-28', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (18, '2024-12-25', '2025-06-25', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (19, '2025-01-19', '2027-01-19', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (20, '2024-12-24', '2026-12-24', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (21, '2024-06-03', '2026-06-03', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (22, '2025-03-05', '2025-09-05', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (23, '2025-03-24', '2026-03-24', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (24, '2024-07-28', '2025-01-28', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (25, '2025-04-04', '2027-04-04', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (26, '2025-02-02', '2027-02-02', 'Expired');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (27, '2024-10-31', '2025-04-30', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (28, '2025-04-23', '2025-10-23', 'Active');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (29, '2024-08-09', '2026-08-09', 'Claimed');
INSERT INTO product_warranty_status (sale_id, warranty_start_date, warranty_end_date, status) VALUES (30, '2024-12-12', '2026-12-12', 'Active');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (2, 4, '2024-08-21', 16, 148.1, 'Partial');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (3, 15, '2025-04-01', 18, 68.0, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (9, 20, '2024-07-11', 12, 71.26, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (7, 11, '2024-09-28', 11, 149.19, 'Paid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (5, 11, '2024-09-14', 6, 125.6, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (9, 14, '2024-09-05', 5, 94.55, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (5, 13, '2024-07-05', 19, 52.68, 'Partial');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (9, 7, '2025-02-08', 11, 73.15, 'Paid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (7, 18, '2025-02-22', 20, 60.95, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (7, 10, '2024-07-14', 11, 108.94, 'Partial');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (7, 18, '2024-08-11', 18, 61.79, 'Paid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (1, 12, '2025-05-16', 5, 58.95, 'Paid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (2, 11, '2025-01-19', 20, 138.32, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (8, 13, '2025-05-01', 20, 67.0, 'Partial');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (8, 20, '2024-09-11', 18, 132.17, 'Paid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (6, 15, '2024-08-30', 11, 104.99, 'Partial');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (9, 16, '2024-08-13', 16, 102.14, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (5, 11, '2024-06-01', 17, 137.02, 'Unpaid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (6, 5, '2025-04-08', 13, 65.1, 'Paid');
INSERT INTO vendor_purchases (vendor_id, product_id, purchase_date, quantity, purchase_price, payment_status) VALUES (2, 7, '2024-10-11', 12, 74.4, 'Unpaid');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (1, 6, '2024-07-28', 259.56, 'Bank Transfer', 'Payment note 1');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (7, 19, '2024-10-26', 217.63, 'Cash', 'Payment note 2');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (7, 9, '2025-05-12', 847.16, 'Bank Transfer', 'Payment note 3');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (10, 8, '2025-02-27', 462.63, 'Bank Transfer', 'Payment note 4');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (4, 6, '2024-06-18', 217.65, 'Cheque', 'Payment note 5');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (7, 1, '2024-11-24', 617.36, 'Cheque', 'Payment note 6');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (8, 5, '2025-05-15', 698.15, 'Cheque', 'Payment note 7');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (4, 11, '2024-08-14', 936.73, 'Bank Transfer', 'Payment note 8');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (2, 10, '2024-06-08', 905.15, 'Cheque', 'Payment note 9');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (4, 9, '2025-03-16', 978.59, 'Bank Transfer', 'Payment note 10');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (7, 20, '2024-11-11', 803.29, 'Bank Transfer', 'Payment note 11');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (5, 13, '2024-09-21', 165.53, 'Cash', 'Payment note 12');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (5, 16, '2024-10-23', 351.79, 'Cash', 'Payment note 13');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (7, 13, '2024-07-21', 143.52, 'Bank Transfer', 'Payment note 14');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (7, 7, '2024-10-17', 759.87, 'Bank Transfer', 'Payment note 15');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (10, 6, '2024-09-05', 638.42, 'Cheque', 'Payment note 16');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (3, 17, '2025-01-31', 196.2, 'Cheque', 'Payment note 17');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (4, 1, '2024-12-06', 461.49, 'Cheque', 'Payment note 18');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (1, 10, '2024-10-05', 501.5, 'Cash', 'Payment note 19');
INSERT INTO vendor_payments (vendor_id, purchase_id, payment_date, amount_paid, payment_method, note) VALUES (9, 8, '2024-12-03', 208.61, 'Cheque', 'Payment note 20');


-- Admin: full access
INSERT INTO permissions (role, table_name, can_select, can_insert, can_update, can_delete)
SELECT 'admin', table_name, TRUE, TRUE, TRUE, TRUE
FROM (VALUES
  ('vendors'), ('customers'), ('products'), ('bills'), 
  ('sales'), ('product_warranty_status'), ('vendor_purchases'), ('vendor_payments')
) AS t(table_name);

-- Employees: read access to inventory and customers
INSERT INTO permissions (role, table_name, can_select)
VALUES
  ('employee', 'products', TRUE),
  ('employee', 'customers', TRUE);

-- Customers: read-only access to inventory and their own purchase data
INSERT INTO permissions (role, table_name, can_select)
VALUES
  ('customer', 'products', TRUE),
  ('customer', 'sales', TRUE),
  ('customer', 'product_warranty_status', TRUE);
