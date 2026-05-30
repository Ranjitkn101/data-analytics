
-- Transform RAW → CLEANSED (Silver Layer)
CREATE OR REPLACE TABLE `pro-bigquery-cloud-analytics.ds_bigquery_cloud_analytics.sales_cleansed` AS
WITH source AS (
    SELECT
        SAFE_CAST(order_id AS INT64) AS order_id,
        NULLIF(TRIM(customer_id), '') AS customer_id,
        SAFE_CAST(amount AS NUMERIC) AS amount,
        SAFE_CAST(quantity AS INT64) AS quantity,

        -- Handle multiple date formats safely
        CASE
            WHEN REGEXP_CONTAINS(order_date, r'^\d{4}-\d{2}-\d{2}$')
                THEN SAFE.PARSE_DATE('%Y-%m-%d', order_date)

            WHEN REGEXP_CONTAINS(order_date, r'^\d{2}-\d{2}-\d{4}$')
                THEN SAFE.PARSE_DATE('%d-%m-%Y', order_date)

            WHEN REGEXP_CONTAINS(order_date, r'^\d{4}/\d{2}/\d{2}$')
                THEN SAFE.PARSE_DATE('%Y/%m/%d', order_date)

            WHEN REGEXP_CONTAINS(order_date, r'^[A-Za-z]+ \d{1,2} \d{4}$')
                THEN SAFE.PARSE_DATE('%B %d %Y', order_date)

            ELSE NULL
        END AS order_date,

        CURRENT_TIMESTAMP() AS processed_at
    FROM `pro-bigquery-cloud-analytics.ds_bigquery_cloud_analytics.sales_raw`
),

cleaned AS (
    SELECT *
    FROM source
    WHERE order_id IS NOT NULL
      AND customer_id IS NOT NULL
      AND amount IS NOT NULL
      AND quantity IS NOT NULL
      AND order_date IS NOT NULL
      AND order_id > 0
      AND amount >= 0
      AND quantity >= 0
),

deduped AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY processed_at DESC) AS rn
    FROM cleaned
)

SELECT
    order_id,
    customer_id,
    amount,
    quantity,
    order_date,
    processed_at
FROM deduped
WHERE rn = 1;
