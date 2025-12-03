-- 1. Find the manager who oversees the department with the highest average product cost along with the department name and average cost.
WITH dept_averages AS (
    SELECT 
        dept_name,
        AVG(price) as avg_cost
    FROM product
    GROUP BY dept_name
)
SELECT 
    m.ID as manager_id,
    m.name as manager_name,
    d.name as department_name,
    da.avg_cost
FROM manager m
INNER JOIN department d ON m.ID = d.manager_ID
INNER JOIN dept_averages da ON d.name = da.dept_name
WHERE da.avg_cost = (SELECT MAX(avg_cost) FROM dept_averages);


-- 2. Find the lowest salary associate in each department along with their salary and department name.
 SELECT 
    a.name,
    a.salary,
    a.dept_name
FROM associate a
INNER JOIN (
    SELECT 
        dept_name,
        MIN(salary) as min_salary
    FROM associate
    GROUP BY dept_name
) dept_min ON a.dept_name = dept_min.dept_name 
           AND a.salary = dept_min.min_salary
ORDER BY a.dept_name;


-- 3. Find the most popular aisle for members based on purchase frequency in the last 3 months, along with the purchase count.
SELECT
    a.ID AS aisle_id,
    a.dept_name,
    COUNT(*) AS purchase_count
FROM purchase pur
JOIN product p ON pur.product_ID = p.ID
JOIN aisle a ON p.aisle_id = a.ID
WHERE pur.date_purchased >= date('now', '-3 months')
GROUP BY a.ID, a.dept_name
ORDER BY purchase_count DESC
LIMIT 1;


-- 4. Find the highest cost product that each supplier supplies, along with the supplier and product details.
SELECT 
    s.supplier_ID,
    s.name as supplier_name,
    s.phone_Number,
    p.ID as product_id,
    p.name as product_name,
    p.price as product_cost
FROM supplier s
INNER JOIN supplies sup ON s.supplier_ID = sup.supplier_ID
INNER JOIN product p ON sup.product_ID = p.ID
INNER JOIN (
    SELECT 
        sup.supplier_ID,
        MAX(p.price) as max_price
    FROM supplies sup
    INNER JOIN product p ON sup.product_ID = p.ID
    GROUP BY sup.supplier_ID
) max_products ON s.supplier_ID = max_products.supplier_ID 
               AND p.price = max_products.max_price
ORDER BY s.supplier_ID;


-- 5. Take the daily revenue and compare it to the revenue from the day before and give the difference as a percentage. 
WITH daily AS (
    SELECT 	
        pu.date_purchased,
        SUM(p.price * pu.quantity) AS revenue
    FROM purchase pu
    JOIN product p ON pu.product_ID = p.ID
    GROUP BY pu.date_purchased
)
SELECT
    date_purchased,
    revenue,
    LAG(revenue) OVER (ORDER BY date_purchased) AS prev_day,
    (revenue - LAG(revenue) OVER (ORDER BY date_purchased)) 
        / NULLIF(LAG(revenue) OVER (ORDER BY date_purchased), 0) AS pct_change
FROM daily;

