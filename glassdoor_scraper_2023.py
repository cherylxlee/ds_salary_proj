# -*- coding: utf-8 -*-
"""
@author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
@adapted for 2023 by cherylee
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import pandas as pd
import time

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    # Initializing the webdriver
    service = Service(executable_path=path)
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click() #clicking to the X.
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed')
            pass
    
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "jl")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, './/div[@class="employerName"]').text
                    location = driver.find_element(By.XPATH, './/div[@class="location"]').text
                    job_title = driver.find_element(By.XPATH, './/div[contains(@class, "title")]').text
                    job_description = driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH, './/span[@class="gray salary"]').text
            except NoSuchElementException:
                salary_estimate = -1
            
            try:
                rating = driver.find_element(By.XPATH, './/span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            try:
                driver.find_element(By.XPATH, './/div[@class="tab" and @data-tab-type="overview"]').click()

                headquarters, size, founded, type_of_ownership, industry, sector, revenue, competitors = [-1]*8

                # Extract company details
                # ... [Additional company details extraction]

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                # Set all company details to -1
                pass

            if verbose:
                # Print company details for debugging
                pass

            # Append job information to jobs list
            jobs.append({
                "Job Title": job_title,
                "Salary Estimate": salary_estimate,
                "Job Description": job_description,
                "Rating": rating,
                "Company Name": company_name,
                "Location": location,
                # ... [Additional job details]
            })

        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, './/li[@class="next"]//a').click()
        except NoSuchElementException:
            print(f"Scraping terminated before reaching target number of jobs. Needed {num_jobs}, got {len(jobs)}.")
            break

    driver.quit()
    return pd.DataFrame(jobs)