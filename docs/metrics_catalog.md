# HR Analytics Metrics Catalog

This catalog documents the curated SQL views and equivalent Python helpers exposed by the project. Each artefact is safe for direct consumption in BI tools.

## Gender & Diversity
- **`vw_hr_gender_breakdown` / `analytics.gender_breakdown`**  
  Headcount split by gender for employees aged 18+. Null or undisclosed genders surface explicitly.

- **`vw_hr_race_breakdown` / `analytics.race_breakdown`**  
  Employee distribution across race/ethnicity categories, sorted descending by headcount.

## Age Composition
- **`vw_hr_age_range` / `analytics.age_distribution()['range']`**  
  Youngest and oldest employee ages.

- **`vw_hr_age_by_decade` / `analytics.age_distribution()['by_decade']`**  
  Headcount aggregated into 10-year buckets (18–24, 25–34, ...).

- **`vw_hr_age_bands` & `vw_hr_age_gender` / `analytics.age_gender_breakdown`**  
  Power BI-friendly banding with optional gender cross-tab for workforce planning.

## Workforce Distribution
- **`vw_hr_location_split` / `analytics.location_distribution`**  
  Headquarters vs. remote distribution by `location`.

- **`vw_hr_state_distribution` / `analytics.location_state_distribution`**  
  Headcount by US state (or country subdivision).

- **`vw_hr_jobtitle_distribution` / `analytics.jobtitle_distribution`**  
  Role mix sorted by headcount.

## Tenure & Turnover
- **`vw_hr_terminated_avg_tenure` / `analytics.average_terminated_tenure`**  
  Average tenure in years for terminated employees (up to current date).

- **`vw_hr_department_turnover` / `analytics.department_turnover`**  
  Department-level active vs. terminated counts and turnover rate.

- **`vw_hr_department_tenure` / `analytics.department_tenure_distribution`**  
  Average tenure in years for terminated employees by department.

## Headcount Momentum
- **`vw_hr_headcount_trend` / `analytics.employee_count_over_time`**  
  Year-over-year hires, terminations, net change, and percent change for high-level reporting.

## Validation Signals
Python pipeline consumers also receive structured validation messages (duplicate IDs, chronology issues, age bounds) to feed data-quality dashboards or automated alerts.
