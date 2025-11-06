-- ============================================================================
-- 01_clean_hr_dataset.sql
-- Purpose : Recreate a clean, analytics-ready copy of the HR dataset.
-- Author  : Sebastian Gonzalez
-- Notes   : The script is idempotent and leaves the raw `hr` table untouched.
-- ============================================================================

CREATE DATABASE IF NOT EXISTS hr_osr;
USE hr_osr;

-- --------------------------------------------------------------------------
-- Helper function to normalise heterogenous date strings.
-- --------------------------------------------------------------------------
DROP FUNCTION IF EXISTS parse_date_flexible;
DELIMITER $$
CREATE FUNCTION parse_date_flexible(raw_value VARCHAR(50))
RETURNS DATE
DETERMINISTIC
BEGIN
    DECLARE candidate DATE;
    IF raw_value IS NULL OR TRIM(raw_value) = '' THEN
        RETURN NULL;
    END IF;

    SET candidate = STR_TO_DATE(raw_value, '%Y-%m-%d %H:%i:%s UTC');
    IF candidate IS NOT NULL THEN
        RETURN candidate;
    END IF;

    SET candidate = STR_TO_DATE(raw_value, '%Y-%m-%d');
    IF candidate IS NOT NULL THEN
        RETURN candidate;
    END IF;

    SET candidate = STR_TO_DATE(raw_value, '%m/%d/%Y');
    IF candidate IS NOT NULL THEN
        RETURN candidate;
    END IF;

    SET candidate = STR_TO_DATE(raw_value, '%m-%d-%Y');
    RETURN candidate;
END$$
DELIMITER ;

-- --------------------------------------------------------------------------
-- Step 0: Ensure the primary key column name is normalised.
-- --------------------------------------------------------------------------
ALTER TABLE hr
    CHANGE COLUMN `ï»¿id` employee_id VARCHAR(20) NULL;

-- --------------------------------------------------------------------------
-- Step 1: Rebuild the cleaned table in a single pass so that history and
--         auditing are preserved and we can re-run this script safely.
-- --------------------------------------------------------------------------
DROP TABLE IF EXISTS hr_clean;

CREATE TABLE hr_clean AS
SELECT
    TRIM(employee_id) AS employee_id,
    NULLIF(TRIM(first_name), '') AS first_name,
    NULLIF(TRIM(last_name), '') AS last_name,
    parse_date_flexible(birthdate) AS birthdate,
    parse_date_flexible(hire_date) AS hire_date,
    parse_date_flexible(NULLIF(termdate, '0000-00-00')) AS termdate,
    NULLIF(TRIM(gender), '') AS gender,
    NULLIF(TRIM(race), '') AS race,
    NULLIF(TRIM(department), '') AS department,
    NULLIF(TRIM(jobtitle), '') AS jobtitle,
    NULLIF(TRIM(location), '') AS location,
    NULLIF(TRIM(location_city), '') AS location_city,
    NULLIF(TRIM(location_state), '') AS location_state,
    TIMESTAMPDIFF(
        YEAR,
        parse_date_flexible(birthdate),
        CURRENT_DATE()
    ) AS age
FROM hr;

-- --------------------------------------------------------------------------
-- Step 2: Indexes optimise lookups for BI tools and reporting.
-- --------------------------------------------------------------------------
ALTER TABLE hr_clean
    ADD PRIMARY KEY (employee_id),
    ADD INDEX idx_hr_clean_department (department),
    ADD INDEX idx_hr_clean_location_state (location_state),
    ADD INDEX idx_hr_clean_termdate (termdate);

-- --------------------------------------------------------------------------
-- Step 3: Quality checks that can be monitored or exported to dashboards.
-- --------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_records,
    SUM(CASE WHEN birthdate IS NULL THEN 1 ELSE 0 END) AS missing_birthdate,
    SUM(CASE WHEN hire_date IS NULL THEN 1 ELSE 0 END) AS missing_hire_date,
    SUM(CASE WHEN age < 18 THEN 1 ELSE 0 END) AS underage_records
FROM hr_clean;

SELECT
    MIN(age) AS youngest_employee,
    MAX(age) AS oldest_employee
FROM hr_clean;
