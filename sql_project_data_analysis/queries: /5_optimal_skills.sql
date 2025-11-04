WITH skills_demand as (
    SELECT skills_dim.skill_id,
        skills_dim.skills,
        count(skills_job_dim.job_id) as demand_count
    FROM job_postings_fact
        INNER JOIN skills_job_dim ON job_postings_fact.job_id = skills_job_dim.job_id
        INNER JOIN skills_dim ON skills_job_dim.skill_id = skills_dim.skill_id
    WHERE job_title_short = 'Data Analyst'
        and salary_year_avg is not null
        and job_work_from_home = TRUE
    group by skills_dim.skill_id
    order by demand_count desc
),
avg_salary as (
    SELECT skills_job_dim.skill_id,
        round(AVG(salary_year_avg), 0) as avg_salary
    FROM job_postings_fact
        INNER JOIN skills_job_dim ON job_postings_fact.job_id = skills_job_dim.job_id
        INNER JOIN skills_dim ON skills_job_dim.skill_id = skills_dim.skill_id
    WHERE job_title_short = 'Data Analyst'
        and salary_year_avg is not null
        and job_work_from_home = true
    group by skills_job_dim.skill_id
)
SELECT skills_demand.skill_id,
    skills_demand.skills,
    demand_count,
    avg_salary
FROM skills_demand
    INNER JOIN avg_salary on skills_demand.skill_id = avg_salary.skill_id
where demand_count > 10
order by avg_salary desc,
    demand_count DESC
limit 25;