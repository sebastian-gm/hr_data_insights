-- Create and use the hr_osr database
CREATE DATABASE IF NOT EXISTS hr_osr;
USE hr_osr;

select * from hr;

-- Modify the column name ï»¿id to emp_id with proper type and constraints
ALTER TABLE hr
CHANGE COLUMN `ï»¿id` emp_id VARCHAR(20) NULL;

-- Display the structure of the hr table
DESCRIBE hr;

-- Select birthdate from hr for review
SELECT birthdate FROM hr;

-- Disable safe updates for session to allow updates without a WHERE clause
SET sql_safe_updates = 0;

-- Update birthdate format to YYYY-MM-DD
UPDATE hr
SET birthdate = CASE
    WHEN birthdate LIKE '%/%' THEN DATE_FORMAT(STR_TO_DATE(birthdate, '%m/%d/%Y'),'%Y-%m-%d')
    WHEN birthdate LIKE '%-%' THEN DATE_FORMAT(STR_TO_DATE(birthdate, '%m-%d-%Y'),'%Y-%m-%d')
    ELSE NULL
END;

-- Change the type of birthdate to DATE
ALTER TABLE hr
MODIFY COLUMN birthdate DATE;


select birthdate from hr;


-- Repeat similar steps for hire_date
UPDATE hr
SET hire_date = CASE
    WHEN hire_date LIKE '%/%' THEN DATE_FORMAT(STR_TO_DATE(hire_date, '%m/%d/%Y'),'%Y-%m-%d')
    WHEN hire_date LIKE '%-%' THEN DATE_FORMAT(STR_TO_DATE(hire_date, '%m-%d-%Y'),'%Y-%m-%d')
    ELSE NULL
END;

ALTER TABLE hr
MODIFY COLUMN hire_date DATE;

-- Update termdate format and handle invalid dates
UPDATE hr
SET termdate = NULL
WHERE termdate = '0000-00-00' OR termdate = ' ';

UPDATE hr
SET termdate = DATE(STR_TO_DATE(termdate, '%Y-%m-%d %H:%i:%s UTC'))
WHERE termdate IS NOT NULL;

ALTER TABLE hr
MODIFY COLUMN termdate DATE;

-- Add an age column and calculate age
ALTER TABLE hr ADD COLUMN age INT;
UPDATE hr
SET age = TIMESTAMPDIFF(YEAR, birthdate, CURDATE());

-- Retrieve youngest and oldest age
SELECT MIN(age) AS youngest, MAX(age) AS oldest
FROM hr;

-- Count number of employees under 18
SELECT COUNT(*) FROM hr
WHERE age < 18;


-- Check remaining invalid termdate values if any
SELECT COUNT(*)
FROM hr
WHERE termdate IS NULL;

-- View updated hire_date and termdate columns
SELECT hire_date FROM hr;
SELECT termdate FROM hr;