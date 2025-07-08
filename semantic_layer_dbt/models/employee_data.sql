{{ config(
    materialized='view'
) }}

WITH cleaned_data AS (

    SELECT
        "emp_id" AS employee_id,
        "frst_nm" AS first_name,
        "lst_nm" AS last_name,
        "gndr" AS gender,
        "dept" AS department,
        "salry" AS salary,
        -- Convert hire date to a date type
        TO_DATE("hre_dte", 'YYYY-MM-DD') AS hire_date,
        "loc" AS location

    FROM 
        {{ source('public', 'employee_data_raw') }}

)

SELECT
    employee_id,
    first_name,
    last_name,
    gender,
    department,
    salary,
    hire_date,
    location

FROM
    cleaned_data
