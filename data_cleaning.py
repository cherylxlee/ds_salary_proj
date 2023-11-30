# -*- coding: utf-8 -*-
"""
@author: cherylee
"""

import pandas as pd

df = pd.read_csv(r'glassdoor_jobs.csv')

salary  = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_K = salary.apply(lambda x: x.replace('K', ' ').replace('$', ' '))

df['min_salary'] = minus_K.apply(lambda x: int(x.split('-')[0]))

def extract_max_salary(salary_estimate):
    salary_parts = salary_estimate.split('-')
    if len(salary_parts) > 1:
        return salary_parts[1]
    else:
        return None  # Handle cases where there is no max salary

df['max_salary'] = minus_K.apply(extract_max_salary)

df['max_salary'] = df['max_salary'].fillna(df['min_salary'])
df['max_salary'] = df['max_salary'].astype('int')
df['avg_salary'] = (df['max_salary'] + df['min_salary'])/2


# company name text only
df['Company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)

# state field
def extract_state_location(Location):
    split = Location.split(',')
    if len(split) > 1:
        return split[1]
    elif split[0] == 'remote': 
        return 'remote' # Handle the location with no state and remote jobs
    else:
        return split[0] 
    
df['Job_State'] = df['Location'].apply(extract_state_location)

df.Job_State.value_counts()
    

#age of the company
df['age_of_company'] = df.Founded.apply(lambda x: x if x < 1 else 2023 - x)

# parsing of job description(python, etc.)

# python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['python_yn'].value_counts()

# sql
df['sql_yn'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() or 'SQL' in x.lower() else 0)
df['sql_yn'].value_counts()

# excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['excel_yn'].value_counts()


# spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['spark_yn'].value_counts()

# aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['aws_yn'].value_counts()


# industry variable
df['Industry'] = df['Industry'].apply(lambda x: 'unknown' if x == '-1' else x)

# sector variable
df['Sector'] = df['Sector'].apply(lambda x: 'unknown' if x == '-1' else x)

# 'type of ownership' variable
df['Type of ownership'] = df['Type of ownership'].apply(lambda x: 'unknown' if x == '-1' else x)


df.to_csv('salary_data_cleaned.csv', index=False)