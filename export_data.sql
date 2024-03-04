-- BUSINESS QUESTIONS

-- 1. Gender breakdown of employees
SELECT gender, COUNT(*) AS count
FROM hr
WHERE age >= 18
GROUP BY gender;

-- 2. Race/Ethnicity breakdown of employees
SELECT race, COUNT(*) AS count
FROM hr
WHERE age >= 18
GROUP BY race
ORDER BY count DESC;

-- 3. Age distribution of employees
-- Min and Max age
SELECT MIN(age) AS youngest, MAX(age) AS oldest
FROM hr
WHERE age >= 18;

-- Grouped by age range
SELECT FLOOR(age/10)*10 AS age_group, COUNT(*) AS count
FROM hr
WHERE age >= 18
GROUP BY age_group;


-- Grouped by specific age ranges
SELECT 
  CASE 
    WHEN age >= 18 AND age <= 24 THEN '18-24'
    WHEN age >= 25 AND age <= 34 THEN '25-34'
    WHEN age >= 35 AND age <= 44 THEN '35-44'
    WHEN age >= 45 AND age <= 54 THEN '45-54'
    WHEN age >= 55 AND age <= 64 THEN '55-64'
    ELSE '65+' 
  END AS age_group, 
  COUNT(*) AS count
FROM hr
WHERE age >= 18
GROUP BY age_group
ORDER BY age_group;

-- Breakdown by age group and gender
SELECT 
  CASE 
    WHEN age >= 18 AND age <= 24 THEN '18-24'
    WHEN age >= 25 AND age <= 34 THEN '25-34'
    WHEN age >= 35 AND age <= 44 THEN '35-44'
    WHEN age >= 45 AND age <= 54 THEN '45-54'
    WHEN age >= 55 AND age <= 64 THEN '55-64'
    ELSE '65+' 
  END AS age_group, gender,
  COUNT(*) AS count
FROM hr
WHERE age >= 18
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- 4. Employees at headquarters vs remote locations
SELECT location, COUNT(*) as count
FROM hr
WHERE age >=18
GROUP BY location;

-- 5. Average length of employment for terminated employees
SELECT ROUND(AVG(DATEDIFF(termdate, hire_date))/365,0) AS avg_length_of_employment
FROM hr
WHERE termdate IS NOT NULL AND termdate <= CURDATE() AND age >= 18;


-- 6. Gender distribution across departments
SELECT department, gender, COUNT(*) as count
FROM hr
WHERE age >= 18
GROUP BY department, gender
ORDER BY department;

-- 7. Distribution of job titles
SELECT jobtitle, COUNT(*) as count
FROM hr
WHERE age >= 18
GROUP BY jobtitle
ORDER BY count DESC;

-- 8. Department with the highest turnover rate
SELECT department, COUNT(*) as total_count, 
    SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) as terminated_count, 
    COUNT(*) - SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) as active_count,
    (SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) / COUNT(*)) as termination_rate
FROM hr
WHERE age >= 18
GROUP BY department
ORDER BY termination_rate DESC;


-- 9. Employee distribution across locations by state
SELECT location_state, COUNT(*) as count
FROM hr
WHERE age >= 18
GROUP BY location_state
ORDER BY count DESC;


-- 10. Company's employee count change over time
SELECT 
    YEAR(hire_date) AS year, 
    COUNT(*) AS hires, 
    SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) AS terminations, 
    COUNT(*) - SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END) AS net_change,
    ROUND(((COUNT(*) - SUM(CASE WHEN termdate IS NOT NULL AND termdate <= CURDATE() THEN 1 ELSE 0 END)) / COUNT(*) * 100),2) AS net_change_percent
FROM hr
WHERE age >= 18
GROUP BY YEAR(hire_date)
ORDER BY YEAR(hire_date) ASC;
    
    
-- 11. Tenure distribution for each department
SELECT department, ROUND(AVG(DATEDIFF(CURDATE(), termdate)/365),0) as avg_tenure
FROM hr
WHERE termdate IS NOT NULL AND termdate <= CURDATE() AND age >= 18
GROUP BY department;