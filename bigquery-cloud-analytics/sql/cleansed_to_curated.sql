-- Transform CLEANSED → CURATED (Gold Layer)
CREATE OR REPLACE TABLE `pro-bigquery-cloud-analytics.ds_bigquery_cloud_analytics.sales_curated` AS
WITH prepared AS (
    SELECT
        order_id,
        customer_id,
        amount,
        quantity,
        order_date,

        -- Ensure numeric multiplication
        SAFE_CAST(amount * quantity AS NUMERIC) AS total_order_value,

        -- Extract YYYY-MM safely
        FORMAT_DATE('%Y-%m', order_date) AS order_month,

        CASE
            WHEN amount >= 0 AND quantity >= 0 THEN 'VALID'
            ELSE 'REVIEW'
        END AS data_quality_flag,

        CURRENT_TIMESTAMP() AS curated_at
    FROM `pro-bigquery-cloud-analytics.ds_bigquery_cloud_analytics.sales_cleansed`
)

SELECT
    order_id,
    customer_id,
    amount,
    quantity,
    order_date,
    total_order_value,
    order_month,
    data_quality_flag,
    curated_at
FROM prepared;
