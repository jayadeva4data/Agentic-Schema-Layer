-- This dbt model transforms the raw ecommerce dataset into a cleaned and structured format.
-- The model is named 'ecommerce_dataset' to avoid conflicts with the raw source table.

WITH base AS (
    SELECT
        "userId" AS user_id,
        "productId" AS product_id,
        "Product Name" AS product_name,
        "Category" AS category,
        "Release Year" AS release_year,
        "User Rating" AS user_rating,
        "Average Rating" AS average_rating
    FROM
        {{ source('public', 'ecommerce_dataset_raw') }}
)

SELECT
    user_id,
    product_id,
    product_name,
    category,
    release_year,
    user_rating,
    average_rating
FROM
    base
