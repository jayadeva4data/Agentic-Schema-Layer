{{ config(
    materialized='view'
) }}

WITH base AS (
    SELECT
        "District_Name" AS district_name,
        "AcCode" AS ac_code,
        "ACName" AS ac_name,
        "Mandal_Name" AS mandal_name,
        "SECRETARIAT_CODE" AS secretariat_code,
        "SECRETARIAT_Name" AS secretariat_name,
        "CLUSTER_ID" AS cluster_id,
        "CLUSTER_NAME" AS cluster_name,
        "CITIZEN_NAME" AS citizen_name,
        "MOBILE" AS mobile,
        TO_DATE("DOB", 'YYYY-MM-DD') AS date_of_birth,
        "GENDER" AS gender,
        "SCHEME" AS scheme
    FROM {{ source('public', 'beneficiaries_raw') }}
)

SELECT
    district_name,
    ac_code,
    ac_name,
    mandal_name,
    secretariat_code,
    secretariat_name,
    cluster_id,
    cluster_name,
    citizen_name,
    mobile,
    date_of_birth,
    gender,
    scheme
FROM base
