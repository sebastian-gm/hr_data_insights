-- ============================================================================
-- 02_hr_analytics_views.sql
-- Purpose : Publish reusable views that answer the core HR business questions.
-- Source  : hr_clean (prepared by 01_clean_hr_dataset.sql)
-- ============================================================================

USE hr_osr;

-- Shared adult workforce view ------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_adults AS
SELECT *
FROM hr_clean
WHERE age IS NULL OR age >= 18;

-- 1. Gender breakdown --------------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_gender_breakdown AS
SELECT
    gender,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY gender;

-- 2. Race/Ethnicity breakdown ------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_race_breakdown AS
SELECT
    race,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY race
ORDER BY employee_count DESC;

-- 3. Age distribution --------------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_age_range AS
SELECT
    MIN(age) AS youngest,
    MAX(age) AS oldest
FROM vw_hr_adults;

CREATE OR REPLACE VIEW vw_hr_age_by_decade AS
SELECT
    FLOOR(age / 10) * 10 AS age_decade,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY age_decade;

CREATE OR REPLACE VIEW vw_hr_age_bands AS
SELECT
    CASE
        WHEN age BETWEEN 18 AND 24 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        WHEN age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END AS age_band,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY age_band
ORDER BY age_band;

CREATE OR REPLACE VIEW vw_hr_age_gender AS
SELECT
    CASE
        WHEN age BETWEEN 18 AND 24 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        WHEN age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END AS age_band,
    gender,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY age_band, gender
ORDER BY age_band, gender;

-- 4. Headquarters vs remote --------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_location_split AS
SELECT
    location,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY location
ORDER BY employee_count DESC;

-- 5. Average tenure of terminated employees ----------------------------------
CREATE OR REPLACE VIEW vw_hr_terminated_avg_tenure AS
SELECT
    ROUND(AVG(DATEDIFF(termdate, hire_date)) / 365, 2) AS avg_tenure_years
FROM vw_hr_adults
WHERE termdate IS NOT NULL
  AND termdate <= CURDATE();

-- 6. Gender distribution by department ---------------------------------------
CREATE OR REPLACE VIEW vw_hr_department_gender AS
SELECT
    department,
    gender,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY department, gender
ORDER BY department, gender;

-- 7. Job title distribution ---------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_jobtitle_distribution AS
SELECT
    jobtitle,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY jobtitle
ORDER BY employee_count DESC;

-- 8. Department turnover -----------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_department_turnover AS
SELECT
    department,
    COUNT(*) AS total_count,
    SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) AS terminated_count,
    SUM(CASE WHEN termdate IS NULL OR termdate > CURDATE() THEN 1 ELSE 0 END) AS active_count,
    SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) / COUNT(*) AS turnover_rate
FROM vw_hr_adults
GROUP BY department
ORDER BY turnover_rate DESC;

-- 9. Distribution by state ---------------------------------------------------
CREATE OR REPLACE VIEW vw_hr_state_distribution AS
SELECT
    location_state,
    COUNT(*) AS employee_count
FROM vw_hr_adults
GROUP BY location_state
ORDER BY employee_count DESC;

-- 10. Headcount change over time ---------------------------------------------
CREATE OR REPLACE VIEW vw_hr_headcount_trend AS
SELECT
    YEAR(hire_date) AS calendar_year,
    COUNT(*) AS hires,
    SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) AS terminations,
    COUNT(*) - SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) AS net_change,
    ROUND(
        (
            COUNT(*) - SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END)
        ) / NULLIF(COUNT(*), 0),
        4
    ) AS net_change_percent
FROM vw_hr_adults
GROUP BY YEAR(hire_date)
ORDER BY calendar_year;

-- 11. Terminated employee tenure by department -------------------------------
CREATE OR REPLACE VIEW vw_hr_department_tenure AS
SELECT
    department,
    ROUND(AVG(DATEDIFF(termdate, hire_date)) / 365, 2) AS avg_tenure_years
FROM vw_hr_adults
WHERE termdate IS NOT NULL
  AND termdate <= CURDATE()
GROUP BY department;
