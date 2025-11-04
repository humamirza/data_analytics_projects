/* 
Question: what skills are required for the top paying data analyst jobs?
- use the top 10 highest-paying data analyst jobs from first query
- add specific skills required for these roles
- why? it provides a detailed look at which high-paying jobs demand certain skills, 
helping job seekers understand which skills to develop that align with top salaries
*/

WITH top_paying_job_skills AS (
SELECT 
    job_id,
    job_title,
    salary_year_avg,
    name as company_name
FROM 
    job_postings_fact
LEFT JOIN company_dim ON job_postings_fact.company_id = company_dim.company_id
WHERE 
    salary_year_avg is not NULL AND 
    job_location = 'Anywhere' AND 
    job_title_short = 'Data Analyst'
ORDER BY salary_year_avg DESC
limit 10
)


SELECT 
    top_paying_job_skills.*,
    skills
FROM 
    top_paying_job_skills
INNER JOIN skills_job_dim ON top_paying_job_skills.job_id = skills_job_dim.job_id
INNER JOIN skills_dim ON skills_job_dim.skill_id = skills_dim.skill_id
ORDER BY salary_year_avg DESC