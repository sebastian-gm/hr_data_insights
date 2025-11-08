# HR Workforce Intelligence Report

> For more of my projects and HR analytics work, connect with me on [LinkedIn](https://www.linkedin.com/in/sebastian-gonzalez-mendez/).

Table of Contents
- [Project Background](#project-background)
- [Executive Summary](#executive-summary)
- [Insights Deep-Dive](#insights-deep-dive)
  - [Workforce Composition](#workforce-composition)
  - [Tenure and Retention](#tenure-and-retention)
  - [Department Health](#department-health)
  - [Geographic Footprint](#geographic-footprint)
  - [Talent Pipeline Momentum](#talent-pipeline-momentum)
  - [Remote Work and Role Mix](#remote-work-and-role-mix)
- [Recommendations](#recommendations)
- [Assumptions and Caveats](#assumptions-and-caveats)
- [Reproducibility & Assets](#reproducibility--assets)

***

## Project Background
This analysis transforms the Kaggle Human Resources dataset (20k employee records through 2020) into a production-ready data product and insight pack for the HR Leadership Team of a national professional-services firm. The brief: quantify retention risks, surface demographic trends, and deliver an evidence-based roadmap the HR business partners can action in quarterly planning.

The insights below are calculated from the cleaned dataset at `data/processed/Cleaned_HR_Data.csv`, which is produced by the Python pipeline in this repo and feeds the refreshed Power BI dashboard (`hr_dashboard.pbix`).

## Executive Summary
- Workforce of **20,304 employees**, with **17,770 active** and an overall attrition rate of **12.5%** (2,534 exits recorded through 2025).
- A **mid-career heavy population**: median age **37** and **59%** of employees are between **25-44**. Tenure skews long—median active tenure is **15.1 years**, signalling deep institutional knowledge but limited recent hiring.
- **Headquarters concentration** persists: **75%** of active employees sit in HQ roles located primarily in **Ohio (81%)**, constraining geographic resilience and succession coverage.
- **Engineering, Accounting, Human Resources, Sales, and Services** account for half of active headcount; **Auditing (20.8%) and Legal (15.6%)** show the steepest attrition, highlighting niche capability risk.
- Remote work adoption is modest (**24.9%**) but consistent across corporate functions, suggesting remote-first policies can be scaled without materially disrupting department mix.

*Dashboard preview*: see `dashboard.pdf` for the static Power BI export aligned to these insights.

## Insights Deep-Dive

### Workforce Composition
- **Balanced gender mix** across active staff (Male 50.8%, Female 46.4%, Non-Conforming 2.7%) supports enterprise diversity goals, though non-binary representation remains small.
- **Racial diversity is broad**: five groups (White 28.3%, Two or More Races 16.6%, Black or African American 16.2%, Asian 16.0%, Hispanic or Latino 11.5%) each contribute double-digit representation, enabling inclusive talent programming.
- **Mid-career dominance**: 25–44-year-olds make up 59.4% of headcount, while only 11.2% are emerging talent aged 18–24, signalling a future pipeline gap if hiring velocity does not increase.

### Tenure and Retention
- **Median active tenure is 15.1 years**; 50.8% of employees have been with the firm for 15+ years. This stabilises institutional knowledge but suppresses upward mobility and innovation unless complemented by targeted recruitment.
- **Attrition is concentrated early**: exiting employees have an average tenure of **8.3 years** (median 7.5). Departure peaks at the 7–10 year mark, pointing to mid-career advancement friction.
- Annual exits have trended between **136–182** over the last five recorded years, roughly in line with historical norms despite the pandemic-era disruption.

### Department Health
- **Engineering (5,329 active), Accounting (2,674), Sales (1,445), Human Resources (1,439), and Services (1,363)** comprise the largest active cohorts and should anchor succession planning.
- **Auditing’s attrition rate (20.8%)** is nearly double the enterprise average, but the team is small (48 employees). **Legal (15.6%), Training (12.9%), Sales (12.8%), and Human Resources (12.8%)** also exceed the threshold for leadership attention.
- **Role repetition is high**: the top-10 job titles (e.g., Research Assistant II, Business Analyst, Staff Accountant I) cover 3,866 active employees. Targeted job family reviews can unlock efficiencies in learning-path design and workforce planning.

### Geographic Footprint
- **Ohio hosts 81.1% of employees**, amplified by the 75.1% Headquarters share. Pennsylvania (5.1%), Illinois (4.0%), Indiana (3.1%), and Michigan (3.1%) form the secondary hubs.
- The narrow footprint increases disaster recovery and recruitment risks; relocating or hiring remote pods in underserved states could diversify talent access.

### Talent Pipeline Momentum
- The firm hired roughly **1,000 people per year from 2011–2019**, but hiring volume slipped to **920 in 2020**, and no post-2020 hires appear in the dataset—likely due to data cut-off.
- With no employees under 4.9 years of tenure, the current pipeline does not include the post-2020 cohorts typically used to fill entry-level and emerging leader pools. HR should validate whether data integration gaps or hiring freezes drove this trend.

### Remote Work and Role Mix
- **Remote talent represents 24.9%** of active staff but is evenly distributed across the top corporate functions (Accounting, HR, Product Management, Engineering each show ~25–26% remote share).
- The homogeneous remote adoption rate suggests policy standardisation is feasible. Departments that remain heavily HQ-based (e.g., Services, Training) could pilot hybrid support models without disrupting overall coverage.

### Visual Gallery (Optional)
- Run `python scripts/create_visuals.py` to render the bar and pie charts that correspond to the insights above.  
- PNG files (age composition, department headcount, attrition leaders, location split) will be written to `docs/visualizations/` and can be embedded in slide decks or refreshed quarterly.

## Recommendations
1. **Strengthen the Talent Pipeline**  
   - Restart graduate and early-career programs to rebalance the age/tenure pyramid; set FY targets to restore 18–24 representation above 15%.  
   - Deploy analytics dashboards that flag when a department’s median tenure exceeds 12 years so HRBPs can plan succession rotations.
2. **Targeted Retention Interventions**  
   - Partner with Auditing and Legal leadership to diagnose root causes behind attrition rates (>15%)—focus on career path clarity, workload, and compensation alignment.  
   - Launch mid-career retention pilots (7–10 year tenure band) emphasising mentorship, internal mobility sprints, and recognition to curb exits at the tipping point.
3. **Diversify Geography and Ways of Working**  
   - Expand remote hiring in non-Ohio markets to reduce geographic concentration; prioritise states with proven remote success (e.g., Pennsylvania, Illinois).  
   - Translate learnings from remote-friendly departments into playbooks for customer-facing teams, enabling 5–10% year-over-year growth in remote coverage without service degradation.

## Assumptions and Caveats
- **Data Horizon**: The cleaned CSV includes hires through December 2020 and terminations through 2025. There are no post-2020 hires, so entry-level trends may be understated if newer cohorts exist in production systems.
- **Future-Dated Terminations**: A small number of rows contain termination timestamps beyond the extract date. The pipeline treats dates after `today()` as still-active records.
- **Job Family Standardisation**: Titles remain granular (e.g., “Research Assistant I” vs “II”). Additional harmonisation may be required for benchmarking against external sources.
- **Geography Coverage**: State values are US-centric; international employees may be absent or grouped under Remote. Cross-check with HRIS geography fields before global reporting.
- **Non-Binary Representation**: The dataset includes a “Non-Conforming” gender category. Ensure reporting guidelines comply with privacy and regulatory standards before public disclosure.

## Reproducibility & Assets
- **Python Package**: `src/hr_data_insights/` contains modular cleaning, validation, and analytics logic. Run `python scripts/run_pipeline.py` to regenerate `data/processed/Cleaned_HR_Data.csv` and the analytics tables used above.
- **SQL Deliverables**:  
  - `sql/01_clean_hr_dataset.sql` rebuilds an `hr_clean` table and reusable date-parsing function.  
  - `sql/02_hr_analytics_views.sql` publishes BI-ready views (`vw_hr_gender_breakdown`, `vw_hr_department_turnover`, etc.).
- **Notebook Walkthrough**: `hr_cleaning.ipynb` demonstrates how to execute the pipeline, inspect validation warnings, and preview analytics tables interactively.
- **Power BI Dashboard**: Refresh `hr_dashboard.pbix` against the processed CSV or SQL views to visualise the KPIs cited above. A static export is available in `dashboard.pdf`.
- **Static Visuals**: Execute `python scripts/create_visuals.py` to generate PNG charts stored under `docs/visualizations/`.
- **Testing**: Run `pytest` to validate critical cleaning functions before promoting updates.
