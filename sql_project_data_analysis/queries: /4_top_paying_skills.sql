/* filter skills by their salaries */

SELECT 
    skills,
    round(AVG(salary_year_avg), 0) as avg_salary
FROM 
    job_postings_fact
INNER JOIN skills_job_dim ON job_postings_fact.job_id = skills_job_dim.job_id
INNER JOIN skills_dim ON skills_job_dim.skill_id = skills_dim.skill_id
WHERE job_title_short = 'Data Analyst' and salary_year_avg is not null 
 -- and job_work_from_home = true
group by skills
order by avg_salary desc
LIMIT 25
