# -*- coding: utf-8 -*-
"""
@author: cherylee
"""

import glassdoor_scraper as gs 
import pandas as pd 

# Update path to where your current chrome driver is
path = r"C:/Users/Cheryl/ds_salary_proj/chromedriver.exe"

df = gs.get_jobs('data_scientist', 500, False, path, 20)

df.to_csv("glassdoor_jobs.csv", index=False)