-- ============================
-- Project: Retail Sales Performance Dashboard (SQL Script)
-- ============================

-- Create Table
CREATE TABLE sales_data (
    order_id VARCHAR(50),
    product VARCHAR(100),
    quantity INT,
    unit_price FLOAT,
    order_date DATE,
    region VARCHAR(50)
);

-- Sample Insert (remove or replace with real data load)
-- INSERT INTO sales_data (order_id, product, quantity, unit_price, order_date, region)
-- VALUES ('A001', 'Gadget', 10, 50.00, '2023-01-15', 'North');

-- Revenue, Cost & Profit by Region and Product
-- Assume estimated cost is 70% of unit price
SELECT
    region,
    product,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
    ROUND(SUM(quantity * unit_price * 0.7), 2) AS estimated_cost,
    ROUND(SUM(quantity * unit_price - quantity * unit_price * 0.7), 2) AS profit
FROM sales_data
GROUP BY region, product
ORDER BY region, product;

-- Monthly Sales and Profit Trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    ROUND(SUM(quantity * unit_price * 0.7), 2) AS cost,
    ROUND(SUM(quantity * unit_price - quantity * unit_price * 0.7), 2) AS profit
FROM sales_data
GROUP BY month
ORDER BY month;

-- Monthly Profit Heatmap Data
SELECT
    EXTRACT(YEAR FROM order_date) AS year,
    DATE_FORMAT(order_date, '%M') AS month_name,
    ROUND(SUM(quantity * unit_price - quantity * unit_price * 0.7), 2) AS profit
FROM sales_data
GROUP BY year, month_name
ORDER BY year, FIELD(month_name, 'January','February','March','April','May','June','July','August','September','October','November','December');

-- Region and Product-Wise Summary View 
CREATE VIEW region_product_summary AS
SELECT
    region,
    product,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    ROUND(SUM(quantity * unit_price - quantity * unit_price * 0.7), 2) AS profit
FROM sales_data
GROUP BY region, product;
